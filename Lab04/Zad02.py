import socket

IP = "127.0.0.1"
PORT = 9401


def start_server():
    print("Starting server...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((IP, PORT))
        server.listen()

        while True:
            connection, address = server.accept()

            with connection:
                print("Connected by", address)
                while True:
                    data = connection.recv(4096)
                    if not data:
                        break
                    print("Received: ", data.decode())

                    connection.sendall(data)


if __name__ == "__main__":
    start_server()