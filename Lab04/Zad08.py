import socket

IP = "127.0.0.1"
PORT = 9407


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

                    recieved_data = ""

                    while len(recieved_data) < 20:
                        data = connection.recv(20 - len(recieved_data))
                        print("Received: ", data.decode())
                        recieved_data += data.decode("utf-8")

                    connection.sendall(recieved_data.encode("utf-8"))
        
        except TimeoutError:
            print("Timeout")
            continue
        except InterruptedError:
            print("Interrupted")
            exit(0)

if __name__ == "__main__":
    start_server()