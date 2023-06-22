import socket

CRLF = "\r\n"

HOST = "localhost"
PORT = 10000

ENDPOINT = "/.ws"

INITIAL_MESSAGE = "GET " + ENDPOINT + " HTTP/1.1" + \
    CRLF + "Host: " + HOST + \
    CRLF + "Upgrade: websocket" + \
    CRLF + "Connection: Upgrade" + \
    CRLF + "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" + \
    CRLF + "Sec-WebSocket-Protocol: chat" + \
    CRLF + "Sec-WebSocket-Version: 13" + \
    CRLF + CRLF

class WebsocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))
        print("Connected to " + self.host + ":" + str(self.port))

        self.socket.sendall(INITIAL_MESSAGE.encode())
        response = self.socket.recv(1024)
        print("Initial response: ", response, sep="\n")

    
if __name__ == "__main__":
    client = WebsocketClient(HOST, PORT)
    client.connect()