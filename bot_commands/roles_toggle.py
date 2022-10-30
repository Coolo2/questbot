import discord
from discord.ext import commands

import QuestClient as qc

async def command(client : qc.Client, ctx : commands.Context, role_name : str):
    
    user = qc.classes.User(client, ctx.author)
    roles = user.unlockable_roles 

    for role in roles:
        if role.role.lower() == role_name.lower():

            role_object = qc.var.role_unlockables[role.role]
            member = ctx.guild.get_member(user.user.id)

            if member.get_role(role_object.id):
                await member.remove_roles(role_object)
            else:
                await member.add_roles(role_object)
            
            return await ctx.send(embed=discord.Embed(color=qc.var.embedSuccess, title="Toggled role", description=f"Toggled {role.role.replace('_', ' ').title()} role!"))
    
    raise qc.errors.MildError("You have not unlocked this role or the bot encountered an error while trying to add it to you.")