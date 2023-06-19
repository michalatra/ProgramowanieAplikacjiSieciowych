import socket

HOST = "127.0.0.1"
PORT = 9802


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((HOST, PORT))
        server.settimeout(10)
        print("Server is listening on port {}".format(PORT))

        while True:
            try:
                data, address = server.recvfrom(1024)
                print("Received: {}".format(data.decode()))
            except socket.timeout:
                print("Server timed out")


if __name__ == "__main__":
    start_server()