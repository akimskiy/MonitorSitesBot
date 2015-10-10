#!/usr/bin/env python3

import asyncio
from aiohttp import web
import json
from telegram import Telegram
import rethinkdb as r
import db

token = '136121379:AAFyb9wycaAMEqyAnHvPjkxD0puU0niccd0'
api = Telegram(token)

@asyncio.coroutine
def initBot(request):
    res = api.setWebhook('http://188.226.250.167/w'+token)
    print(res)
    return web.Response(body='ok'.encode('utf-8'))

@asyncio.coroutine
def webhook(request):
    content = yield from request.read()
    string = content.decode('utf-8')
    update = json.loads(string)
    mes = {
        'chat_id': update['message']['chat']['id'],
        'text': 'hello '+update['message']['from']['first_name']
    }
    command = update['message']['text'].partition(' ')
    user_id = update['message']['from']['id']

    conn = db.get_conn()

    if command[0] == '/addsite':
        site = command[2]
        r.table('sites').insert({'site': site, 'user_id': user_id}).run(conn)
        mes['text'] = 'Site '+site+' was added successfully'

    if command[0] == '/list':
        sites = r.table('sites').filter({'user_id': user_id}).run(conn)
        mes['text'] = 'Your sites:\n'
        for site in sites:
            mes['text'] += site['site']+'\n'

    print(api.sendMessage(mes))

    # cursor = r.table('sites').run(conn)
    # for row in cursor:
    #     print(row)
    conn.close()
    return web.Response(body='ok'.encode('utf-8'))

@asyncio.coroutine
def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(body=text.encode('utf-8'))


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('POST', '/w'+token, webhook)
    app.router.add_route('GET', '/initBot', initBot)
    app.router.add_route('GET', '/', handle)

    srv = yield from loop.create_server(app.make_handler(),
                                        '127.0.0.1', 8888)
    print("Server started at http://127.0.0.1:8888")
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
