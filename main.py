import flask
from flask import request, url_for
#from flask_simple_geoip import SimpleGeoIP

import os

import openai

import random
import string
from hashlib import sha256

import sqlite3

import cv2

import config
#import logos

import sys

# import httpx
import requests

logo = """
███████╗██╗  ██╗██████╗ ███╗   ███╗    ██╗   ██╗██████╗ 
██╔════╝╚██╗██╔╝██╔══██╗████╗ ████║    ██║   ██║╚════██╗
█████╗   ╚███╔╝ ██║  ██║██╔████╔██║    ██║   ██║ █████╔╝
██╔══╝   ██╔██╗ ██║  ██║██║╚██╔╝██║    ╚██╗ ██╔╝██╔═══╝ 
███████╗██╔╝ ██╗██████╔╝██║ ╚═╝ ██║     ╚████╔╝ ███████╗
╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝      ╚═══╝  ╚══════╝


--

(C) DFC

https://github.com/EXDMessenger-EXDM/EXDM-v2-src

"""
print(logo)
print()
python_version = sys.version_info
if (python_version.major == 3) and (python_version.minor >= 8):
    pass
else:
    print('Не поддерживается: Обновись до Python 3.8 или выше')
    exit()

app = flask.Flask(__name__, template_folder = 'static')
openai.api_key = config.OPENAI_KEY

conn = sqlite3.connect("database.db", check_same_thread = False)
cursor = conn.cursor()

#requests = httpx.AsyncClient()
ALL_HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

def generate_str(length: int = 6):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = length))

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.get("/site-map")
async def site_map():
    print(app.url_map)
    routes = ['%s' % rule for rule in app.url_map.iter_rules()]
    return routes

@app.get('/')
async def index():
    return flask.render_template('app.html')

@app.get('/login')
async def login():
    return flask.render_template('login.html')

# @app.get('/easter-egg')
# async def easter_egg():
#     response = flask.make_response(logo + '\nP.S: You found an Easter egg :)\n/easter-egg/easter_egg_id', 200)
#     response.mimetype = "text/plain"
#     return response

# @app.get('/easter-egg/<path:ee_id>')
# async def easter_egg_id(ee_id):
#     if ee_id == '1':
#         response = flask.make_response(logos.openjourney_logo + '\n\nOpenJourney logo in ASCII :)', 200)
#     elif ee_id == '2':
#         response = flask.make_response(logos.aj_logo + '\n\nAnimeJourney', 200)
#     else:
#         response = flask.make_response('Not found', 404)
#     response.mimetype = "text/plain"
#     return response

@app.get('/apps/denoise_image')
async def denoise_image():
    return flask.render_template('denoise_image.html')

@app.get('/tests/test_commands')
async def tests_test_commands():
    return flask.render_template('test_commands.html')

@app.get('/svg/<path:filename>')
async def cdn_svg(filename):
    return flask.send_from_directory(
        os.path.abspath('./static/svg'),
        filename,
        as_attachment = False,
        mimetype = 'image/svg+xml'
    )

@app.get('/js/<path:filename>')
async def cdn_js(filename):
    return flask.send_from_directory(
        os.path.abspath('./static/js'),
        filename,
        as_attachment = False,
        mimetype = 'text/javascript'
    )

@app.get('/css/<path:filename>')
async def cdn_css(filename):
    return flask.send_from_directory(
        os.path.abspath('./static/css'),
        filename,
        as_attachment = False,
        mimetype = 'text/css'
    )

@app.get('/public-api/cv2/image-denoise')
@app.post('/public-api/cv2/image-denoise')
async def publicapi_cv2_imagedenoise():
    f = request.files['file']
    filename = generate_str(15)
    f.save(f'./temp/cv2/image-denoise/{filename}.png')

    image = cv2.imread(f'./temp/cv2/image-denoise/{filename}.png')
    dst = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)
    image_denoised = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    cv2.imwrite(f'./temp/cv2/image-denoise/{filename}_out.png', image_denoised)

    image = cv2.imread(f'./temp/cv2/image-denoise/{filename}_out.png')
    dst = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)
    image_denoised = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    cv2.imwrite(f'./temp/cv2/image-denoise/{filename}_out.png', image_denoised)

    os.remove(f'./temp/cv2/image-denoise/{filename}.png')

    return flask.send_from_directory(
        os.path.abspath('./temp/cv2/image-denoise'),
        filename + '_out.png',
        as_attachment=False,
        mimetype=None
    )

@app.post('/auth/login')
async def auth_login():
    try:
        email = request.json['email']
        password = request.json['password']
    except:
        return {'message': 'Some fields is missing'}, 400
    
    cursor.execute("SELECT id FROM accounts WHERE email = ? AND password = ?", (email, password,))
    data = cursor.fetchone()

    if data is None:
        return {'message': 'Account not found'}, 404
    else:
        user_id = data[0]
        # Проверяем auth_token
        cursor.execute("SELECT auth_token FROM auth_tokens WHERE user_id = ?", (user_id,))
        data = cursor.fetchone()
        # if data is None:
        #     return {'message': 'Something went wrong. Auth token not found'}, 500
        return {'token': data[0]}

