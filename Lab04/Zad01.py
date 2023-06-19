import socket
import datetime

IP = "127.0.0.1"
PORT = 9400


def start_server():
    print("Starting server...")
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                server.bind((IP, PORT))
                server.settimeout(5)
                server.listen()

                connection, address = server.accept()

                with connection:
                    print("Connected by", address)
                    while True:
                        data = connection.recv(1024)
                        if not data:
                            break
                        print("Received: ", data.decode())

                        now = datetime.datetime.now()
                        now = now.strftime("%Y-%m-%d %H:%M:%S")

                        connection.sendall(now.encode("utf-8"))
        except TimeoutError:
            print("Timeout")
            continue
        except InterruptedError:
            print("Interrupted")
            exit(0)


if __name__ == "__main__":
    start_server()