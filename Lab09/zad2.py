import socket

# HOST = "httpbin.org"
HOST = "127.0.0.1"
PORT = 80

HTTP_REQUEST = """GET /image/png HTTP/1.1\r\nHost: httpbin.org\r\nUser-Agent:Safari/7.0.3\r\nContent-Type: image/png\r\n\r\n"""

class Client:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


    def getContent(self, filename="image.png"):
        content = b""

        self.sock.sendall(HTTP_REQUEST.encode())
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            content = content + data
        self.sock.close()
        
        content = content.split(b"\r\n\r\n")[1]

        with open(filename, "wb") as f:
            f.write(content)

if __name__ == "__main__":
    client = Client()
    client.getContent()