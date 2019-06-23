import RPi.GPIO as GPIO
import time

class DistanceSensor():
    def __init__(sefl, trig_pin, echo_pin):
        SETTLE_WAIT = 2

        assert isinstance(trig_pin, int), "Please provide trig pin"
        assert isinstance(echo_pin, int), "Please provide echo pin"
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

        # Setup the pins
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.output(self.trig_pin, GPIO.LOW)

        # Wait sensor to settle
        time.sleep(SETTLE_WAIT)

    def distance():
        BETWEEN_TRIG = 0.00001

        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(BETWEEN_TRIG)
        GPIO.output(self.trig_pin, GPIO.LOW)

        while GPIO.input(self.echo_pin)==0:
            pulse_start_time = time.time()
        while GPIO.input(self.echo_pin)==1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        self.distance = round(pulse_duration * 17150, 2)

        return self.distance

    def __del__(self):
        GPIO.cleanup()
