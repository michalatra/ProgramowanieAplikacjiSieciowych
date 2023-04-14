import socket

IP = "127.0.0.1"
PORT = 1588


def send_message():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((IP, PORT))
            data = client.recv(4096)
            print("Received: ", data.decode())

            while True:
                message = input("Enter message: ")

                print("Sending message...")
                client.sendall(message.encode("utf-8"))
                data = client.recv(4096)
                print("Received: ", data.decode())

        except TimeoutError:
            print("Server is not responding")
        except InterruptedError:
            print("Interrupted")
            exit(0)


if __name__ == "__main__":
    send_message()