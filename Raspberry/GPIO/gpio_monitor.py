import RPi.GPIO as GPIO
import time
import sys
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
print "monitor for GPIO: ", sys.argv[1]
input_monitor = int(sys.argv[1])
GPIO.setup(input_monitor, GPIO.IN, GPIO.PUD_UP)
monitor_status = GPIO.input(input_monitor)
print time.ctime(), monitor_status
while True:
	if GPIO.input(input_monitor) != monitor_status:
                monitor_status = GPIO.input(input_monitor)
		print time.ctime(), monitor_status
