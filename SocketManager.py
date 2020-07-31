# Socket Connection References using OpenCV
# https://answers.opencv.org/question/197414/sendreceive-vector-mat-over-socket-cc/
# https://walkinpcm.blogspot.com/2016/05/python-python-opencv-tcp-socket-image.html
# https://docs.opencv.org/3.4.0/d4/da8/group__imgcodecs.html#ga461f9ac09887e47797a54567df3b8b63

import socket
import Utils

args = Utils.get_parser()
logger = Utils.get_logger()

class Socket_Mananger:
    FLAGS_SERVER = 0
    FLAGS_CLIENT = 1
    cnt = 0
    IMG_LENGTH = 0

    def __init__(self, host, port, buff):
        self.host = host
        self.port = port
        self.buff = buff

    def create_server_socket(self):
        # socket.socket(family, type, proto)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if server_socket == -1:
            self.error_handling('Cannot create the server socket')
        # To solve for WinError 10048 while using port
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return server_socket

    def create_client_socket(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if client_socket == -1:
            self.error_handling('Cannot create the client socket')
        return client_socket

    def print_log_msg(self, log_msg):
        print(log_msg)

    def error_handling(self, err_msg):
        logger.error(err_msg)
        # print('ERR : ', err_msg)
        exit(1)

    def recv_img(self, client_socket):
        buf = b''
        while self.buff != 0:
            self.cnt += 1
            print(self.cnt)
            data = client_socket.recv(self.buff)
            buf += data
            self.buff -= len(data)

        return buf

    def processing(self, flags = FLAGS_SERVER):
        if flags == self.FLAGS_SERVER:
            # Server
            server_socket = self.create_server_socket()

            # socket.bind((hostname, port))
            # hostname : "", "your-hostname", "your-ip-addr"
            # port : 1 ~ 65535
            server_socket.bind((self.host, self.port))
            # Listen
            server_socket.listen()
            print("Waiting for a client.")

            # Accept
            client_socket, client_socket_addr = server_socket.accept()
            self.print_log_msg(client_socket_addr)
            print(client_socket_addr)

            while True:
                data = client_socket.recv(self.buff)
                if not data:
                    break
                 
                data_decode = data.decode()
                print(data_decode)
                client_socket.send("{0}".format(data_decode).encode())

            # Close
            logger.info('SYSTEM OFF')
            server_socket.close()
            client_socket.close()
            exit(1)

        elif flags == self.FLAGS_CLIENT:
            # Client
            client_socket = self.create_client_socket()
            # Connection with specified information
            client_socket.connect((self.host, self.port))
            if client_socket == -1:
                self.error_handling('Cannot connet the server')

            while True:
                # Send msg
                client_socket.sendall('Hello\n'.encode())

                # Recv
                data = client_socket.recv(1024)
                print('Received', repr(data.decode()))

            # Close
            client_socket.close()

if __name__ == '__main__':
    sManager = Socket_Mananger(args.host, args.port, args.buff)
    sManager.processing(flags=sManager.FLAGS_SERVER)
