from sensors import DistanceSensor
from actuators import Led
import time


class ParkingSpace():
    def __init__(self,
                 name = None: str
                 rl_pin = None:int,
                 gl_pin = None: int,
                 echo = None: int,
                 trig = None: int,
                 down_dist = 6: int,
                 up_dist = 8: int):

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

    def update_sign():
        if self._state = 'EMPTY':
            self.green_led.on()
            self.red_led.off()
        elif self.state = 'OCCUPIED':
            self.green_led.off()
            self.red_led.on()
        else:
            self.green_led.off()
            self.red_led.off()

    def __del__(self):
        del self.green_led
        del self.red_led
        del self.distance_sensor


class ParkingLot():
    def __init__(self):
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

        self.left_parking = ParkingSpace(name='left',
                                         rl_pin=self.LR_LED,
                                         gl_pin=self.LG_LED,
                                         echo=self.L_ECHO,
                                         trig=self.L_TRIG)

    def run(self):
        while True:
            time.sleep(0.2)
            print("Left parking state: {1}"
                  "".format(self.left_parking.state()))

            self.left_parking.update_sign()

    def __del__(self):
        del self.left_parking


__all__ = ['ParkingSpace', 'ParkingLot']
