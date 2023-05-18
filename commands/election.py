import asyncio
import discord
from dataclasses import dataclass
from discord.ext import commands, tasks
from collections import defaultdict
import inspect
import sys
import settings

bot = None

@dataclass
class Election:
    is_running = False
    previous_winner = None
    disqualified = None

def get_command_names(module):
    return [func for _, func in inspect.getmembers(module) if isinstance(func, commands.core.Command)]

async def setup(setup_bot : commands.Bot):

    global bot
    bot = setup_bot
    current_module = sys.modules[__name__]
    commands = get_command_names(current_module)
    for func in commands:
        bot.add_command(func)


# map : {voter : Context.author -> elected : discord.Member}
voted = {}     

# map: {elected : discord.Member -> votes : int} 
votes = defaultdict(lambda: 1)

@commands.Command
async def vote(ctx : commands.context.Context, elected : discord.Member):

    if ctx.channel.id != settings.Config.voting:
        return await ctx.send("You're not allowed to vote in this channel")
     
    
    if not Election.is_running:
        return await ctx.send("No election currently running")
    
    if voted.get(ctx.author) == elected:
        return await ctx.send(f"You have already voted on {elected}")
    
    if Election.disqualified == elected:
        return await ctx.send(f"{elected} has been disqualified from the election")
        
    if voted.get(ctx.author):
        votes[voted[ctx.author]] -= 1   # in case you switch your vote, the last person's votes should decrease by 1

    votes[elected] += 1                 # current person votes increases by 1
    voted[ctx.author] = elected         # the person the user has voted now changes

    await ctx.send(f"{ctx.author.name} has voted on {elected.mention} ({votes[elected]} votes)")

 
async def election():

    channel = bot.get_channel(settings.Config.announce)
    if Election.is_running:
        return await channel.send("An election is already running")
    
    # have to deal with first election this way
    if Election.previous_winner:
        old_winner : discord.Member = Election.previous_winner
        role : discord.Role = discord.utils.get(old_winner.guild.roles, name="admin")
        await old_winner.remove_roles(role) 

    Election.is_running = True

    await channel.send("The election has currently started")
    await asyncio.sleep(settings.Config.duration)   
    await stop()


async def stop():

    channel = bot.get_channel(settings.Config.announce)
    if not Election.is_running:
        return await channel.send("No election currently running")
    
    Election.is_running = False

    if not votes:
        return await channel.send("No one has been elected")

    winner : discord.Member = max(votes, key=votes.get) 
    role : discord.Role = discord.utils.get(winner.guild.roles, name=settings.Config.role)
    
    if Election.previous_winner == winner:     
        Election.disqualified = winner
    else:
        Election.disqualified = None

    await winner.add_roles(role)
    await channel.send(f"@everyone The election has ended, the winner is {winner.mention} with {max(votes.values())} votes")

    Election.previous_winner = winner           # someone has been elected once 
    votes.clear()
    voted.clear()

@commands.Command
async def start(ctx : commands.context.Context):
    
    to_configure = settings.Config.configured(settings.Config)
    if to_configure:
        return await ctx.send("Configure the following: " + ", ".join(to_configure))
    
    await election()

@commands.Command
@commands.is_owner()
async def end(ctx : commands.context.Context):
    await stop()
