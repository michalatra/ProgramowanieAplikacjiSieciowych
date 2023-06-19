import socket
from threading import Thread
import sys

HOST = "127.0.0.1"
PORT = 8080

class ClientThread(Thread):
    def __init__(self, conn: socket, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def __del__(self):
        self.conn.close()

    def handleHttpRequest(self, data: bytes) -> bytes:
        data = data.decode()
        print("Recieved: ", data)
        return b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Hello World</h1></body></html>"


    def run(self):
        print("New client thread started for ", self.addr)
        try:
            request = b""
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                request = request + data
            response = self.handleHttpRequest(request)
            self.conn.send(response)
            self.conn.close()

        except Exception as e:
            self.conn.close()

class HttpServer:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))

    def start(self):
        print("Server started")
        print("Listening on port", self.port)
        while True:
            self.sock.listen(5)
            conn, addr = self.sock.accept()
            print("New connection from", addr)
            ClientThread(conn, addr).start()

if __name__ == "__main__":
    port = PORT
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    server = HttpServer(port=port)
    server.start()