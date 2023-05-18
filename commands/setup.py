from discord.ext import commands
import settings
import inspect
import sys

def get_command_names(module):
    return [func for _, func in inspect.getmembers(module) if isinstance(func, commands.core.Command)]

async def setup(setup_bot : commands.Bot):

    global bot
    bot = setup_bot
    current_module = sys.modules[__name__]
    commands = get_command_names(current_module)
    for func in commands:
        bot.add_command(func)

@commands.command(name='set_announce')
@commands.is_owner()
async def set_announcement(ctx : commands.context.Context, channel : str):
    
    channel_id = int(channel[2:-1])
    settings.Config.announce = channel_id
    await ctx.send(f"{channel} is the announcement channel")
    

@commands.command(name='set_voting')
@commands.is_owner()
async def set_vote(ctx : commands.context.Context, channel : str):
    
    channel_id = int(channel[2:-1])
    settings.Config.voting = channel_id
    await ctx.send(f"{channel} is the voting channel")

@commands.command(name='set_duration')
@commands.is_owner()
async def set_duration(ctx : commands.context.Context, duration : int, type : str):
    
    factor = 1
    if type == "minutes":
        factor *= 60
    elif type == "hours":
        factor *= 60

    settings.Config.duration = duration * factor
    
    await ctx.send(f"Elections now take {duration} {type}")

@commands.command(name='set_role')
@commands.is_owner()
async def set_role(ctx : commands.context.Context, name : str):
    
    settings.Config.role = name
    await ctx.send(f"The winner of the elections shall receive the {name} role")