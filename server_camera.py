import socket
import cv2
import struct
import pickle
from ObjectDetectionWebcam import objectDetect

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 9092
# host = socket.gethostname()
connection_file = serversocket.makefile('wb')
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
print(host, port)
serversocket.bind((host, port))
serversocket.listen(5)
clientsocket, addr = serversocket.accept()
print("Got a connection from %s" % str(addr))

obj = objectDetect()
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
img_counter = 0

while True:
    ret, frame = cam.read()
    frame = obj.detect_object_from_image(frame)
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame, 0)
    # print(data)
    size = len(data)
    # print("{}: {}".format(img_counter, size))
    clientsocket.sendall(struct.pack(">L", size) + data)
    # print(struct.pack(">L", size) + data)
    img_counter += 1
    # clientsocket.send(msg.encode('ascii'))

