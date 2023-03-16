import sys
import socket


def perform_port_scan(host: str):
    for port in range(1, 65536):
        address = (host, port)

        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.settimeout(0.1)
            soc.connect(address)
            if soc:
                print("Found open port: ", port)
        except socket.error:
            pass
        finally:
            soc.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No host provided.")
        exit()

    perform_port_scan(sys.argv[1])