import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
board_output = 4
GPIO.setup(board_output, GPIO.OUT)
board_output_value = False
GPIO.output(board_output, board_output_value)
while True:
        GPIO.output(board_output, board_output_value)
        print "set board as", board_output_value
        board_output_value = not board_output_value
        time.sleep(5)
