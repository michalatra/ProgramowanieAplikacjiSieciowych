import socket

SERVER_IP = "ntp.task.gda.pl"
SERVER_PORT = 13

def connect_to_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockIPv4:
        sockIPv4.connect((SERVER_IP, SERVER_PORT))
        data = sockIPv4.recv(1024)
    print(data.decode("utf-8"))


if __name__ == "__main__":
    connect_to_server()