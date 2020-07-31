# Socket Connection References using OpenCV
# https://answers.opencv.org/question/197414/sendreceive-vector-mat-over-socket-cc/
# https://walkinpcm.blogspot.com/2016/05/python-python-opencv-tcp-socket-image.html
# https://docs.opencv.org/3.4.0/d4/da8/group__imgcodecs.html#ga461f9ac09887e47797a54567df3b8b63

import socket
import Utils
import sys
import numpy as np
import DesignManager
# from Design import DesignManager as DesignManager

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

    def create_serverUI(self, client_socket):
        self.dManager = DesignManager.MainWindow(client_socket, self.buff)
        self.app = DesignManager.app

    def create_server_socket(self):
        # 소켓 객체를 생성합니다.
        # 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if server_socket == -1:
            self.error_handling('Cannot create the server socket')
        # 포트 사용중이라 연결할 수 없다는 WinError 10048 에러 해결를 위해 필요합니다.
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
            # bind 함수는 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용됩니다.
            # HOST는 hostname, ip address, 빈 문자열 ""이 될 수 있습니다.
            # 빈 문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용합니다.
            # PORT는 1-65535 사이의 숫자를 사용할 수 있습니다.
            server_socket.bind((self.host, self.port))
            # 서버가 클라이언트의 접속을 허용하도록 합니다.
            server_socket.listen()
            print("Waiting for a client.")
            # accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴합니다.
            client_socket, client_socket_addr = server_socket.accept()
            self.print_log_msg(client_socket_addr)

            self.create_serverUI(client_socket)
            print(client_socket_addr)
            # self.dManager.textBrowser.append("{0} -p {1}".format(client_socket_addr[0], str(client_socket_addr[1])))
            self.app.exec_() # 무한루프

            # while True:
            #     data = client_socket.recv(self.buff)
            #     print(data)
            #     print(len(data))
            #     data_decode = data.decode()
            #
            #     if "IMG" in data_decode:
            #         self.IMG = True
            #         buff_tmp = self.buff
            #         self.buff = int(data_decode.lstrip('IMG:').rstrip('\0'))
            #         print(self.buff)
            #
            #         img = self.recv_img(client_socket)
            #
            #         if self.buff == len(img):
            #             self.error_handling("LOAD IMG")
            #
            #         self.buff = buff_tmp
            #
            #     else:
            #         print(data)
            #         data_decode = data_decode.split('\0')
            #         data_decode.pop()
            #         [print(d) for d in data_decode]
            #         break

            # 소켓을 닫습니다.
            logger.info('SYSTEM OFF')
            server_socket.close()
            client_socket.close()
            exit(1)

        elif flags == self.FLAGS_CLIENT:
            # Client
            client_socket = self.create_client_socket()
            # 지정한 HOST와 PORT를 사용하여 서버에 접속합니다.
            client_socket.connect((self.host, self.port))
            if client_socket == -1:
                self.error_handling('Cannot connet the server')

            cnt = 0
            while True:
                # 메시지를 전송합니다.
                client_socket.sendall('안녕{0}\n'.format(cnt).encode())

                # 메시지를 수신합니다.
                # data = client_socket.recv(1024)
                # print('Received', repr(data.decode()))

                if cnt == 10:
                    break
                cnt += 1

            # 소켓을 닫습니다.
            client_socket.close()

if __name__ == '__main__':
    sManager = Socket_Mananger(args.host, args.port, args.buff)
    sManager.processing(flags=sManager.FLAGS_SERVER)