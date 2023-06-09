import sys
import socket


def try_connect(host: str, port: int):
    address = (host, port)

    try:
        service = socket.getservbyport(port)
    except OSError:
        service = "unknown"

    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.settimeout(1)
        soc.connect(address)
        if soc:
            print("Connection on port %s was successful (service: %s)" % (port, service))
    except socket.error:
        print("Connection not successfull on port %s (service: %s)" % (port, service))
    finally:
        soc.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("No host or port provided.")
        exit()

    try_connect(sys.argv[1], int(sys.argv[2]))
