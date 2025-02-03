# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Simulated data generator
def generate_random_data():
    while True:
        # Generate random sensor-like data
        temperature = round(random.uniform(20.0, 35.0), 2)
        humidity = round(random.uniform(30.0, 70.0), 2)
        power_consumption = round(random.uniform(100.0, 500.0), 2)
        
        # Emit data to all connected clients
        socketio.emit('sensor_update', {
            'temperature': temperature,
            'humidity': humidity,
            'power_consumption': power_consumption
        })
        
        # Wait for 2 seconds before next update
        time.sleep(2)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connection_response', {'message': 'Connected to real-time server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    # Start background thread for data generation
    data_thread = threading.Thread(target=generate_random_data)
    data_thread.daemon = True
    data_thread.start()
    
    # Run the Flask-SocketIO app
    socketio.run(app, debug=True)
