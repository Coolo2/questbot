import discord
from discord.ext import commands

import QuestClient as qc

async def command(client : qc.Client, ctx : commands.Context, user_disc : discord.User = None):
    if user_disc == None:
        user_disc = ctx.author
    
    user = qc.classes.User(client, user_disc)
    roles = user.unlockable_roles 

    embed = discord.Embed(title="Your toggleable roles: ", color=qc.var.embed)

    for role in roles:
        role_object = qc.var.role_unlockables[role.role]
        member = ctx.guild.get_member(user.user.id)

        if member.get_role(role_object.id):
            value = "Toggled on"
        else:
            value = "Toggled off"
        embed.add_field(name=f"{role.role.replace('_', ' ').title()} (level {role.level})", value=value)
    
    if len(embed.fields) == 0:
        embed.description = "*You have not unlocked any roles. Try getting some Quest XP!*"
    
    await ctx.send(embed=embed)