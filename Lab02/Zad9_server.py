import socket

SERVER_PORT = 2906

def start_server():
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.bind(('', SERVER_PORT))

        while True:
            data, addr = soc.recvfrom(1024)
            print(data.decode("utf-8"))
            soc.sendto(data, addr)

    except socket.error:
        print("Socket creation error")
        exit()


if __name__ == "__main__":
    start_server()