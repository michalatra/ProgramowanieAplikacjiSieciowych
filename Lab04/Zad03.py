import socket

IP = "127.0.0.1"
PORT = 9402


def start_server():
    print("Starting server...")
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
                server.bind((IP, PORT))
                server.settimeout(5)

                message, address = server.recvfrom(4096)
                print("Received: ", message.decode())

                server.sendto(message, address)
        except TimeoutError:
            print("Timeout")
            continue
        except InterruptedError:
            print("Interrupted")
            exit(0)

if __name__ == "__main__":
    start_server()