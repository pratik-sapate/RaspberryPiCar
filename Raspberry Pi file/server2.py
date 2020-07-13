'''
from flask import Flask
import RPi.GPIO as GPIO
import time

left_positive = 19
left_negitive = 26
right_positive = 5
right_negitive = 6

GPIO.setmode(GPIO.BCM)

GPIO.setup(left_positive, GPIO.OUT)
GPIO.setup(left_negitive, GPIO.OUT)
GPIO.setup(right_positive, GPIO.OUT)
GPIO.setup(right_negitive, GPIO.OUT)

GPIO.output(left_positive, GPIO.LOW)
GPIO.output(left_negitive, GPIO.LOW)
GPIO.output(right_positive, GPIO.LOW)
GPIO.output(right_negitive, GPIO.LOW)

app = Flask(__name__)

@app.route('/forword')
def Forword():
    GPIO.output(left_positive, GPIO.HIGH)
    GPIO.output(left_negitive, GPIO.LOW)
    GPIO.output(right_positive, GPIO.HIGH)
    GPIO.output(right_negitive, GPIO.LOW)
    time.sleep(2)
    GPIO.output(left_positive, GPIO.LOW)
    GPIO.output(left_negitive, GPIO.LOW)
    GPIO.output(right_positive, GPIO.LOW)
    GPIO.output(right_negitive, GPIO.LOW)
    return "Forword"

@app.route('/reverse')
def Reverse():
    GPIO.output(left_positive, GPIO.LOW)
    GPIO.output(left_negitive, GPIO.HIGH)
    GPIO.output(right_positive, GPIO.LOW)
    GPIO.output(right_negitive, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(left_positive, GPIO.LOW)
    GPIO.output(left_negitive, GPIO.LOW)
    GPIO.output(right_positive, GPIO.LOW)
    GPIO.output(right_negitive, GPIO.LOW)
    return "Reverse"

@app.route('/clockwise')
def Clockwise():
    GPIO.output(left_positive, GPIO.HIGH)
    GPIO.output(left_negitive, GPIO.LOW)
    GPIO.output(right_positive, GPIO.LOW)
    GPIO.output(right_negitive, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(left_positive, GPIO.LOW)
    GPIO.output(left_negitive, GPIO.LOW)
    GPIO.output(right_positive, GPIO.LOW)
    GPIO.output(right_negitive, GPIO.LOW)
    return "Forword"

@app.route('/anticlockwise')
def Anticlockwise():
    GPIO.output(left_positive, GPIO.LOW)
    GPIO.output(left_negitive, GPIO.HIGH)
    GPIO.output(right_positive, GPIO.HIGH)
    GPIO.output(right_negitive, GPIO.LOW)
    time.sleep(2)
    GPIO.output(left_positive, GPIO.LOW)
    GPIO.output(left_negitive, GPIO.LOW)
    GPIO.output(right_positive, GPIO.LOW)
    GPIO.output(right_negitive, GPIO.LOW)
    return "Anticlockwise"

if __name__ == "__main__":
        app.run(debug=True, port=9090, host='192.168.43.159') '''