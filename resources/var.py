
import os
import discord
import typing

production = False

address = "http://192.168.0.104:5000"
#address = "http://629e-81-98-18-61.ngrok.io"

allowed_guilds = [discord.Object(704596977576312842)]
allowed_guilds_raw = [704596977576312842]

commandsChannel = 704599391024971887

embed = 0x6600ff
embedFail = 0xFF0000
embedSuccess = 0x00FF00

prefix = "qt!"

unb_prefix = "^"
unb_id = 292953664492929025

voiceChannels = 6

completionEmoji = ":tada:"

botID = 704282608120627250
app_secret = os.getenv("secret")

currency = "<:funny_potion:720925205102592021>"
quest_xp_currency = "<:quest_xp:1026167239487000576>"
shards_currency = "<:shards:1026167063057805455>"

identify = f"https://discord.com/api/oauth2/authorize?client_id={botID}&permissions=8&redirect_uri={address}/return&response_type=code&scope=identify%20guilds"

invite = f"https://discord.com/api/oauth2/authorize?client_id={botID}&permissions=0&redirect_uri={address}/invited&response_type=code&scope=bot%20applications.commands"

UBversion = "v1"
UBheaders = {"Authorization": os.getenv("UBtoken")}
UBbase = f"https://unbelievaboat.com/api/{UBversion}"

host = "0.0.0.0"
port = 5000

role_unlockables : typing.Dict[str, discord.Object] = {
    "camo":discord.Object(1031985906397221005), 
    "light_camo":discord.Object(1031995996659519548), 
    "amoled_camo":discord.Object(1031996985324081173),
    "bot":discord.Object(1031997820498100244)
}