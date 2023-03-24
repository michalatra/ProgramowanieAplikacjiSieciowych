import socket

IP = "127.0.0.1"
PORT = 9404


def get_result(data: str):
    try:
        hostname = socket.gethostbyaddr(data)[0]
    except Exception:
        hostname = None

    if hostname:
        return hostname
    else:
        return "Invalid hostname"


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