from flask import Flask, render_template, Markup, request, send_from_directory, redirect, make_response, jsonify
from threading import Thread
import os, time, json, base64
from resources import var
from website.oauth import Oauth as oauth
from flask_minify import minify
from website import encryption
from gevent.pywsgi import WSGIServer
from gevent import monkey

encryptionKey = os.environ.get("encryptionKey")

bot = None

def webserver_run(client):
    global bot 
    bot = client
    t = Thread(target=run)
    t.start()
    

app = Flask('', template_folder=os.path.abspath('./website/html'))
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["TEMPLATES_AUTO_RELOAD"] = True

minify(app=app, html=True, js=True, cssless=True)

@app.route('/css/<path:filename>')
def custom_static(filename):
    return send_from_directory('webserver/Static/CSS/', filename)

@app.route('/js/<path:filename>')
def custom_js(filename):
    return send_from_directory('webserver/Static/JS/', filename)

@app.route('/images/<path:filename>')
def custom_image(filename):
    return send_from_directory('website/static/images/', filename)

@app.route('/')
def home():

    with open("data/values.json") as f:
        XP = json.load(f)
    return render_template('index.html', last_updated=dir_last_updated('/static'), XPData=Markup(XP))

@app.route('/about')
def about():
    return render_template('about.html', last_updated=dir_last_updated('/static'))

@app.route('/invited')
def invited():
    if request.args.get("guild_id") == None:
        return redirect("/")
    guildName = bot.get_guild(int(request.args['guild_id'])) if bot.get_guild(int(request.args['guild_id'])) else "None"
    return render_template('invited.html', last_updated=dir_last_updated('/static'), guild_name=guildName)

@app.route("/login", methods=["GET"])  
def admin():
    try:
        code = request.args['code']
        print(code)
        access_token=oauth.get_access_token(code)
        print(access_token)
        user_json = oauth.get_user_json(access_token)
        print(user_json)
    except Exception as e:
        print(e)
        return redirect(var.login)
    try:
        id = user_json["id"]
        #user = bot.get_user(int(id))
        resp = make_response(redirect("/#dashboard"))
        cookiestring = ''
        cookiestring = cookiestring + ';;;;' + encryption.encode(str(user_json['id']), encryptionKey).decode("utf-8")
        cookiestring = cookiestring + ';;;;' + encryption.encode(str(user_json['username']), encryptionKey).decode("utf-8")
        cookiestring = cookiestring + ';;;;' + encryption.encode(str(user_json['avatar']), encryptionKey).decode("utf-8")
        resp.set_cookie('user', cookiestring, max_age=8_760*3600)
        return resp
    except Exception as e:
        print(e)
        return redirect("/")

@app.route('/dashboard')
def dashboard():
    try:
        user = request.cookies.get('user').split(";;;;")
        id = encryption.decode(user[1], encryptionKey)
        name = encryption.decode(user[2], encryptionKey)
    except:
        return redirect("/login")
    return render_template('dashboard.html', last_updated=dir_last_updated('/static'))


def jsonifyB(data, status=200, indent=4, sort_keys=True):
    response = make_response(json.dumps(dict(data), indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response











def dir_last_updated(folder):
    try:
        return str(max(os.path.getmtime(os.path.join(root_path, f))
                    for root_path, dirs, files in os.walk(folder)
                    for f in files))
    except:
        return 0

def run():
    try:
        http = WSGIServer(('0.0.0.0', 5000), app.wsgi_app) 
        http.serve_forever()
    #app.run(host='0.0.0.0',port=5000,threaded=True)
    except:
        pass


