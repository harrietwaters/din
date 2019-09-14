import json
from RPi import GPIO
from transitions import Machine, State
from .display import Display

class Fan(object):
    def __init__(self): 
        self.fan_on = False
        self.fan_pin = None

    def to_json(self):
        return json.dumps({
            'fan_mode': str(self.state),
            'fan_on': str(self.fan_on)
        })

    def start_fan(self):
        self.fan_on = True
        GPIO.output(self.fan_pin, GPIO.LOW)

    
    def stop_fan(self):
        self.fan_on = False
        GPIO.output(self.fan_pin, GPIO.HIGH)
    
    def on_enter_on(self):
        self.start_fan()

    def on_fan_on(self):
        if not self.fan_on:
            self.stop_fan()

fan_states = ['auto', 'on']
fan_transitions = [
        { 'trigger': 'auto', 'source': '*', 'dest': 'auto', 'before':'stop_fan'},
        { 'trigger': 'on', 'source': '*', 'dest': 'on'},
        { 'trigger': 'turn_fan_on', 'source': 'auto', 'dest': 'auto', 'before':'start_fan'},
        { 'trigger': 'turn_fan_off', 'source': 'auto', 'dest': 'auto', 'before':'stop_fan'},
        { 'trigger': 'turn_fan_on', 'source': 'on', 'dest': None},
        { 'trigger': 'turn_fan_off', 'source': 'on', 'dest': None}
]

fan = Fan()
fanMachine = Machine(model=fan,states=fan_states,transitions=fan_transitions,initial='auto_mode')