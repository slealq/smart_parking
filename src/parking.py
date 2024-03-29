from sensors import DistanceSensor
from actuators import Led
from cloud import Client
import time
from json import dumps

class ParkingSpace():
    def __init__(self,
                 name: str = None,
                 rl_pin: int = None,
                 gl_pin: int = None,
                 echo: int = None,
                 trig: int = None,
                 down_dist: float = 10.0,
                 up_dist: float = 12.0):

        self.name = name
        self.rl_pin = rl_pin
        self.gl_pin = gl_pin
        self.echo = echo
        self.trig = trig

        self.down_dist = down_dist
        self.up_dist = up_dist

        # Instanciate sensors and actuators
        self.green_led = Led(gl_pin)
        self.red_led = Led(rl_pin)
        self.distance_sensor = DistanceSensor(trig, echo)

        self._state = 'SLEEP'

    def state(self):
        current_dist = self.distance_sensor.distance()

        if current_dist > self.up_dist:
            self._state = 'EMPTY'
        elif current_dist < self.down_dist:
            self._state = 'OCCUPIED'
        else:
            self._state = self._state

        return self._state

    def update_sign(self):
        if self._state == 'EMPTY':
            self.green_led.on()
            self.red_led.off()
        elif self._state == 'OCCUPIED':
            self.green_led.off()
            self.red_led.on()
        else:
            self.green_led.off()
            self.red_led.off()

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(repr(self))

    def __del__(self):
        del self.green_led
        del self.red_led
        del self.distance_sensor


class ParkingLot():
    def __init__(self):
        # ParkingLot code
        self.CODE = 'A'
        self.SPACES = 2 # Total spaces available in this parking lot

        # Cycle period
        self.parking_spaces = 2
        self.sleep_time = 0.2 / self.parking_spaces

        # LEFT SIDE PINS
        self.LR_LED = 23
        self.LG_LED = 21
        self.L_ECHO = 8
        self.L_TRIG = 10

        # RIGHT SIDE PINS
        self.RR_LED = 11
        self.RG_LED = 13
        self.R_ECHO = 7
        self.R_TRIG = 22

        # New client
        self.cloud_client = Client()

        # Define parkings
        self.left_parking = ParkingSpace(name='Left',
                                         rl_pin=self.LR_LED,
                                         gl_pin=self.LG_LED,
                                         echo=self.L_ECHO,
                                         trig=self.L_TRIG)

        self.right_parking = ParkingSpace(name='Right',
                                          rl_pin=self.RR_LED,
                                          gl_pin=self.RG_LED,
                                          echo=self.R_ECHO,
                                          trig=self.R_TRIG)

        # All parkings state
        self.all_parking_spaces = {self.left_parking: 'EMPTY',
                                   self.right_parking: 'EMPTY'}

        # Parking Lot available
        self.available_spaces = self.SPACES

    def send_state_change(self):
        empty_spaces = 0

        for parking, state in self.all_parking_spaces.items():
            if state == 'EMPTY':
                empty_spaces += 1

        state_change_json = {
            'parking_code': self.CODE,
            'current_available_spaces': empty_spaces,
            'usage': (self.SPACES - empty_spaces) * 100.0 / self.SPACES
        }

        state_change_json_repr = dumps(state_change_json)

        self.cloud_client.send_data(state_change_json_repr)
        self.available_spaces = empty_spaces

    def check_state_change(self):
        parking_spaces = list(self.all_parking_spaces.keys())
        for parking in parking_spaces:
            past_state = self.all_parking_spaces[parking]
            current_state = parking.state()

            if past_state != current_state:
                self.all_parking_spaces[parking] = current_state
                self.send_state_change()

    def run(self):
        while True:
            for parking in self.all_parking_spaces:
                time.sleep(self.sleep_time)
                print("{0} parking state: {1}"
                      "".format(parking.name, parking.state()))
                parking.update_sign()

            self.check_state_change()

    def __del__(self):
        for parking in self.all_parking_spaces:
            del parking


__all__ = ['ParkingSpace', 'ParkingLot']
