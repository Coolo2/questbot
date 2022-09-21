
import discord, asyncio
from discord.ext import commands

import QuestClient as qc

from bot_commands import zoo_list, zoo_shop, zoo_buy, zoo_sell, zoo_catalog, zoo_trade, zoo_merge, zoo_shardproducers, zoo_upgrade
from bot_commands import balance, quests, miniquests, start, redeem, tier, leaderboard

from discord import app_commands
from discord.ext.commands.hybrid import hybrid_group

class QuestCommandsCog(commands.Cog):
    def __init__(self, bot, client : qc.Client):
        self.bot = bot
        self.client = client
        
    @commands.hybrid_command(name="quests", description="Check quests", aliases=['myquests'])
    async def _quests(self, ctx : commands.Context, member : discord.Member = None):
        await quests.command(self.client, ctx, member)
    
    @commands.hybrid_command(name="miniquests", description="Check miniquests", aliases=['myminiquests'])
    async def _miniquests(self, ctx : commands.Context, member : discord.Member = None):
        await miniquests.command(self.client, ctx, member)
    
    @commands.hybrid_command(name="start", description="Start a quest or miniquest")
    @app_commands.choices(quest_name=[app_commands.Choice(name=q.name.replace("_", " ").title(), value=q.name) for q in qc.quests + qc.miniquests])
    async def _start(self, ctx : commands.Context, quest_name : str):
        await start.command(self.client, ctx, quest_name)
    
    @commands.hybrid_command(name="redeem", description="Redeem the reward for a quest or miniquest")
    @app_commands.choices(quest_name=[app_commands.Choice(name=q.name.replace("_", " ").title(), value=q.name) for q in qc.quests + qc.miniquests])
    async def _redeem(self, ctx : commands.Context, quest_name : str):
        await redeem.command(self.client, ctx, quest_name)
    
    @commands.hybrid_command(name="tier", description="Redeem the reward for a quest or miniquest")
    @app_commands.choices(quest_name=[app_commands.Choice(name=q.name.replace("_", " ").title(), value=q.name) for q in qc.quests + qc.miniquests])
    async def _tier(self, ctx : commands.Context, quest_name : str):
        await tier.command(self.client, ctx, quest_name)
    
    @commands.hybrid_command(name="balance", description="Get all balances")
    async def _balance(self, ctx : commands.Context, user : discord.User = None):
        await balance.command(self.client, ctx, user)
    
    @commands.hybrid_command(name="leaderboard", description="Show the leaderboard for the server")
    async def _leaderboard(self, ctx : commands.Context):
        await leaderboard.command(self.client, ctx)
    
    @hybrid_group()
    async def zoo(self, ctx):
        pass
    @zoo.group(name="buy", description="Buy something from the zoo shop")
    async def zoo_buy(self, ctx):
        pass 
    @zoo.group(name="trade", description="Trade creatures with another person!")
    async def zoo_trade(self, ctx):
        pass 

    @zoo.command(name="list", description="List creatures in your zoo")
    @app_commands.choices(filter=[app_commands.Choice(name=i, value=i) for i in ["golden", "shiny", "standard"]])
    async def _zoo_list(self, ctx : commands.Context, page : int = None, member : discord.User = None, filter : str = None):

        await zoo_list.command(self.client, ctx, page, member, filter)
    
    @commands.hybrid_command(name="catalog", description="Show the zoo catalog")
    @app_commands.choices(section=[app_commands.Choice(name=i, value=i) for i in ["golden", "shiny", "standard"]])
    async def _zoo_catalog(self, ctx : commands.Context, section : str, user : discord.User = None):
        await zoo_catalog.command(self.client, ctx, section, user)
    
    @zoo.command(name="shop", description="View today's zoo shop")
    async def _zoo_shop(self, ctx : commands.Context):
        await zoo_shop.command(self.client, ctx)
    
    @zoo.command(name="merge", description="Merge creatures to make a shard producer!")
    @app_commands.autocomplete(creature=qc.autocompletes.mergeable_autocomplete)
    async def _zoo_merge(self, ctx : commands.Context, creature : str):
        await zoo_merge.command(self.client, ctx, creature)
    
    @zoo.command(name="shardproducers", description="List someone's shard producers")
    async def _zoo_shardproducers(self, ctx : commands.Context, user : discord.User = None, page : int = None):
        await zoo_shardproducers.command(self.client, ctx, user, page)
    
    @zoo.command(name="upgrade", description="Upgrade a shark producer for stars")
    @app_commands.autocomplete(shard_producer=qc.autocompletes.owned_shard_producers)
    async def _zoo_upgrade(self, ctx : commands.Context, shard_producer : str):
        await zoo_upgrade.command(self.client, ctx, shard_producer)
    
    @zoo.command(name="sell", description="Sell a creature in your zoo")
    @app_commands.autocomplete(creature=qc.autocompletes.owned_creature_autocomplete)
    async def _zoo_sell(self, ctx : commands.Context, creature : str):
        await zoo_sell.command(self.client, ctx, creature)
    
    @zoo_buy.command(name="crate", description="Buy a crate from the zoo shop")
    @app_commands.choices(crate_type=[app_commands.Choice(name=i, value=i) for i in ["creature", "shiny", "collectors"]])
    async def _zoo_buy_crate(self, ctx : commands.Context, crate_type : str):
        await zoo_buy.crate(self.client, ctx, crate_type, self)
    
    @zoo_buy.command(name="quest_xp", description="Convert stars to Quest XP")
    async def _zoo_buy_quest_xp(self, ctx : commands.Context, amount : app_commands.Range[int, 1]):
        await zoo_buy.quest_xp(self.client, ctx, amount)
    
    @zoo_trade.command(name="list", description="List ongoing trades")
    @app_commands.choices(bound=[app_commands.Choice(name="Inbound", value="inbound"), app_commands.Choice(name="Outbound", value="outbound")])
    async def _zoo_trade_list(self, ctx : commands.Context, bound : str, user : discord.User = None):
        await zoo_trade.trade_list(self.client, ctx, bound, user)
    
    @zoo_trade.command(name="trade", description="Trade with another player")
    @app_commands.autocomplete(your_creature=qc.autocompletes.owned_creature_autocomplete, their_creature=qc.autocompletes.owned_creature_autocomplete)
    async def _zoo_trade_trade(self, ctx : commands.Context, user : discord.User, your_creature : str, their_creature : str):
        await zoo_trade.trade(self.client, ctx, user, your_creature, their_creature)
    


        

async def setup(bot):
    await bot.add_cog(QuestCommandsCog(bot, bot.client))