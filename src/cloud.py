from socket import socket

class Server():
    def __init__(self, port=12345):
        self.PORT = port
        self.socket = socket()
        print("Socket created succesfully")
        self.socket.bind(('', self.PORT))
        print("Socket binded to {port}".format(port=self.PORT))
        self.socket.listen(5)
        print("Socket is listening")

    def establish_connection(self):
        conn, addr = self.socket.accept()
        print("Got connection from: {addr}".format(**locals()))

        return conn

    def receive_data(self, conn):
        data = conn.recv(1024)
        return data

    def run(self):
        conn = self.establish_connection()
        while True:
            data = self.receive_data(conn)
            print(data)

    def __del__(self):
        self.socket.close()

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
