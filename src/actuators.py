import RPi.GPIO as GPIO

class Led():
    def __init__(self, board_pin):
        assert board_pin, "Please provide a board pin"
        self.board_pin = board_pin

        # Setup the pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.board_pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.board_pin, True)

    def off(self):
        GPIO.output(self.board_pin, False)

    def __del__(self):
        GPIO.cleanup()
