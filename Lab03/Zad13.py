import socket


UDP_DATAGRAM = """ed 74 0b 55 00 24 ef fd 70 72 6f 67 72 61
6d 6d 69 6e 67 20 69 6e 20 70 79 74 68 6f
6e 20 69 73 20 66 75 6e"""

RES_HEAD = "zad14odp"

# SERVER_IP = "212.182.24.27"
SERVER_IP = "127.0.0.1"
SERVER_PORT = 2910

def send_result(result: str):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sockIPv4:
        sockIPv4.connect((SERVER_IP, SERVER_PORT))
        sockIPv4.send(result.encode("utf-8"))
        data = sockIPv4.recv(1024)
    print(data.decode("utf-8"))



def read_data_from_udp():
    combined_frame = UDP_DATAGRAM\
        .replace(" ", "").replace("\n", "")

    source_port = int(combined_frame[0:4], base=16)
    destination_port = int(combined_frame[4:8], base=16)
    length = int(combined_frame[8:12], base=16)
    checksum = int(combined_frame[12:16], base=16)
    data = bytearray.fromhex(combined_frame[16:]).decode("utf-8")


    print(source_port, destination_port, length, checksum, data)
    send_result("%s;src;%i;dst;%i;data;%s" % (RES_HEAD, source_port, destination_port, data))

if __name__ == "__main__":
    read_data_from_udp()