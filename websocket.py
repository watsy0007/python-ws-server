import asyncio
import json
import logging
import websockets as ws
import uuid
import redis
from config import REDIS_URL
from urllib.parse import urlparse

logging.basicConfig()
ticker_users = {}

r = redis.StrictRedis.from_url(REDIS_URL)   

self_id = 'ws_node:{}'.format(str(uuid.uuid4()))

async def handle_ticker(websocket, query):
    query = dict(map(lambda x: x.split('='), query.split('?')))
    uid = str(uuid.uuid4())
    print(uid, type(uid))
    r.sadd(self_id, uid)
    ticker_users[uid] = websocket
    

async def remove_connect(websocket):
    r.srem(self_id, ticker_users[websocket])
    del(ticker_users[websocket])

async def handle_connect(websocket, path):
    r = urlparse(path)
    try:
        if r.path == '/ticker':
            await handle_ticker(websocket, r.query)
    except:
        await remove_connect(websocket)

def run():
    try:
        asyncio.get_event_loop().run_until_complete(ws.serve(handle_connect, 'localhost', 6789))
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print('del key', self_id)
        r.delete(self_id)


if __name__ == "__main__":
    run()