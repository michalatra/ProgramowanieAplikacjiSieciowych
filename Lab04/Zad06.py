import socket

IP = "127.0.0.1"
PORT = 9405


def get_result(data: str):
    try:
        host = socket.gethostbyname(data)
    except Exception:
        host = None

    if host:
        return host
    else:
        return "Invalid host"


def start_server():
    print("Starting server...")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((IP, PORT))

        while True:
            message, address = server.recvfrom(4096)
            print("Received: ", message.decode())

            result = get_result(message.decode())

            server.sendto(result.encode(), address)


if __name__ == "__main__":
    start_server()