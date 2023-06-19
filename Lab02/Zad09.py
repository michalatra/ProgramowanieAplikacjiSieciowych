import sys
import socket


# Dla testów w lokalnym środowisku
SERVER_IP = "127.0.0.1"

# SERVER_IP = "212.182.24.27"
SERVER_PORT = 2906

IP_TO_VALIDATE = "142.250.189.174"


def connect_to_server(ip_to_validate: str):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sockIPv4:
        sockIPv4.connect((SERVER_IP, SERVER_PORT))
        sockIPv4.send(ip_to_validate.encode("utf-8"))
        data = sockIPv4.recv(1024)
        print(data.decode("utf-8"))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        connect_to_server(sys.argv[1])
    else:
        connect_to_server(IP_TO_VALIDATE)