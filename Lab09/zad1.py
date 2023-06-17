import socket

HOST = "httpbin.org"
PORT = 80

HTTP_REQUEST = """GET /html HTTP/1.1\r\nHost: httpbin.org\r\nUser-Agent:Safari/7.0.3\r\n\r\n"""

class Client:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


    def getContent(self, filename="index.html"):
        with open(filename, "wb") as f:
            self.sock.sendall(HTTP_REQUEST.encode())
            while True:
                data = self.sock.recv(1024)
                if not data:
                    break
                f.write(data)
        self.sock.close()

if __name__ == "__main__":
    client = Client()
    client.getContent("index.html")