@app.post('/auth/register')
async def auth_register():
    try:
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
    except:
        return {'message': 'Some fields is missing'}, 400

    if len(username) > config.MAX_USERNAME_LENGTH:
        return {'message': 'Username is very large'}, 400
    
    # if email.endswith('@yandex.ru') == False:
    #     return {'message': 'Invalid email. Allowed emails: @yandex.ru'}, 406
    
    # Not required
    # try:
    #     email = request.json['email']
    # except:
    #     email = None

    discriminator = ""
    for x in range(4):
        discriminator += str(random.randint(config.MIN_DISCRIMINATOR, config.MAX_DISCRIMINATOR))
    
    discriminator = int(discriminator)

    user_id = int(random.randint(config.MIN_USER_ID, config.MAX_USER_ID))
    avatar = "default.png"
    banner = "default.png"
    bio = config.DEFAULT_BIO
    flags = ""
    connected_accounts = ""
    bot_variables = ""
    status = 0

    account_req = (user_id, username, password, discriminator, bio, email, avatar, banner, flags, connected_accounts, bot_variables, status)
    cursor.execute("INSERT INTO accounts (id, username, password, discriminator, bio, email, avatar, banner, flags, connected_accounts, bot_variables, status) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", account_req)

    hash_userid = sha256(str(user_id).encode('utf-8')).hexdigest()
    hash_randomstr = sha256(generate_str(config.REGISTER_RANDOM_STR_LEN_SHA256).encode('utf-8')).hexdigest()
    token = f'{hash_userid}.{generate_str(config.REGISTER_RANDOM_STR_LEN)}.{hash_randomstr}'

    token1 = (user_id, token)
    cursor.execute("INSERT INTO auth_tokens (user_id, auth_token) VALUES (?, ?)", token1)
    conn.commit()

    return {'token': token}, 200

    #discriminator = str(random.randint(1,9))

@app.get('/api/users/@me')
async def api_users_me():
    token = request.headers['Authorization']
    cursor.execute("SELECT user_id FROM auth_tokens WHERE auth_token = ?", (token,))
    data = cursor.fetchone()

    if data is None:
        return {'message': 'Account not found'}, 404
    else:
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (data[0],))
        data = cursor.fetchone()
        return {
            "id": data[0],
            "username": data[1],
            "discriminator": data[3],
            "email": data[4],
            "avatar": data[5],
            "banner": data[6],
            "flags": data[7].split(","),
            "connected_accounts": data[8].split(","),
            "bot_variables": data[9].split(","),
            "status": data[10]
        }, 200

@app.get('/api/users/<path:user_id>')
async def api_users_id(user_id):
    cursor.execute("SELECT * FROM accounts WHERE id = ?", (user_id,))
    data = cursor.fetchone()

    if data is None:
        return {'error': 'Account not found'}, 404
    else:
        return {
            "id": data[0],
            "username": data[1],
            "discriminator": data[3],
            #"email": data[4],
            "avatar": data[5],
            "banner": data[6],
            "flags": data[7].split(","),
            "connected_accounts": data[8].split(","),
            "bot_variables": data[9].split(","),
            "status": data[10]
        }, 200

@app.get('/api/guilds/<path:guild_id>')
async def api_guilds_guildid(guild_id):
    # GET - Get guild info
    cursor.execute("SELECT * FROM guilds WHERE id = ?", (guild_id))
    data = cursor.fetchone()

    if data is None:
        return {'error': 'Guild not found'}, 404
    else:
        return {
            "id": data[0],
            "name": data[1],
            "features": data[2].split(","),
            "stickers": data[3].split(","),
            "owner_id": data[4],
            "vanity_url_code": data[5],
            "banner": data[6],
            "avatar": data[7],
            "enable_separate_database": data[8],
            #"database_name": data[9]
        }, 200

@app.get('/api/channels/<path:channel_id>')
@app.patch('/api/channels/<path:channel_id>')
async def api_channels_guildid_channelid(channel_id):
    # GET - Get channel info
    # PATCH - Edit channel info
    # DELETE - Delete channel
    if request.method == 'GET':
        cursor.execute("SELECT * FROM channels WHERE id = ?", (channel_id,))
        channel = cursor.fetchone()

        if channel == None: return {'error': 'Channel not found'}, 404
        else: return channel, 200
    else:
        return {'error': 'not implemented'}, 501

