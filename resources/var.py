
import os
import discord

address = "http://localhost:5000"

allowed_guilds = [discord.Object(704596977576312842)]
allowed_guilds_raw = [704596977576312842]

commandsChannel = 704599391024971887

embed = 0x6600ff
embedFail = 0xFF0000
embedSuccess = 0x00FF00

prefix = "qt!"

voiceChannels = 6

completionEmoji = ":tada:"

botID = 704282608120627250

currency = "<:funny_potion:720925205102592021>"

login = f"https://discord.com/api/oauth2/authorize?client_id={botID}&redirect_uri={address}/login&response_type=code&scope=identify&prompt=none"

invite = f"https://discord.com/api/oauth2/authorize?client_id={botID}&permissions=0&redirect_uri={address}/invited&response_type=code&scope=bot%20applications.commands"

UBversion = "v1"
UBheaders = {"Authorization": os.getenv("UBtoken")}
UBbase = f"https://unbelievaboat.com/api/{UBversion}"