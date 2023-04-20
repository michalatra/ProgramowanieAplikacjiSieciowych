import socket
from itertools import permutations


HOST = "127.0.0.1"
PORT = 2913
PING = "PING"


def scan_udp_ports():
    udp_sockets = []
    current_port = 666
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        while current_port < 65536:
            print("Scanning port {}".format(current_port))
            try:
                udp_socket.connect((HOST, current_port))
                udp_socket.sendto(PING.encode(), (HOST, current_port))
                (response, address) = udp_socket.recvfrom(1024)
                if response:
                    print(response.decode("utf-8"), address)
                    if response.decode("utf-8") == "PONG":
                        udp_sockets.append(address[1])
            except ConnectionRefusedError:
                pass

            current_port += 1000

    print("Found ports: {}".format(udp_sockets))
    return udp_sockets


def unlock_udp(udp_ports):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        for port in udp_ports:
            # udp_socket.connect((HOST, port))
            udp_socket.sendto(PING.encode(), (HOST, port))


def connect_tcp():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            tcp_socket.connect((HOST, PORT))
            tcp_socket.settimeout(10)
            tcp_socket.sendall("Hello".encode())
            response = tcp_socket.recv(1024)
            print(response.decode("utf-8"))
            return True
    except Exception as e:
        print("An error occurred:", e)
        return False

def verify_unlock_combinations(udp_ports: list):
    for perm in permutations(udp_ports, 3):
        print("Testing: ", perm)
        unlock_udp(udp_ports)
        if connect_tcp():
            break

if __name__ == "__main__":
    udp_ports = scan_udp_ports()
    print("Found ports: ", udp_ports)
    verify_unlock_combinations(udp_ports)
        # unlock_udp([34666, 17666, 53666])