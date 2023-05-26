import socket

CRLF = "\r\n"

HOST = "localhost"
PORT = 10000

class WebsocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connect(self):
        self.socket.connect((self.host, self.port))
        print("Connected to " + self.host + ":" + str(self.port))

        initial_message = self.generate_initial_message().encode()

        self.socket.sendall(initial_message)
        response = self.receive()
        print("Response: ", response)


    def send_frame(self, message: str):
        frame = bytearray()
        frame.append(int("10000100", 2))
        
        payload = message.encode()
        payload_length = len(payload)

        if payload_length < 125:
            frame.append(payload_length)
        elif payload_length < 65536:
            frame.append(126)
            frame.append(payload_length)
        else:
            frame.append(127)
            frame.append(payload_length)
        
        frame.extend(payload)

        # print("Frame: ", frame)

        self.socket.sendall(frame)
        response = self.socket.recv(1024)
        print("Response: ", response)

    def generate_initial_message(self) -> str:
        return "GET /chat HTTP/1.1" \
            + CRLF + "Host: " + self.host  \
            + CRLF + "Upgrade: websocket" \
            + CRLF + "Connection: Upgrade" \
            + CRLF + "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
            + CRLF + "Sec-WebSocket-Version: 13" \
            + CRLF + CRLF



    def send(self, message):
        self.socket.send(message.encode())


    def handle_initial_response(self) -> str:
        return self.socket.recv(1024).decode()


    def close(self):
        self.socket.close()


    
if __name__ == "__main__":
    client = WebsocketClient(HOST, PORT)
    client.connect()
    client.send_frame("Test mesage")
    client.close()