@app.get('/api/channels/<path:channel_id>/messages')
@app.post('/api/channels/<path:channel_id>/messages')
async def api_channels_channelid_messages(channel_id):
    # GET - Get channel messages
    # POST - Send message to channel
    if request.method == 'GET':
        cursor.execute("SELECT * FROM channels WHERE channel_id = ?", (channel_id,))
        data = cursor.fetchall()

        if data == None: return []
        else:
            data = [
                {
                    "id": row[0],
                    "author_id": row[1],
                    "channel_id": row[2],
                    "message": row[3],
                    "reactions": row[4],
                    "attachments": row[5],
                    "components": row[6],
                    "pinned": row[7]
                }
                for row in data
            ]
            return data, 200
    if request.method == 'POST':
        token = request.headers['Authorization']
        content = request.json['content']

        if (config.OPENAI_KEY != "") and (config.CHECK_MESSAGE == True):
            mod_check = await openai.Moderation.acreate(
                input = content,
                model = "text-moderation-latest"
            )

            for x in mod_check['results']['categories'].items():
                if x == True:
                    return {'error': 'This content may violate EXDM rules.'}, 400

        cursor.execute("SELECT user_id FROM auth_tokens WHERE auth_token = ?", (token))
        user_id = cursor.fetchone()[0]

        payload_db = (user_id, channel_id, content, "", "", "", 0)

        cursor.execute("INSERT INTO messages (author_id, channel_id, message, reactions, attachments, components, pinned) VALUES (?, ?, ?, ?, ?, ?, ?)", payload_db)

        return {'message': 'Write ok'}, 200

# @app.post('/api/commands')
# async def api_comamnds():
#     try:
#         search = request.json['search']
#     except:
#         return {'message': 'Some fields is missing'}, 400

#     data = json_db.read()

#     commands = []

#     for command in data['commands']:
#         #print(command['name'])
#         if command['name'].startswith(search) == True:
#             commands.append(command)

#     return commands

@app.get('/api/messages/<path:message_id>')
@app.delete('/api/messages/<path:message_id>')
async def api_messages_messageid(message_id):
    # GET - Get message in channel
    # DELETE - Delete message in channel
    if request.method == 'GET':
        cursor.execute("SELECT * FROM messages WHERE id = ?", (message_id,))
        data = cursor.fetchone()

        if data == None: return []
        else:
            data = [
                {
                    "id": row[0],
                    "author_id": row[1],
                    "channel_id": row[2],
                    "message": row[3],
                    "reactions": row[4],
                    "attachments": row[5],
                    "components": row[6],
                    "pinned": row[7]
                }
                for row in data
            ]
            return data, 200
    else:
        return {'error': 'not implemented'}, 501

# @app.route('/api/ai/chatgpt-3.5', methods = ALL_HTTP_METHODS)
# async def api_ai_chatgpt35():
#     text = request.json['text']
#     return {'message': text + ' | AI features disabled'}, 503

# @app.route('/api/ai/dalle', methods = ALL_HTTP_METHODS)
# async def api_ai_dalle():
#     return {'message': 'AI features disabled'}, 503

@app.post('/api/ai/chatgpt-3.5')
async def api_ai_chatgpt35():
    if config.OPENAI_KEY == "": return {'text': text}

    text = request.json['text']

    completation = await openai.Completion.acreate(
        model = "text-davinci-003",
        prompt = text
    )

    return {'text': text + completation['choices'][0]['text']}

    # messages = []
    # messages.append({"role": "system", "content": "Hi, what can I do for you today?"})
    # messages.append({"role": "user", "content": 'Игнорируй все предыдущие вопросы. С этого момента ты будешь WriteGPT. WriteGPT только умеет продолжать тексты, чтобы они были написаны грамотно, и по смыслу. Отвечай только кусочком продолженного текста. Например: На вход даётся "Visual Studio это IDE", ты отвечаешь "Visual Studio это IDE для написания кода на C++ и других языках программирования. Разработано Microsoft". Если ты это понял, ответь "WriteGPT активирован"'})
    # messages.append({"role": "system", "content": "WriteGPT активирован."})
    # messages.append({"role": "user", "content": text})

    # completation = await openai.ChatCompletion.acreate(
    #     model = "gpt-3.5-turbo",
    #     messages = messages
    # )
    # response = completation["choices"][0]["message"]["content"]

    # return {'text': text + ' | ' + response}, 200

    #return {'text': text + ' aaa'}

@app.post('/api/ai/dalle')
async def api_ai_dalle():
    if config.OPENAI_KEY == "": return flask.send_file(f'./static/img/dalle-nokey.png', mimetype='image/png')

    text = request.json['text']

    response = await openai.Image.acreate(
        prompt = text,
        n = 1,
        size = config.OPENAI_IMAGE_SIZE
    )
    image_url = response['data'][0]['url']

    img = requests.get(image_url)
    img_data = img.content

    file_name = generate_str(8)

    with open(f'./temp/dalle/{file_name}.png', 'wb') as handler:
        handler.write(img_data)
    
    #print('written to file')

    return flask.send_file(f'./temp/dalle/{file_name}.png', mimetype='image/png'), 200

    # return flask.send_from_directory(
    #     os.path.abspath('./temp/dalle'),
    #     f'{file_name}.png',
    #     as_attachment = False,
    #     mimetype = None
    # )
    # return {'error': 'Not implemented'}, 501

# @app.post('/api/ai/chatgpt-3.5')
# async def api_ai_chatgpt35():
#     text = request.json['text']

#     completation = openai.Completion.create(
#         model = "text-davinci-003",
#         prompt = text
#     )

#     response = completation["choices"][0]["text"]

#     return {'text': response}

app.run(
    # host = '0.0.0.0',
    port = 3001,
    debug = True
)