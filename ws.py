from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import redis
import eventlet
from config import REDIS_URL, SECRET_KEY

eventlet.monkey_patch(socket=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socket_io = SocketIO()


def handle_chat(message):
    socket_io.emit('my response', {'data': message['data'].decode()}, namespace='/chat')


r = redis.StrictRedis.from_url(REDIS_URL)
pub_sub = r.pubsub()
pub_sub.subscribe(**{'chat': handle_chat})
pub_sub.run_in_thread(0.05, True)


@app.route('/')
def index():
    return render_template('index.html')


@socket_io.on('my event', namespace='/chat')
def test_message(message):
    emit('my response', {'data': message['data']})


@socket_io.on('my broadcast event', namespace='/chat')
def test_message_broadcast(message):
    emit('my response', {'data': message['data']}, broadcast=True)


@socket_io.on('connect', namespace='/chat')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socket_io.on('disconnect', namespace='/chat')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socket_io.init_app(app, async_mode='eventlet', message_queue=REDIS_URL)
    socket_io.run(app)
