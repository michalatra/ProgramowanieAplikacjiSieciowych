import socket

IP = "127.0.0.1"
PORT = 9406


def send_message():
    while True:
        message = input("Enter message: ")

        print("Sending message...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            try:
                client.connect((IP, PORT))
                client.sendall(message.encode("utf-8"))
                client.settimeout(5)
                data = client.recv(4096)
                print("Received: ", data.decode())
            except TimeoutError:
                print("Server is not responding")
            except InterruptedError:
                print("Interrupted")
                exit(0)


if __name__ == "__main__":
    send_message()