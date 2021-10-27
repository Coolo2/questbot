import discord, asyncio
from discord.ext import commands
from discord.ext.commands import MemberConverter
from discord_components import *

from bot_commands import quests, start, redeem, tier, miniquests, xp, leaderboard, buy, list, catalog, sell, trade

class quest_commands(commands.Cog):
    def __init__(self, bot, bot2=None):
        self.bot = bot
        self.bot2 = bot2
        
    @commands.command(name="quests", description="Check quests", aliases=['myquests'])
    @commands.guild_only()
    async def command_quests(self, ctx, member:discord.Member=None):
        await quests.quests(self.bot, ctx, member)
    
    @commands.command(name="miniquests", description="Check miniquests", aliases=['mini-quests'])
    @commands.guild_only()
    async def command_miniquests(self, ctx, member:discord.Member=None):
        await miniquests.miniquests(self.bot, ctx, member)
    
    @commands.command(name="start", description="Start a quest", aliases=['startquest'])
    @commands.guild_only()
    async def command_start(self, ctx, quest):
        await start.start(self.bot, ctx, quest)
    
    @commands.command(name="redeem", description="Redeem a quest", aliases=['redeemquest'])
    @commands.guild_only()
    async def command_redeem(self, ctx, quest):
        await redeem.redeem(self.bot, ctx, quest)
    
    @commands.command(name="tier", description="Tier up in a quest", aliases=['tierup'])
    @commands.guild_only()
    async def command_tier(self, ctx, quest):
        await tier.tier(self.bot, ctx, quest)
    
    @commands.command(name="xp", description="Get a user's quest XP", aliases=['questxp'])
    @commands.guild_only()
    async def command_xp(self, ctx, user : discord.Member = None):
        await xp.xp(self.bot, ctx, user)
    
    @commands.command(name="leaderboard", description="Get the server leaderboard", aliases=['lb', "leaders"])
    @commands.guild_only()
    async def command_leaderboard(self, ctx):
        await leaderboard.leaderboard(self.bot, ctx)
    
    @commands.command(name="buy", description="Buy a Creature Crate", aliases=['buycreature', "buy-creature", "shop", "crate", "buy-crate"])
    @commands.guild_only()
    async def command_buy(self, ctx, crate = None):
        await buy.buy(self.bot, ctx, crate)
    
    @commands.command(name="list", description="List your creatures", aliases=['creatureslist', "creature-list"])
    @commands.guild_only()
    async def command_list(self, ctx, arg1 = None, arg2 = None, arg3 = None):
        await list.command_list(self.bot, ctx, arg1, arg2, arg3)
    
    @commands.command(name="catalog", description="Get the creature catalog", aliases=["creature-catalog", "creaturecatalog"])
    @commands.guild_only()
    async def command_catalog(self, ctx, section = None, page = 1):
        await catalog.catalog(self.bot, ctx, section, page)
    
    @commands.command(name="sell", description="Sell a creature from your collection", aliases=["sell-creature"])
    @commands.guild_only()
    async def command_sell(self, ctx, *, creature = None):
        await sell.sell(self.bot, ctx, creature)
    
    @commands.command(name="trade", description="Trade a creature with someone else", aliases=["trade-creature"])
    @commands.guild_only()
    async def command_trade(self, ctx, arg2 = None, arg3 = None, arg4 = None, arg5 = None, arg6 = None, arg7 = None, arg8 = None, arg9 = None, arg10 = None, arg11 = None):
        await trade.trade(self.bot, ctx, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11)
    
    @commands.command(name="help")
    async def help(self, ctx):
        await ctx.send(", ".join(command.name for command in self.bot.commands))

def setup(bot):
    bot.add_cog(quest_commands(bot))