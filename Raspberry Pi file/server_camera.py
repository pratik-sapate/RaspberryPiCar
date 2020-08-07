import socket
import cv2
import struct
import pickle
from threading import Thread


def camrera():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host = '192.168.43.159'
    host = '127.0.0.1'
    cam = cv2.VideoCapture(0)
    cam.set(3, 640);
    cam.set(4, 480);
    img_counter = 0

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    port = 9092

    print(host, port)
    serversocket.bind((host, port))
    serversocket.listen(5)
    clientsocket, addr = serversocket.accept()
    print("Got a connection from %s" % str(addr))

    while True:
        ret, frame = cam.read()
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(frame, 0)
        size = len(data)
        clientsocket.sendall(struct.pack(">L", size) + data)
        img_counter += 1

if __name__=="__main__":
    Thread(target=camrera).start()
    import os
    os.system('cmd /c "python serverClient_RPI.py"')
