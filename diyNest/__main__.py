import json
import time
import threading

from .climate import ClimateSensor
from .display import Display
from .Thermostat import thermostat

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)

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
    t.start()

@app.route('/climate', methods = ['GET'])
def climate_get():
    return thermostat.to_json()

@app.route('/climate', methods = ['POST'])
def climate_post():
    with lock:
        new_state = request.get_json()

        if thermostat.target_temp != new_state['target_temp']:
            thermostat.target_temp = new_state['target_temp']

        if thermostat.state[:4] != new_state['thermostat_mode']:
            thermostat.trigger(new_state['thermostat_mode'])

        if thermostat.fan.state[:2] != new_state['fan_mode'][:2]:
            thermostat.fan_mode = new_state['fan_mode']

        print(new_state)
        print(thermostat.to_json())
    return thermostat.to_json()
