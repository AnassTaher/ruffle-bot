import discord
import os
import datetime
from discord.ext import commands
from dotenv import load_dotenv
from dataclasses import dataclass



if __name__ == '__main__':
    start_time = datetime.time()

    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')
    GENERAL = int(os.getenv('GENERAL'))
    LAUNCHED = int(os.getenv('LAUNCHED'))

    bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
    print("test1")
    bot.run(TOKEN)
    print("test2")

@dataclass
class Config:
    announcement : int = 0
    voting : int = 0

@bot.event
async def on_ready():
    from election import check_for_monday
    channel = bot.get_channel(LAUNCHED)
    await channel.send("I have launched")
    check_for_monday.start()

@bot.event
async def on_command_error(ctx, error):
    return await ctx.send(f"Invalid command, error: {error}")


@bot.command(name='announce')
async def set_announcement(ctx : commands.context.Context, channel : str):
    
    print(channel, type(channel))
    channel_id = int(channel[2:-1])
    print(channel_id)
    given = bot.get_channel(channel_id)
    print(given, type(given))


