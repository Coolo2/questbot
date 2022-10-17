#from bot_commands.miniquests import miniquests
import discord
from discord.ext import commands

import QuestClient as qc

from pyppeteer import launch

first = True

async def command(client : qc.Client, ctx : commands.Context, user : discord.User = None):
    global first

    if user == None:
        user = ctx.author
    
    if user.bot:
        raise qc.errors.MildError("Bots don't have profiles!")
    
    if first:
        msg = await ctx.send("First render may take a while...")
    else:
        await ctx.defer()

    browser = await launch(options={'args': ['--no-sandbox']})
    page = await browser.newPage()
    await page.setViewport(viewport={'width': 1000, 'height': 530})
    await page.goto(f'{qc.var.address}/profile/{user.id}?instant=true', headless=True, waitUntil='networkidle0' )
    await page.screenshot({'path': 'screenshot.png', "omitBackground":True})
    await browser.close()

    view = discord.ui.View()
    view.add_item(discord.ui.Button(url=f"{qc.var.address}/profile/{user.id}", emoji="📃", label="View profile"))
    if user == ctx.author:
        view.add_item(discord.ui.Button(url=f"{qc.var.address}/profile/{user.id}/edit", emoji="✏️", label="Edit profile"))

    if first:
        first = False
        return await msg.edit(attachments=[discord.File("screenshot.png")], view=view, content=None)

    return await ctx.send(file=discord.File("screenshot.png"), view=view)