from os import environ as env

SECRET_KEY = env.get('WS_SECRET_KEY', 'flask')
REDIS_URL = env.get('WS_REDIS_URL', 'redis://')
