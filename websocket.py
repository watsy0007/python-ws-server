import asyncio
import json
import logging
import websockets as ws
import concurrent.futures
import uuid
import time
import redis
from config import REDIS_URL, WS_HOST, WS_PORT
from urllib.parse import urlparse
from aredis import StrictRedis as AsyncRedis

ticker_users = {}
r = redis.StrictRedis.from_url(REDIS_URL)   
self_id = 'ws_node:{}'.format(str(uuid.uuid4()))

async def handle_ticker(websocket, query):
    query = dict(map(lambda x: x.split('='), query.split('?')))
    uid = str(uuid.uuid4()) # uid 可以用参数代替, 表示来源
    r.sadd(self_id, uid)
    ticker_users[uid] = websocket
    await websocket.send('connected!')

async def remove_connect(websocket):
    r.srem(self_id, ticker_users[websocket])
    del(ticker_users[websocket])
    

async def handle_connect(websocket, path):
    r = urlparse(path)
    try:
        if r.path == '/ticker':
            await handle_ticker(websocket, r.query)
        async for message in websocket:
            print(message)
    except:
        print('what.....')
        await remove_connect(websocket)

async def send_ticker(data):
    for _, user in ticker_users.items():
        await user.send(data)

async def wait_for_message(pubsub, timeout=2, ignore_subscribe_messages=False):
    while True:
        message = await pubsub.get_message(
            ignore_subscribe_messages=ignore_subscribe_messages,
            timeout=1
        )
        if message is not None:
            if message['type'] == 'message' and message['channel'] == b'ticker':
                await send_ticker(message['data'].decode())
        await asyncio.sleep(0.01)
          
    return None

async def subscribe(rds, users):
    pubsub = rds.pubsub()
    assert pubsub.subscribed is False
    await pubsub.subscribe('ticker', 'chat')
    await wait_for_message(pubsub)

def run():
    try:
        client = AsyncRedis.from_url(REDIS_URL)
        asyncio.get_event_loop().run_until_complete(ws.serve(handle_connect, WS_HOST, WS_PORT))
        asyncio.get_event_loop().run_until_complete(asyncio.wait({subscribe(client, ticker_users)}))
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print('del key', self_id)
        r.delete(self_id)


if __name__ == "__main__":
    run()