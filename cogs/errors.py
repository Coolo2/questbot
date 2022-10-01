

import discord 

from discord.ext import commands 
from discord import app_commands 

import QuestClient as qc

class ErrorHandling(commands.Cog):
    def __init__(self, bot : commands.Bot, client : qc.Client):
        self.client = client 
    
        @bot.event
        async def on_command_error(ctx : commands.Context, error : commands.CommandError ):
            embed = discord.Embed(
                title="You've run into an unknown error",
                description=f"```{error}```\n\nMessage <@368071242189897728> for support",
                color=qc.var.embedFail
            )

            if hasattr(error.original, "original") and isinstance(error.original.original, qc.errors.MildError):
                embed = discord.Embed(
                    title=error.original.original.title,
                    description=f"{error.original.original.description}\n\nMessage <@368071242189897728> for support",
                    color=qc.var.embedFail
                )
            elif isinstance(error.original, qc.errors.MildError):
                embed = discord.Embed(
                    title=error.original.title,
                    description=f"{error.original.description}\n\nMessage <@368071242189897728> for support",
                    color=qc.var.embedFail
                )

            try:
                await ctx.send(embed=embed, ephemeral=True)
            except:
                pass

        """@bot.tree.error 
        async def on_error(interaction : discord.Interaction, error : app_commands.AppCommandError):
            print("h")
            embed = discord.Embed(
                title="You've run into an unknown error",
                description=f"```{error}```\n\nMessage <@368071242189897728> for support",
                color=qc.var.embedFail
            )

            if isinstance(error, app_commands.errors.CommandNotFound):
                return

            if isinstance(error.original, qc.errors.MildError):
                embed = discord.Embed(
                    title=error.original.title,
                    description=f"{error.original.description}\n\nMessage <@368071242189897728> for support",
                    color=qc.var.embedFail
                )

            try:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except:
                await interaction.followup.send(embed=embed, ephemeral=True)"""

async def setup(bot : commands.Bot):
    await bot.add_cog(ErrorHandling(bot, bot.client))