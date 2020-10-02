from flask import Flask
# import RPi.GPIO as GPIO
# multiprocessing is repeating a process so we are using semaphore Lock
import os

left_positive = 19
left_negitive = 26
right_positive = 5
right_negitive = 6

app = Flask(__name__)
# pi_host = '192.168.43.159'
pi_host = '127.0.0.1'
camera_port = 9092
motor_port = 9091

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(left_positive, GPIO.OUT)
# GPIO.setup(left_negitive, GPIO.OUT)
# GPIO.setup(right_positive, GPIO.OUT)
# GPIO.setup(right_negitive, GPIO.OUT)
#
# GPIO.output(left_positive, GPIO.LOW)
# GPIO.output(left_negitive, GPIO.LOW)
# GPIO.output(right_positive, GPIO.LOW)
# GPIO.output(right_negitive, GPIO.LOW)

@app.route('/forword')
def Forword():
    # GPIO.output(left_positive, GPIO.HIGH)
    # GPIO.output(left_negitive, GPIO.LOW)
    # GPIO.output(right_positive, GPIO.HIGH)
    # GPIO.output(right_negitive, GPIO.LOW)
    return "Forword"

@app.route('/reverse')
def Reverse():
    # GPIO.output(left_positive, GPIO.LOW)
    # GPIO.output(left_negitive, GPIO.HIGH)
    # GPIO.output(right_positive, GPIO.LOW)
    # GPIO.output(right_negitive, GPIO.HIGH)
    return "Reverse"

@app.route('/clockwise')
def Clockwise():
    # GPIO.output(left_positive, GPIO.HIGH)
    # GPIO.output(left_negitive, GPIO.LOW)
    # GPIO.output(right_positive, GPIO.LOW)
    # GPIO.output(right_negitive, GPIO.HIGH)
    return "Forword"

@app.route('/anticlockwise')
def Anticlockwise():
    # GPIO.output(left_positive, GPIO.LOW)
    # GPIO.output(left_negitive, GPIO.HIGH)
    # GPIO.output(right_positive, GPIO.HIGH)
    # GPIO.output(right_negitive, GPIO.LOW)
    return "Anticlockwise"

@app.route('/stop')
def stop():
    # GPIO.output(left_positive, GPIO.LOW)
    # GPIO.output(left_negitive, GPIO.LOW)
    # GPIO.output(right_positive, GPIO.LOW)
    # GPIO.output(right_negitive, GPIO.LOW)
    return "stop"

def car_handle():
    app.run(debug=True, port=motor_port, host=pi_host)


if __name__=="__main__":
    car_handle()
