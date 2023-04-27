import socket
from enum import Enum


IP = '127.0.0.1'
PORT = 1588


SERVER_DOMAIN = "test.umcs.pl"
INIT_MESSAGE = f"220 {SERVER_DOMAIN} SMTP Service ready\r\n"


class SMTPCommand(Enum):
    HELO = 1
    MAIL = 2
    RCPT = 3
    DATA = 4
    QUIT = 5
    ERROR = 6


class SMTPResponseCode(Enum):
    OK = 1
    START_MAIL_INPUT = 2
    CLOSING_CONNECTION = 3
    SYNTAX_ERROR = 4


class SMTPResponse:
    def __init__(self, command: SMTPCommand, response_code: SMTPResponseCode, response: bytes):
        self.command = command
        self.responseCode = response_code
        self.response = response


class Mail:
    def __init__(self, sender: str, recipient: str, content: str):
        self.sender = sender
        self.recipient = recipient
        self.content = content


def interpret_command(command):
    command = command.decode().split(" ")
    if command[0] == "HELO":
        return SMTPResponse(SMTPCommand.HELO, SMTPResponseCode.OK, b"250 OK\r\n")
    elif command[0] == "MAIL":
        return SMTPResponse(SMTPCommand.MAIL, SMTPResponseCode.OK, b"250 OK\r\n")
    elif command[0] == "RCPT":
        return SMTPResponse(SMTPCommand.RCPT, SMTPResponseCode.OK, b"250 OK\r\n")
    elif command[0] == "DATA":
        return SMTPResponse(SMTPCommand.DATA, SMTPResponseCode.START_MAIL_INPUT, b"354 Start mail input; end with <CRLF>.<CRLF>\r\n")
    elif command[0] == "QUIT":
        return SMTPResponse(SMTPCommand.QUIT, SMTPResponseCode.CLOSING_CONNECTION, b"221 Closing connection\r\n")
    else:
        return SMTPResponse(SMTPCommand.ERROR, SMTPResponseCode.SYNTAX_ERROR, b"500 Syntax error, command unrecognized\r\n")


def handle_smtp_connection(connection):
    mail = Mail("", "", "")

    connection.send(INIT_MESSAGE.encode())

    while True:
        data = connection.recv(1024)
        interpreted = interpret_command(data)
        connection.send(interpreted.response)
        if interpreted.responseCode == SMTPResponseCode.CLOSING_CONNECTION:
            connection.close()
            break


def start_email_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((IP, PORT))
        server.listen()

        print(f"Server is listening on {IP}:{PORT}")

        while True:
            try:
                connection, address = server.accept()
                print(f"Connection with {address} has been established")
                handle_smtp_connection(connection)
            except KeyboardInterrupt:
                print("Server is shutting down")
                exit(0)
            except Exception as e:
                print("Unexpected error occurred ", e)

if __name__ == "__main__":
    start_email_server()
