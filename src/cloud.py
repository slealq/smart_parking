from socket import *
from json import loads

class Server():
    usage = None

    def __init__(self, conn=None, port=12345):
        self.PORT = port
        self.socket = socket()
        self.data = ""
        self.conn = conn
        print("Socket created succesfully")
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind(('', self.PORT))
        print("Socket binded to {port}".format(port=self.PORT))
        self.socket.listen(5)
        print("Socket is listening")

    def establish_connection(self):
        conn, addr = self.socket.accept()
        print("Got connection from: {addr}".format(**locals()))

        return conn

    def update_usage(self):
        if self.data:
            self.usage = loads(self.data)['usage']

        # send the usage through a pipe
        self.conn.send(self.usage)

    def receive_data(self, conn):
        data = conn.recv(1024)
        return data

    def run(self):
        conn = self.establish_connection()
        while True:
            self.data = self.receive_data(conn)
            print(self.data)
            self.update_usage()
            print("New usage: {0}".format(self.usage))

    def __del__(self):
        self.socket.close()
        self.conn.close()

class Client():
    def __init__(self, port=12345, target_host='192.168.0.2'):
        self.PORT = port
        self.TARGET_HOST = target_host
        self.socket = socket()
        self.socket.connect((self.TARGET_HOST, self.PORT))

    def test_data(self):
        self.socket.send(bytes('This is a test', 'utf-8'))

    def send_data(self, data: str):
        self.socket.send(bytes(data, 'utf-8'))

    def __del__(self):
        self.socket.close()
