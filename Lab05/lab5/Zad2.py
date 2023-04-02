import socket
import random

HOST="127.0.0.1"
PORT=3103

def generate_random_number():
    return random.randint(0, 10000)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print("Server is listening on port {}".format(PORT))

        while True:
            try:
                client, address = server.accept()
                with client:
                    print('Connected by', address)
                    print("Generating random number...")
                    random_number = generate_random_number()
                    print("Random number generated: {}".format(random_number))

                    while True:
                        data = client.recv(1024)
                        if not data:
                            break

                        decoded = data.decode()
                        print("Received: {}".format(decoded))

                        decoded = int(decoded)

                        if decoded == random_number:
                            print("Correct!")
                            client.sendall(b"Correct!")
                            break
                        elif decoded > random_number:
                            print("Too big!")
                            client.sendall(b"Too big!")
                        else:
                            print("Too small!")
                            client.sendall(b"Too small!")
            except KeyboardInterrupt:
                print("Stopping server...")
                server.close()


if __name__ == '__main__':
    start_server()