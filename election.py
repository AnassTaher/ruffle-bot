import datetime
import asyncio
import discord
from main import bot, GENERAL
from dataclasses import dataclass
from discord.ext import commands, tasks
from collections import defaultdict

# map : {voter : Context.author -> elected : discord.Member}
voted = {}     

# map: {elected : discord.Member -> votes : int} 
votes = defaultdict(lambda: 1)


@dataclass
class Election:
    is_running = False
    previous_winner = None
    disqualified = None

@bot.command()
async def vote(ctx : commands.context.Context, elected : discord.Member):

    channel = bot.get_channel(GENERAL) 
    if not Election.is_running:
        return await channel.send("No election currently running")
    
    if voted.get(ctx.author) == elected:
        return await channel.send(f"You have already voted on {elected}")
    
    if Election.disqualified == elected:
        return await channel.send(f"{elected} has been disqualified from the election")
        
    if voted.get(ctx.author):
        votes[voted[ctx.author]] -= 1   # in case you switch your vote, the last person's votes should decrease by 1

    votes[elected] += 1                 # current person votes increases by 1
    voted[ctx.author] = elected         # the person the user has voted now changes

    await channel.send(f"{ctx.author.name} has voted on {elected.mention} ({votes[elected]} votes)")

@tasks.loop(seconds=10)
async def check_for_monday():

    current_day = datetime.date.today().weekday()
    print(current_day)
    if current_day == 0:
        election.start()
        check_for_monday.stop()
        

@tasks.loop(seconds=30)
async def election():

    channel = bot.get_channel(GENERAL)
    if Election.is_running:
        return await channel.send("An election is already running")
    
    # have to deal with first election this way
    if Election.previous_winner:
        old_winner : discord.Member = Election.previous_winner
        role : discord.Role = discord.utils.get(old_winner.guild.roles, name="admin")
        await old_winner.remove_roles(role) 

    
    Election.is_running = True

    await channel.send("The election has currently started")
    await asyncio.sleep(10)   
    await stop()


async def stop():

    channel = bot.get_channel(GENERAL)
    if not Election.is_running:
        return await channel.send("No election currently running")
    
    Election.is_running = False

    if not votes:
        return await channel.send("No one has been elected")

    winner : discord.Member = max(votes, key=votes.get) 
    role : discord.Role = discord.utils.get(winner.guild.roles, name="admin")
    
    if Election.previous_winner == winner:     
        Election.disqualified = winner
    else:
        Election.disqualified = None

    await winner.add_roles(role)
    await channel.send(f"The election has ended, the winner is {winner.mention} with {max(votes.values())} votes")

    Election.previous_winner = winner           # someone has been elected once 
    votes.clear()
    voted.clear()

@bot.command()
async def end(ctx : commands.context.Context):
    await stop()