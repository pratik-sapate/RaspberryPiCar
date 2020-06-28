import socket
import cv2
import io
import struct
import time
import pickle
import zlib


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
# host = socket.gethostname()
connection_file = serversocket.makefile('wb')
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
msg = 'Hi Client' + "\r\n"

while True:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame, 0)
    # print(data)
    size = len(data)
    # print("{}: {}".format(img_counter, size))
    clientsocket.sendall(struct.pack(">L", size) + data)
    # print(struct.pack(">L", size) + data)
    img_counter += 1
    # clientsocket.send(msg.encode('ascii'))

