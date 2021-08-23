import discord, random
from discord.ext import commands
from resources import var

class errorHandling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        
        msgMild = random.choice(["Uh oh!", "Oops!", "Oh no!"])
        msgUnkown = random.choice(["You've ran into an unknown error!", "You've ran into an error!"])
        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title=msgMild, description=f"```{str(error)}```", colour=var.embedFail, timestamp=ctx.message.created_at)
            return await ctx.send(embed=embed)
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title=msgMild, description=f"```{error}```", colour=var.embedFail, timestamp=ctx.message.created_at)
            return await ctx.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title=msgMild, description=f"```{error}```", colour=var.embedFail, timestamp=ctx.message.created_at)
            return await ctx.send(embed=embed)
        if isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(title=msgMild, description=f"```{error}\n\nEnsure that I have the above permissions and my role is high enough to use {ctx.command.name}```", colour=var.embedFail, timestamp=ctx.message.created_at)
            return await ctx.send(embed=embed)
        if isinstance(error, commands.NoPrivateMessage):
            embed = discord.Embed(title=msgMild, description=f"```{error}```", colour=var.embedFail, timestamp=ctx.message.created_at)
            return await ctx.send(embed=embed)
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=msgMild, description=f"{error}", colour=var.embedFail)
            return await ctx.send(embed=embed)
        if isinstance(error, commands.CommandNotFound):
            command = await self.getCommandFromError(error)

            embed = discord.Embed(title=msgMild, 
                description=f"Command **{var.prefix}{command}** was not found!", colour=var.embedFail, timestamp=ctx.message.created_at)
            return await ctx.send(embed=embed)

        embed = discord.Embed(title=msgUnkown, description=f"```{error}``` DM <@368071242189897728> for support", colour=var.embedFail, timestamp=ctx.message.created_at)
        await ctx.send(embed=embed)
    
    async def getCommandFromError(self, error):
        commands = str(error).replace('Command "', '')
        commands = commands.replace('" is not found', '')

        return commands


def setup(bot):
    bot.add_cog(errorHandling(bot))