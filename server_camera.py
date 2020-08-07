import socket
import cv2
import struct
import pickle


from ObjectDetectionWebcam import objectDetect


class server(object):
    # self.host = '192.168.43.159'
    host = '127.0.0.1'
    port_video = 9092
    # port_car_control = 9091
    # car_signal =
    @staticmethod
    def videoCameraCamera(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((self.host, self.port_video))
        self.serversocket.listen(5)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        print("video sever started at port : ", self.host, self.port_video)
        self.clientsocket, self.addr = self.serversocket.accept()
        print("Got a connection from %s for camera" % str(self.addr))
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
            self.clientsocket.sendall(struct.pack(">L", size) + data)
            # print(struct.pack(">L", size) + data)
            img_counter += 1
            # clientsocket.send(msg.encode('ascii'))


if __name__ == '__main__':
    obj = server()
    obj.videoCameraCamera()


