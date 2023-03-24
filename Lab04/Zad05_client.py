import socket

IP = "127.0.0.1"
PORT = 9404


def send_message():
    while True:
        message = input("Enter message: ")

        print("Sending message...")
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
            client.connect((IP, PORT))
            client.sendall(message.encode("utf-8"))
            data = client.recv(4096)
            print("Received: ", data.decode())

if __name__ == "__main__":
    send_message()