from transitions import Machine, State

import json

from .display import Display
from .Fan import fan

class Thermostat(object):
    def __init__(self, fan):
        self._curr_temp = 0
        self._target_temp = 0

        self.fan = fan
        self.fan.auto()

        self.display = Display()
        self.display.thermostat_mode = 'off'
        self.display.fan_mode = 'auto'

        self._temp_high = None

        self._temp_history = []
    
    def to_json(self):
        return json.dumps({
            'current_temp': str(self._curr_temp),
            'target_temp': str(self._target_temp),
            'temp_history': str(self._temp_history),
            'temp_high': str(self._temp_high),
            'thermostat_mode': str(self.state[:4]),
            'thermostat_state': str(self.state),
            'fan': self.fan.to_json()
        })

    def check_temp(self):
        if self._target_temp is not None and self._curr_temp is not None:
            if self._curr_temp > self._target_temp:
                self._temp_high = True
                self.temp_high()
            elif self._curr_temp < self._target_temp:
                self._temp_high = False
                self.temp_low()

    @property
    def fan_mode(self):
        return self.fan.state

    @fan_mode.setter
    def fan_mode(self, value):
        if value == 'auto':
            self.fan.trigger('auto')
            self.display.fan_mode = 'auto'
        elif value == 'on':
            self.fan.trigger('on')
            self.display.fan_mode = 'on'
        
    @property
    def target_temp(self):
        self._target_temp

    @target_temp.setter
    def target_temp(self, value):
        self._target_temp = int(round(float(value)))
        self.display.target_temp = str(self._target_temp)
        self.check_temp()

    @property
    def curr_temp(self):
        self._curr_temp

    @curr_temp.setter
    def curr_temp(self, value):
        self._temp_history.insert(0,int(round(float(value))))

        if len(self._temp_history) == 10:
            self._temp_history.pop()

        self._curr_temp = sum(self._temp_history) / len(self._temp_history)
        self._curr_temp = round(self._curr_temp)

        self.display.curr_temp = str(self._curr_temp)
        self.check_temp()

    def on_enter_off(self):
        self.display.thermostat_mode = 'off'

    def start_cool_mode(self):
        self.display.thermostat_mode = 'cool'

    def start_heat_mode(self):
        self.display.thermostat_mode = 'heat'

    def on_enter_heat_heater_on(self):
        self.fan.turn_fan_on()

    def on_exit_heat_heater_on(self):
        self.fan.turn_fan_off()

    def on_enter_cool_compressor_on(self):
        self.fan.turn_fan_on()

    def on_exit_cool_compressor_on(self):
        self.fan.turn_fan_off()

thermostat = Thermostat(fan)
thermostat_states = ['heat_heater_off','heat_heater_on','cool_compressor_off','cool_compressor_on', 'off']
thermostat_transitions = [
        #Off trigger
        { 'trigger': 'off', 'source': '*', 'dest': 'off'},
        { 'trigger': 'temp_low', 'source': 'off', 'dest': None},
        { 'trigger': 'temp_high', 'source': 'off', 'dest': None},

        #Heat triggers
        { 'trigger': 'heat', 'source': ['off', 'cool_compressor_off', 'cool_compressor_on'], 'dest': 'heat_heater_off', 'before': 'start_heat_mode'},
        { 'trigger': 'heat', 'source': ['heat_heater_off', 'heat_heater_on'], 'dest': None},
        #Heat temp low
        { 'trigger': 'temp_low', 'source': 'heat_heater_off', 'dest': 'heat_heater_on'},
        { 'trigger': 'temp_low', 'source': 'heat_heater_on', 'dest': None},
        #Heat temp high
        { 'trigger': 'temp_high', 'source': 'heat_heater_off', 'dest': None},
        { 'trigger': 'temp_high', 'source': 'heat_heater_on', 'dest': 'heat_heater_off'},

        #Cool triggers
        { 'trigger': 'cool', 'source': ['off', 'heat_heater_on', 'heat_heater_off'], 'dest': 'cool_compressor_off', 'before': 'start_cool_mode'},
        { 'trigger': 'cool', 'source': ['cool_compressor_off', 'cool_compressor_off'], 'dest': None},
        #Cool temp low
        { 'trigger': 'temp_low', 'source': 'cool_compressor_off', 'dest': None},
        { 'trigger': 'temp_low', 'source': 'cool_compressor_on', 'dest': 'cool_compressor_off'},
        #Cool temp high
        { 'trigger': 'temp_high', 'source': 'cool_compressor_off', 'dest': 'cool_compressor_on'},
        { 'trigger': 'temp_high', 'source': 'cool_compressor_on', 'dest': None}
]

thermostatMachine = Machine(model=thermostat,states=thermostat_states,transitions=thermostat_transitions,initial='off')
