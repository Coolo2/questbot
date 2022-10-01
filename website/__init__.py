
import profile
import quart 
import discord
import os
import logging

from resources import var

import QuestClient as qc

from discord.ext import commands
import json

import discordoauth
from discordoauth import errors as oauth_errors

import urllib.parse
import secrets

import typing

users = {}

async def generate_app(bot : commands.Bot, client : qc.Client) -> quart.Quart:

    app = quart.Quart(__name__, template_folder=os.path.abspath('./website/html'), static_folder=os.path.abspath("./website/static"))

    oauth_client = discordoauth.Client(
        var.botID,
        var.app_secret
    )

    scopes_identify = discordoauth.Scopes(identify=True)

    if var.production:
        logging.getLogger('quart.serving').setLevel(logging.ERROR)

    if var.production == False:
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        app.config["TEMPLATES_AUTO_RELOAD"] = True

    @app.route("/", methods=["GET"])
    async def _index():
        return await quart.render_template("index.html", address=var.address)
    
    @app.route("/profile/<path:user>", methods=["GET"])
    async def _profile(user):
        return await quart.render_template("profile.html", address=var.address)
    
    @app.route("/api/xp", methods=["GET"])
    async def _api_xp():
        with open("data/values.json") as f:
            xp = json.load(f)
        
        return quart.jsonify(xp)
    
    @app.route("/api/creatures", methods=["GET"])
    async def _api_creatures():
        with open("resources/zoo/creatures.json") as f:
            creatures = json.load(f)
        
        return quart.jsonify(client.get_zoo().creatures)
    
    @app.route("/api/emojis", methods=["GET"])
    async def _api_emojis():
        with open("resources/zoo/emojis.json", encoding="utf-8") as f:
            emojis = json.load(f)
        
        return quart.jsonify(emojis)
    
    @app.route("/api/profile/<path:user_id>", methods=["GET"])
    async def _api_profile(user_id):

        guild = bot.get_guild(client.var.allowed_guilds[0].id)
        
        user = bot.get_user(int(user_id))
        cl_user = qc.classes.User(client, user)
        await cl_user.economy.loadBal(guild)

        web = qc.classes.Web(client)

        data = {}

        data["user"] = {
            "avatar_url":user.display_avatar.with_size(128).url,
            "name":user.name,
            "id":str(user.id),
            "discriminator":user.discriminator
        }

        data["badges"] = [{"name":b.name, "description":b.description} for b in await cl_user.badge.badges]

        data["balances"] = {
            "ub":{"cash":cl_user.economy.cash, "bank":cl_user.economy.bank, "total":cl_user.economy.total},
            "quest_xp":cl_user.getXP(),
            "shards":cl_user.getShards()
        }

        cl_user.zoo.getZoo()

        data["currency"] = f"https://cdn.discordapp.com/emojis/{client.var.currency.split(':')[2].replace('>', '')}.webp"
        data["creatures"] = cl_user.zoo.creatures

        data["profile_art"] : typing.List[dict] = []
        for name, profile_art in web.profile_art.items():
            d = {
                "name":profile_art.name,
                "file":profile_art.file,
                "owned":False,
                "equipped":False
            }
            if name in cl_user.profile.profile_art:
                d["owned"] = True 
                if cl_user.profile.profile_art[name].equipped == True:
                    d["equipped"] = True

            data["profile_art"].append(d)
        
        
        return quart.jsonify(data)
    
    @app.route("/login", methods=["GET"])
    async def login():
        
        resp = await quart.make_response(quart.redirect(var.identify))

        if "to" in quart.request.args:
            resp.set_cookie("redirectTo", urllib.parse.quote(quart.request.args["to"]))

        return resp
    
    @app.route("/api/user", methods=["GET"])  
    async def userinfo():
        
        code = quart.request.cookies.get('code')
        reuse_token = quart.request.cookies.get("reuse_token")

        session = oauth_client.new_session(code, scopes_identify, var.address+"/return")

        if not code:
            return quart.jsonify({"error":"Not Logged In"})

        if reuse_token in users:
            if "user" in users[reuse_token]:

                user_cached = users[reuse_token]["user"]
                user = client.bot.get_user(int(user_cached["id"])) if "id" in user_cached else None

                if user:
                    for key, value in user._to_minimal_user_json().items():
                        if key == "avatar" or key == "id":
                            continue
                        users[reuse_token]["user"][key] = value
                    

                return quart.jsonify(users[reuse_token]["user"])
        
        rt = secrets.token_urlsafe(16)
        try:
            print(code)
            access = await session.refresh_access_token(code)
        except oauth_errors.HTTPError:
            return quart.jsonify({"error":"Login invalid"})

        user = await session.fetch_user()

        users[rt] = {"access":access, "user":user.raw}

        resp = await quart.make_response(quart.jsonify(user.raw))
        resp.set_cookie("code", access.refresh_token, max_age=8_760*3600)
        resp.set_cookie("reuse_token", rt, max_age=8_760*3600)

        return resp
    
    @app.route("/return", methods=["GET"])  
    async def discord_return():

        if "error" in quart.request.args:
            return quart.redirect("/")

        code = quart.request.args['code']

        session = oauth_client.new_session(code, scopes_identify, var.address+"/return")

        access = await session.get_access_token()

        users[ access.refresh_token ] = {"access":access}

        url = "/"
        if "redirectTo" in quart.request.cookies:
            url = quart.request.cookies.get("redirectTo")

        resp = await quart.make_response(quart.redirect(url))

        if url != "/":
            resp.delete_cookie("redirectTo")

        resp.set_cookie("code", access.refresh_token, max_age=8_760*3600)

        return resp
    
    async def get_member(guild : discord.Guild, request : quart.Request) -> discord.Member:
        reuse_token = request.cookies.get("reuse_token")

        member : discord.Member = guild.get_member(int(users[reuse_token]["user"]["id"]))
        if not member:
            member : discord.Member = await guild.fetch_member(int(users[reuse_token]["user"]["id"]))

        return member
    
        

    return app