#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

colors = [0xFF00, 0x00FF]
pins = (11, 12)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pins, GPIO.OUT)
GPIO.output(pins, GPIO.LOW)

p_R = GPIO.PWM(pins[0], 2000)
p_G = GPIO.PWM(pins[1], 2000)

p_R.start(0)
p_G.start(0)

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setColor(col):
    R_val = col >> 8
    G_val = col & 0x00FF

    R_val = map(R_val, 0, 255, 0, 100)
    G_val = map(G_val, 0, 255, 0, 100)

    p_R.ChangeDutyCycle(R_val)
    p_G.ChangeDutyCycle(G_val)

def loop():
    while True:
        for col in colors:
            setColor(col)
            time.sleep(0.5)

def destroy():
    p_R.stop()
    p_G.stop()
    GPIO.output(pins, GPIO.LOW)
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
