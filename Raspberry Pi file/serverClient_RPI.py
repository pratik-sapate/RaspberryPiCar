from flask import Flask
# import RPi.GPIO as GPIO
import socket
import cv2
import pickle
import struct
from multiprocessing import Process, Lock
from threading import Thread
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
motor_port = 9090

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
    # time.sleep(2)
    # GPIO.output(left_positive, GPIO.LOW)
    # GPIO.output(left_negitive, GPIO.LOW)
    # GPIO.output(right_positive, GPIO.LOW)
    # GPIO.output(right_negitive, GPIO.LOW)
    return "Forword"

@app.route('/reverse')
def Reverse():
    # GPIO.output(left_positive, GPIO.LOW)
    # GPIO.output(left_negitive, GPIO.HIGH)
    # GPIO.output(right_positive, GPIO.LOW)
    # GPIO.output(right_negitive, GPIO.HIGH)
    # time.sleep(2)
    # GPIO.output(left_positive, GPIO.LOW)
    # GPIO.output(left_negitive, GPIO.LOW)
    # GPIO.output(right_positive, GPIO.LOW)
    # GPIO.output(right_negitive, GPIO.LOW)
    return "Reverse"

@app.route('/clockwise')
def Clockwise():
    # GPIO.output(left_positive, GPIO.HIGH)
    # GPIO.output(left_negitive, GPIO.LOW)
    # GPIO.output(right_positive, GPIO.LOW)
    # GPIO.output(right_negitive, GPIO.HIGH)
    # time.sleep(2)
    # GPIO.output(left_positive, GPIO.LOW)
    # GPIO.output(left_negitive, GPIO.LOW)
    # GPIO.output(right_positive, GPIO.LOW)
    # GPIO.output(right_negitive, GPIO.LOW)
    return "Forword"

@app.route('/anticlockwise')
def Anticlockwise():
    # GPIO.output(left_positive, GPIO.LOW)
    # GPIO.output(left_negitive, GPIO.HIGH)
    # GPIO.output(right_positive, GPIO.HIGH)
    # GPIO.output(right_negitive, GPIO.LOW)
    # time.sleep(2)
    # GPIO.output(left_positive, GPIO.LOW)
    # GPIO.output(left_negitive, GPIO.LOW)
    # GPIO.output(right_positive, GPIO.LOW)
    # GPIO.output(right_negitive, GPIO.LOW)
    return "Anticlockwise"

def camera_server():
    try:
        print("camera_server")
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # host = socket.gethostname()
        connection_file = serversocket.makefile('wb')
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        print(pi_host, camera_port)
        serversocket.bind((pi_host, camera_port))
        serversocket.listen(5)
        clientsocket, addr = serversocket.accept()
        print("Got a connection from %s" % str(addr))

        # obj = objectDetect()
        cam = cv2.VideoCapture(0)
        cam.set(3, 640);
        cam.set(4, 480);
        img_counter = 0

        while True:
            ret, frame = cam.read()
            # frame = obj.detect_object_from_image(frame)
            result, frame = cv2.imencode('.jpg', frame, encode_param)
            data = pickle.dumps(frame, 0)
            # print(data)
            size = len(data)
            # print("{}: {}".format(img_counter, size))
            clientsocket.sendall(struct.pack(">L", size) + data)
            # print(struct.pack(">L", size) + data)
            img_counter += 1
            # clientsocket.send(msg.encode('ascii'))
    except:
        print("problem occored")
        # lock.release()
        # Process(target=camera_server).start()


def car_handle():
    app.run(debug=True, port=motor_port, host=pi_host)


if __name__=="__main__":
    # Thread(target=car_handle).start()
    # car_handle()
    pro1 = Process(target=camera_server)
    pro2 = Process(target=car_handle)

    pro2.start()
    pro1.start()
    pro1.join()
    pro2.join()


