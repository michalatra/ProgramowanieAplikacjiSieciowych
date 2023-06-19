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
    NOOP = 5
    RSET = 6
    QUIT = 7
    ERROR = 8   


class SMTPResponseCode(Enum):
    OK = 1
    START_MAIL_INPUT = 2
    CLOSING_CONNECTION = 3
    SYNTAX_ERROR = 4
    PARAMETER_ERROR = 5


class SMTPResponse:
    def __init__(self, command: SMTPCommand, data: str, response_code: SMTPResponseCode, response: bytes):
        self.command = command
        self.data = data
        self.responseCode = response_code
        self.response = response


class Mail:
    def __init__(self, sender: str, recipient: str, content: str):
        self.sender = sender
        self.recipient = recipient
        self.content = content


def handle_helo_command(command: list[str]):
    if len(command) != 2:
        return SMTPResponse(SMTPCommand.ERROR, "", SMTPResponseCode.PARAMETER_ERROR, b"555 Parameter error, command unrecognized\r\n")
    else:
        return SMTPResponse(SMTPCommand.HELO, command[1], SMTPResponseCode.OK, b"250 OK\r\n")
    

def handle_mail_command(command: list[str]):
    if len(command) != 3 or command[1] != "FROM" or command[2] == "":
        return SMTPResponse(SMTPCommand.ERROR, "", SMTPResponseCode.PARAMETER_ERROR, b"555 Parameter error, command unrecognized\r\n")
    else:
        return SMTPResponse(SMTPCommand.MAIL, command[1], SMTPResponseCode.OK, b"250 OK\r\n")
    

def handle_rcpt_command(command: list[str]):
    if len(command) != 3 or command[1] != "TO" or command[2] == "":
        return SMTPResponse(SMTPCommand.ERROR, "", SMTPResponseCode.PARAMETER_ERROR, b"555 Parameter error, command unrecognized\r\n")
    else:
        return SMTPResponse(SMTPCommand.RCPT, command[1], SMTPResponseCode.OK, b"250 OK\r\n")


def handle_data_command(command: list[str]):
    if len(command) != 1:
        return SMTPResponse(SMTPCommand.ERROR, "", SMTPResponseCode.PARAMETER_ERROR, b"555 Parameter error, command unrecognized\r\n")
    else:
        return SMTPResponse(SMTPCommand.DATA, "", SMTPResponseCode.OK, b"354 Start mail input; end with <CRLF>.<CRLF>\r\n")
    

def handle_quit_command(command: list[str]):
    if len(command) != 1:
        return SMTPResponse(SMTPCommand.ERROR, "", SMTPResponseCode.PARAMETER_ERROR, b"555 Parameter error, command unrecognized\r\n")
    else:
        return SMTPResponse(SMTPCommand.QUIT, "", SMTPResponseCode.CLOSING_CONNECTION, b"221 Closing connection\r\n")
    
def handle_noop_command(command: list[str]):
    if len(command) != 1:
        return SMTPResponse(SMTPCommand.ERROR, "", SMTPResponseCode.PARAMETER_ERROR, b"555 Parameter error, command unrecognized\r\n")
    else:
        return SMTPResponse(SMTPCommand.NOOP, "", SMTPResponseCode.OK, b"250 OK\r\n")
    

def handle_rset_command(command: list[str]):
    if len(command) != 1:
        return SMTPResponse(SMTPCommand.ERROR, "", SMTPResponseCode.PARAMETER_ERROR, b"555 Parameter error, command unrecognized\r\n")
    else:
        return SMTPResponse(SMTPCommand.RSET, "", SMTPResponseCode.OK, b"250 OK\r\n")
    

def handle_data(mail: Mail, connection: socket.socket, interpreted: SMTPResponse):
    mail.content = ""
    connection.send(interpreted.response)
    try:
        while True:
            print("Waiting for data")
            data = connection.recv(1024).decode()
            mail.content += data
            print("Received data: ", data)
            print("Mail content = ", mail.content)
            if data == ".\r\n":
                connection.sendall(b"250 OK\r\n")
                break
        print(f"Mail from {mail.sender} to {mail.recipient} with content {mail.content}")
    except Exception as e:
        print("Unexpected error occurred ", e)
        connection.send(b"500 Syntax error, command unrecognized\r\n")


def interpret_command(command):
    try:
        command = command.decode().replace("\r\n", "").split(" ")

        print("Interpreting command: ", command)

        if command[0] == "HELO":
            return handle_helo_command(command)
        elif command[0] == "MAIL":
            return handle_mail_command(command)
        elif command[0] == "RCPT":
            return handle_rcpt_command(command)
        elif command[0] == "DATA":
            return handle_data_command(command)
        elif command[0] == "NOOP":
            return handle_noop_command(command)
        elif command[0] == "RSET":
            return handle_rset_command(command)
        elif command[0] == "QUIT":
            return handle_quit_command(command)
        else:
            return SMTPResponse(SMTPCommand.ERROR, "", SMTPResponseCode.SYNTAX_ERROR, b"500 Syntax error, command unrecognized\r\n")
    except Exception as e:
        print("Unexpected error occurred ", e)
        return SMTPResponse(SMTPCommand.ERROR, "", SMTPResponseCode.SYNTAX_ERROR, b"500 Syntax error, command unrecognized\r\n")


def handle_smtp_connection(connection):
    mail = Mail("", "", "")

    connection.send(INIT_MESSAGE.encode())

    while True:
        data = connection.recv(1024)
        interpreted = interpret_command(data)

        if interpreted.responseCode == SMTPResponseCode.OK:
            if interpreted.command == SMTPCommand.RCPT:
                mail.recipient = interpreted.data
            elif interpreted.command == SMTPCommand.MAIL:
                mail.sender = interpreted.data
            elif interpreted.command == SMTPCommand.DATA:
                handle_data(mail, connection, interpreted)

        if interpreted.responseCode != SMTPResponseCode.OK or interpreted.command != SMTPCommand.DATA:
            print("Sending response: ", interpreted.response)
            connection.send(interpreted.response)

        if interpreted.responseCode == SMTPResponseCode.CLOSING_CONNECTION:
            print("Closing connection")
            connection.close()
            break


def start_email_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((IP, PORT))
        server.listen()

        print(f"Server is listening on {IP}:{PORT}")

        try:
            while True:
                print("Waiting for connection")
                connection, address = server.accept()
                print(f"Connection with {address} has been established")
                handle_smtp_connection(connection)
        except KeyboardInterrupt:
            print("Server is shutting down")
            server.shutdown(socket.SHUT_RDWR)
            server.close()
            exit(0)
        except Exception as e:
            print("Unexpected error occurred ", e)

if __name__ == "__main__":
    start_email_server()
