import discord
from discord.ext import commands
import settings

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)

def startup():

    @bot.event
    async def on_ready():

        for file in settings.CMDS_DIR.glob("*.py"):
            if file.name != "__init__.py":
                await bot.load_extension(f"commands.{file.name[:-3]}")
    
    bot.run(settings.TOKEN)

@bot.event
async def on_command_error(ctx, error):
    return await ctx.send(f"Invalid command, error: {error}")


@bot.command()
async def help(ctx : commands.context.Context):
    
    
    title = f"""
        Command list
    """

    description = f"""

        Config:
            > *set_announce  channel* :   **!set_announce #general**
            > *set_voting channel* :   **!set_voting #general**
            > *set_duration number unit* : **!set_duration 5 minutes**
            > *set_role name* : **!set_role admin**
                    
        Election:
            > *start* : **!start**
            > *end*   : **!end**
            > *vote @user* : **!vote @user**
        
    """

    embed = discord.Embed(title=title, description=description, color=0x72d345)

    await ctx.send(embed=embed)
    
if __name__ == '__main__':
    startup()






