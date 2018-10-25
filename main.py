from flask import Flask, render_template
from flask_socketio import SocketIO
import sys
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
messages = []

@app.route('/')
def sessions():
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    
    try:
        print(str(json['message']))

        if (str(json['message']) == "!exit"):
            socketio.emit('quit','quitting now')
            os._exit

        elif (str(json['message']) == "!username"):
            json['message'] = "Your Username is: " + json['user_name']
        
        elif (str(json['message']) == "!help"):
            json['message'] = "Commands: !username, !clear, and of course !help!"

        elif (str(json['message']).startswith('!')):
            json['message'] = "Unrecognized command. Type '!help' for available commands"

        else:
            myMessage = str(json['user_name']) + " " + str(json['message'])

        messages.append(myMessage)
        print(messages)
        socketio.emit('my response', json, callback=messageReceived)

    except:
        socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)