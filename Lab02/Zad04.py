import socket

# Dla testów w lokalnym środowisku
SERVER_IP = "127.0.0.1"

# SERVER_IP = "212.182.24.27"
SERVER_PORT = 2901
MESSAGE_CONTENT = "Test Message Content Intended to Verify Server Functionality"


def connect_to_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sockIPv4:
        sockIPv4.connect((SERVER_IP, SERVER_PORT))
        sockIPv4.send(MESSAGE_CONTENT.encode("utf-8"))
        data = sockIPv4.recv(1024)
    print(data.decode("utf-8"))


if __name__ == "__main__":
    connect_to_server()