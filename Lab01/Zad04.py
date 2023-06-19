import sys
import socket

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No address provided.")
        exit()

    address = sys.argv[1]
    hostname = socket.gethostbyaddr(address)

    print("Hostname: ", hostname)
