
#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522

def selectReader(reader):
    if reader == 1:
        spi.openSPI(device='/dev/spidev0.0',speed=1000000)
    elif reader == 2:
        spi.openSPI(device='/dev/spidev0.1',speed=1000000)

reader = SimpleMFRC522.SimpleMFRC522()
selectReader(1)
try:
        text = raw_input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
finally:
        GPIO.cleanup()
