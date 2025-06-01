import sys
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO
from flask_mail import Mail, Message

if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    from collections.abc import MutableMapping
else:
    from collections import MutableMapping

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = '71762131028@cit.edu.in'
app.config['MAIL_PASSWORD'] = 'ozgu ubda jyvl kxqk'

mail = Mail(app)
socketio = SocketIO(app, async_mode="threading")  # Use threading as the async mode

# Dictionary to store radio station information
radio_stations = {
    'delhi': {'Radio City': 'http://radionorthsea.zapto.org:8008/stream', 'Red FM': 'http://132.185.209.55/bbc_world_service', 'BBC':'http://132.185.209.52/bbc_world_service'},
    'mumbai': {'Classic FM': 'http://media-ice.musicradio.com:80/ClassicFM-M-Movies', 'Fever FM': 'http://media-ice.musicradio.com/ClassicFMMP3','fnf FM': 'http://192.99.8.192:5032/;stream','Hits of MUmbai':'https://stream-140.zeno.fm/60ef4p33vxquv?zs=98RPr6ouTqmuamV3Q-QJMQ','Joy melodies':'https://stream-159.zeno.fm/9re8ry3qzk0uv?zs=4DhinWr_SeS9pVYG6Z6GTA'},
    'tamil nadu':{'Trumphet madurai':'https://stream-151.zeno.fm/pyrbm4khva0uv?zs=HkDW6NJUQnup6iAtsrQqNQ','Arumbu':'https://stream-155.zeno.fm/22db1xmde2zuv?zs=BDnZcOJISjm8OXXJNDcIug','Geetham':'https://stream-152.zeno.fm/b9vhhaukg5zuv?zs=VB_GdqeOSPSCTxqEBRgjXw','Joyful melodies':'https://edge-audio-06-thn.sharp-stream.com/ssvcbfbs4.mp3'},
    
    # Add more stations for other states
}

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/preferences')
def preferences():
    return render_template('preferences.html')


@app.route('/index')
def index():
    return render_template('index.html')


@socketio.on('get_stations')
def get_stations(data):
    state = data['state'].lower()
    if state in radio_stations:
        stations = list(radio_stations[state].keys())
        socketio.emit('stations_list', {'stations': stations})
    else:
        socketio.emit('stations_list', {'error': 'State not found'})

@socketio.on('play_station')
def play_station(data):
    state = data['state'].lower()
    station_name = data['station']
    if state in radio_stations and station_name in radio_stations[state]:
        streaming_url = radio_stations[state][station_name]
        socketio.emit('start_streaming', {'streaming_url': streaming_url})
    else:
        socketio.emit('start_streaming', {'error': 'Station not found'})

@socketio.on('save_recording')
def save_recording(data):
    filename = f"{data['state']}_{data['station']}_recording.wav"
    with open(filename, 'wb') as f:
        f.write(data['blob'])

@socketio.on('get_recording')
def get_recording(data):
    state = data['state'].lower()
    station = data['station']
    filename = f"{state}_{station}_recording.wav"
    
    try:
        with open(filename, 'rb') as f:
            blob = f.read()
            socketio.emit('send_recording', {'blob': blob})
    except FileNotFoundError:
        socketio.emit('send_recording', {'error': 'Recording not found'})

@app.route('/download_recording', methods=['POST'])
def download_recording():
    data = request.json
    filename = data.get('filename', '')
    folder = '.'  # Change to the folder where your recordings are stored

    try:
        return send_from_directory(folder, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'Recording not found'}), 404
@app.route('/send_email', methods=['POST'])
def send_email_route():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    state = data.get('state')
    station = data.get('station')

    msg = Message('Radio Session Details',
                  sender='your_username@example.com',
                  recipients=[email])

    msg.body = f"Hello {name},\n\nYou have selected {station} station in {state} state.\n\nThank you for using our service!"

    mail.send(msg)

    return jsonify({'message': 'Email sent successfully'})


if __name__ == '__main__':
    socketio.run(app, debug=True)
