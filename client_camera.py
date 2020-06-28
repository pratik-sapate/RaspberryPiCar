import socket
import cv2
import pickle
import struct ## new


class ControlRaspberryPiCamera:
    def controlCamera(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "127.0.0.1"
        # host = '192.168.43.159'
        port = 9092
        serversocket.connect((host, port))
        data = b""
        payload_size = struct.calcsize(">L")
        print('payload_size: ', payload_size)
        while True:
            while len(data) < payload_size:
                print("Recv: {}".format(len(data)))
                data += serversocket.recv(4096)

            print("Done Recv: {}".format(len(data)))
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            print("msg_size: {}".format(msg_size))

            while len(data) < msg_size:
                data += serversocket.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow('ImageWindow', frame)
            cv2.waitKey(1)
            # msg = serversocket.recv(1024)
            # print(msg.decode('ascii'))


if __name__ == "__main__":
    obj = ControlRaspberryPiCamera()
    obj.controlCamera()