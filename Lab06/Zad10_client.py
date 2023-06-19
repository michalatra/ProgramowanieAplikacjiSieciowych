import socket
from enum import Enum

IP = "127.0.0.1"
PORT = 1588

class SMTPCommand(Enum):
    HELO = "HELO"
    MAIL = "MAIL FROM"
    RCPT = "RCPT TO"
    DATA = "DATA"
    NOOP = "NOOP"
    RSET = "RSET"
    QUIT = "QUIT"


def map_id_to_command(id: int) -> SMTPCommand:
    match id:
        case 0: return SMTPCommand.HELO
        case 1: return SMTPCommand.MAIL
        case 2: return SMTPCommand.RCPT
        case 3: return SMTPCommand.DATA
        case 4: return SMTPCommand.NOOP
        case 5: return SMTPCommand.RSET
        case 6: return SMTPCommand.QUIT
        case _: return None


def send_with_response(message: str, connection: socket.socket) -> str:
    try:
        print(f"Sending message: {message}")
        connection.sendall(f"{message}\r\n".encode("utf-8"))
        data = connection.recv(4096).decode()
        print(f"Received: {data}")
        return data
    except Exception as e:
        print("Unexpected error occurred ", e)
        return None
    

def send_without_response(message: str, connection: socket.socket):
    try:
        print(f"Sending message: {message}")
        connection.sendall(f"{message}\r\n".encode("utf-8"))
    except Exception as e:
        print("Unexpected error occurred ", e)
        return None
    

def get_command() -> SMTPCommand:
    print("Select command from available: ")
    for (idx, command) in enumerate(SMTPCommand):
        print(f"{idx + 1}. {command.value}")

    while True:
        command = input("Enter command: ")
        mapped = map_id_to_command(int(command) - 1)
        if mapped:
            return mapped
        else:
            print("Invalid command")


def handle_command(connection: socket.socket):
    while True:
        command = get_command()
        
        if command in [SMTPCommand.HELO, SMTPCommand.RCPT, SMTPCommand.MAIL]:
            parameter = input("Enter parameter: ")
            message = f"{command.value} {parameter}"

            response = send_with_response(message, connection)
            if response and response.startswith("250"):
                print("Message sent")
            else:
                print("Unexpected response from server while trying to send message")
        elif command in [SMTPCommand.NOOP, SMTPCommand.RSET]:
            response = send_with_response(command.value, connection)
            if response and response.startswith("250"):
                print("Message sent")
            else:
                print("Unexpected response from server while trying to send message")
        elif command == SMTPCommand.QUIT:
            print("Sending QUIT message...")
            response = send_with_response(command.value, connection)
            if response and response.startswith("221"):
                print("Closing connection")
                connection.close()
                break
            else:
                print("Unexpected response from server while trying to QUIT")
                continue
        elif command == SMTPCommand.DATA:
            print("Sending DATA message...")
            response = send_with_response(command.value, connection)
            if response and response.startswith("354"):
                while True:
                    message = input("Enter message: ")
                    if message == ".":
                        send_without_response(message, connection)
                        print("End of message sent")
                        break
                    send_without_response(message, connection)

                continue
            else:
                print("Unexpected response from server while trying to send DATA")
                continue
    


def send_message():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((IP, PORT))
            data = client.recv(4096)
            print("Received: ", data.decode())

            handle_command(client)
        except TimeoutError:
            print("Server is not responding")
        except InterruptedError:
            print("Interrupted")
            exit(0)


if __name__ == "__main__":
    send_message()