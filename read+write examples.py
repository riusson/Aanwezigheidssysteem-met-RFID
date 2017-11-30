
#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522_monitor

def selectReader(reader):
    if reader == 1:
        spi.openSPI(device='/dev/spidev0.0',speed=1000000)
    elif reader == 2:
        spi.openSPI(device='/dev/spidev0.1',speed=1000000)

readerInstance = SimpleMFRC522_monitor.SimpleMFRC522_monitor()
selectReader(1) #change to 2 for scanning 2nd reader
try:
        ##reading tag
        id, text = reader.read()
        print(id)
        print(text)
        ##writing tag
        text = raw_input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
finally:
        GPIO.cleanup()
