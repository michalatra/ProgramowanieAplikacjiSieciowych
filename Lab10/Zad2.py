import socket
import os

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

    def send_message(self, message):
        frame = self.generate_websocket_frame(message)
        self.socket.sendall(frame)
        print("Sent message: ", frame, sep="\n")
        response = self.socket.recv(1024)
        print("Response: ", response, sep="\n")

    def generate_websocket_frame(self, message) -> bytes:
        message_bytes = message.encode()
        message_length = len(message)
        masking_key = os.urandom(4)

        print("Message length: ", message_length)

        frame = bytearray()

        frame.append(int('10000001', 2))
        if message_length <= 125:
            frame.extend((message_length + 128).to_bytes(1, byteorder="big"))
        elif message_length <= 65535:
            frame.extend(int(128 + 126).to_bytes(1, byteorder="big"))
            frame.extend(message_length.to_bytes(2, byteorder="big"))
        else:
            frame.extend(int(128 + 127).to_bytes(1, byteorder="big"))
            frame.extend(message_length.to_bytes(8, byteorder="big"))

        frame.extend(masking_key)

        for i in range(message_length):
            frame.append(message_bytes[i] ^ masking_key[i % 4])

        return frame


    
if __name__ == "__main__":
    client = WebsocketClient(HOST, PORT)
    client.connect()
    client.send_message("Hello world!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    client.send_message("Long lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec auctor, nisl eget ultricies aliquam, nunc nisl aliquet nunc, sit amet aliquam nisl nunc eu nisl. Sed euismod, nisl eget ultricies aliquam, nunc nisl aliquet nunc, sit amet aliquam nisl nunc eu nisl. Sed euismod, nisl eget ultricies aliquam, nunc nisl aliquet nunc, sit amet aliquam nisl nunc eu nisl. Sed euismod, nisl eget ultricies aliquam, nunc nisl aliquet nunc, sit amet aliquam nisl nunc eu nisl. Sed euismod, nisl eget ultricies aliquam, nunc nisl aliquet nunc, sit amet aliquam nisl nunc eu nisl. Sed euismod, nisl eget ultricies aliquam, nunc nisl aliquet nunc, sit amet aliquam nisl nunc eu nisl. Sed euismod, nisl eget ultricies aliquam, nunc nisl aliquet nunc, sit amet aliquam nisl nunc eu nisl. Sed euismod, nisl eget ultricies aliquam, nunc nisl aliquet nunc, sit amet aliquam nisl nunc eu nisl.")