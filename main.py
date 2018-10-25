from flask import Flask, render_template
from flask_socketio import SocketIO
<<<<<<< Updated upstream
import sys
import os
=======
import sys, datetime

>>>>>>> Stashed changes
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

        # The Logic for our !username command.
        elif (str(json['message']) == "!username"):
            json['message'] = "Your Username is: " + json['user_name']
        
        # The Logic for our !help command.
        elif (str(json['message']) == "!help"):
            json['message'] = "Commands: !username, !clear, and of course !help!"

        # The Logic for our !store command.
        elif (str(json['message']) == "!store"):
            print("in store")
            f = open("chatLog.txt", "a+")
            f.write(datetime.date.today().strftime("%I:%M%p on %B %d, %Y"))
            f.write("\n")
            for lines in messages:
                f.write(lines + "\n")
            f.write("\n")
            f.close()
            json['message'] = "Current Chat was correctly stored to chatLog.txt"

        # The Logic for our !clearLog command.
        elif (str(json['message']) == "!clearLog"):
            f = open("chatLog.txt", "w")
            f.write("")
            f.close()
            json['message'] = "Erased Current cache and logging.. Proceed to Chat!"
        
        # Not a correct command logic.
        elif (str(json['message']).startswith('!')):
            json['message'] = "Unrecognized command. Type '!help' for available commands"

        # If it isn't a command then store it in our messages array for later storage.
        else:
            myMessage = str(json['user_name']) + ": " + str(json['message'])

        # Push it to the array and emit it to the client. 
        messages.append(myMessage)
        print("MESSAGES: " + messages)
        socketio.emit('my response', json, callback=messageReceived)

    except:
        socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)