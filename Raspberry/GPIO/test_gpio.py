import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
input_1 = 15
output_1 = 4
GPIO.setup(input_1, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(output_1, GPIO.OUT)
input_status = GPIO.input(input_1)
output_status = False
count = 0
while True:
	if GPIO.input(input_1) != input_status:
                input_status = GPIO.input(input_1)
		print(input_status)
	if count % 20 == 0:
                GPIO.output(output_1, output_status)
                output_status = not output_status
        time.sleep(0.5)
