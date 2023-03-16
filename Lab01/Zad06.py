import sys
import socket


def try_connect(host: str, port: int):
    address = (host, port)

    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.settimeout(1)
        soc.connect(address)
        if soc:
            print("Connection successful")
    except socket.error:
        print("Connection error")
    finally:
        soc.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("No host or port provided.")
        exit()

    try_connect(sys.argv[1], int(sys.argv[2]))
