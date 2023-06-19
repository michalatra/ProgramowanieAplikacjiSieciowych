import sys
import socket

# Dla testów w lokalnym środowisku
SERVER_IP = "127.0.0.1"

# SERVER_IP = "212.182.24.27"
SERVER_PORT = 2908
MESSAGE_CONTENT = "Test Message Content Intended to Verify Server Functionality"

MESSAGE_LENGTH = 20


def connect_to_server(message_content: str):

    if len(message_content) > MESSAGE_LENGTH:
        message_content = message_content[:MESSAGE_LENGTH]
    elif len(message_content) < MESSAGE_LENGTH:
        message_content += ' ' * (MESSAGE_LENGTH - len(message_content))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockIPv4:
        sockIPv4.connect((SERVER_IP, SERVER_PORT))

        sent_bytes = 0
        encoded_message = message_content.encode("utf-8")

        while sent_bytes < len(encoded_message):
            sent_bytes += sockIPv4.send(encoded_message[sent_bytes:])

        data = ""
        while len(data) < MESSAGE_LENGTH:
            data += sockIPv4.recv(MESSAGE_LENGTH - len(data)).decode("utf-8")

    print(data)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        connect_to_server(sys.argv[1])
    else:
        connect_to_server(MESSAGE_CONTENT)