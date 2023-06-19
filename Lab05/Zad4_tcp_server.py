import socket

HOST = "127.0.0.1"
PORT = 9801


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.settimeout(10)
        server.listen()
        print("Server is listening on port {}".format(PORT))

        while True:
            try:
                client, address = server.accept()
                with client:
                    print('Connected by', address)
                    while True:
                        data = client.recv(1024)
                        if not data:
                            break
                        print("Received: {}".format(data.decode()))
            except socket.timeout:
                print("Server timed out")


if __name__ == "__main__":
    start_server()