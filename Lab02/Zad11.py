import sys
import socket

# Dla testów w lokalnym środowisku
SERVER_IP = "127.0.0.1"

# SERVER_IP = "212.182.24.27"
SERVER_PORT = 2908
MESSAGE_CONTENT = "Test Message Content Intended to Verify Server Functionality"


def connect_to_server(message_content: str):

    if len(message_content) > 20:
        message_content = message_content[:20]
    elif len(message_content) < 20:
        message_content += ' ' * (20 - len(message_content))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockIPv4:
        sockIPv4.connect((SERVER_IP, SERVER_PORT))
        sockIPv4.send(message_content.encode("utf-8"))
        data = sockIPv4.recv(20)
    print(data.decode("utf-8"))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        connect_to_server(sys.argv[1])
    else:
        connect_to_server(MESSAGE_CONTENT)