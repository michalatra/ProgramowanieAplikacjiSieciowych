import socket
from threading import Thread
import sys
import os

HOST = "localhost"
PORT = 2556

class WebsocketThread(Thread):
    def __init__(self, socket: socket.socket):
        super().__init__()
        self.socket = socket

    def run(self):
        print("WebsocketThread started")
        message = self.socket.recv(1024)
        print("Received message: ", message, sep="\n")
        endpoint = self.interpret_initial_message(message)
        response = "HTTP/1.1 101 Switching Protocols\r\n" + \
            "Upgrade: websocket\r\n" + \
            "Connection: Upgrade\r\n" + \
            "Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=\r\n" + \
            "Sec-WebSocket-Protocol: chat\r\n" + \
            "\r\n"
        self.socket.sendall(response.encode())
        print("Sent response: ", response, sep="\n")

        self.handle_websocket_connection()

        print("WebsocketThread ended")
    
    def interpret_initial_message(self, message):
        message = message.decode()
        lines = message.split("\r\n")
        print(lines)
        endpoint = lines[0].split(" ")[1]
        print(endpoint)
        return endpoint
    
    def handle_websocket_connection(self):
        while True:
            message = self.socket.recv(1024)
            print("Received message: ", message, sep="\n")
            if message == b"close":
                break
            else:
                fin, opcode, mask, payload_length, mask_key, payload = self.interpret_websocket_frame(message)
                responseMessage = self.prepare_websocket_response_frame(fin, opcode, mask, payload_length, mask_key, payload)
                self.socket.sendall(responseMessage)
                print("Sent message: ", responseMessage, sep="\n")
        
    def interpret_websocket_frame(self, message):
        fin = message[0] & 0b10000000
        opcode = message[0] & 0b00001111
        mask = message[1] & 0b10000000
        payload_length = message[1] & 0b01111111
        if payload_length == 126:
            payload_length = int.from_bytes(message[2:4], byteorder="big")
            mask_key = message[4:8]
            payload = message[8:]
        elif payload_length == 127:
            payload_length = int.from_bytes(message[2:10], byteorder="big")
            mask_key = message[10:14]
            payload = message[14:]
        else:
            mask_key = message[2:6]
            payload = message[6:]
        
        print("Decoded message: ", fin, opcode, mask, payload_length, mask_key, payload, sep="\n")
        return fin, opcode, mask, payload_length, mask_key, payload
    
    def prepare_websocket_response_frame(self, fin, opcode, mask, payload_length, mask_key, payload):
        message = bytearray()
        message.append(fin | opcode)
        message.append(mask | payload_length)
        message.extend(mask_key)
        message.extend(payload)
        return message



class WebsocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.socket.bind((self.host, self.port))
        print("Bound to " + self.host + ":" + str(self.port))

        self.socket.listen()
        print("Listening...")

        while True:
            client_socket, client_address = self.socket.accept()
            print("Accepted connection from " + str(client_address))
            thread = WebsocketThread(client_socket)
            thread.start()

if __name__ == "__main__":
    port = PORT
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    server = WebsocketServer(HOST, port)
    server.start()


