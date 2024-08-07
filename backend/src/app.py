from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeme!'
socketio = SocketIO(app)

mouse_peps = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    emit('my response', json)

@socketio.on('mouse_event')
def handle_mouse_event(i, x, y):
    print("id: {}, x: {}, y: {}".format(i, x, y))
    mouse_peps[i] = (x, y)
    emit('mouse_people', mouse_peps, broadcast=True)


if __name__ == '__main__':
    socketio.run(app)

