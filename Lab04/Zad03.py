import socket

IP = "127.0.0.1"
PORT = 9402


def start_server():
    print("Starting server...")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((IP, PORT))

        while True:
            message, address = server.recvfrom(4096)
            print("Received: ", message.decode())

            server.sendto(message, address)


if __name__ == "__main__":
    start_server()