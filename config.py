from os import environ as env

SECRET_KEY = env.get('WS_SECRET_KEY', 'flask')
REDIS_URL = env.get('WS_REDIS_URL', 'redis://')
WS_HOST = env.get('WS_HOST', '0.0.0.0')
WS_PORT = env.get('WS_PORT', 6789)
