import json
import os
import time
import threading
from signal import signal, SIGINT

from .climate import ClimateSensor
from .display import Display
from .Thermostat import thermostat

from flask import Flask, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='thermostat-web/build')

CORS(app, support_credentils=True)

lock = threading.Lock()

climate_sensor = ClimateSensor()
def climate_loop():
    thermostat.target_temp = 78
    while True:
        climate = climate_sensor.get_climate()

        if climate is not None:
            with lock:
                thermostat.curr_temp = climate['temperature']

        time.sleep(5)

t = threading.Thread(target=climate_loop)
@app.before_first_request
def startup():
    t.daemon = True
    t.start()

@app.route('/climate', methods = ['GET'])
def climate_get():
    return thermostat.to_json()

@app.route('/climate', methods = ['POST'])
def climate_post():
    with lock:
        new_state = request.get_json()

        print(new_state)
        if 'targetTemp' in new_state:
            thermostat.target_temp = new_state['targetTemp']

        if 'thermostatMode' in new_state:
            thermostat.trigger(new_state['thermostatMode'])

        if 'fanMode' in new_state:
            thermostat.fan_mode = new_state['fanMode']

        print(thermostat.to_json())

    return thermostat.to_json()

@app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
def servce(path):
    if path != "" and os.path.exists(app.static_folder + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

