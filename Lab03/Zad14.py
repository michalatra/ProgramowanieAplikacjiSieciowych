import socket


TCP_DATAGRAM = """0b 54 89 8b 1f 9a 18 ec bb b1 64 f2 80 18
00 e3 67 71 00 00 01 01 08 0a 02 c1 a4 ee
00 1a 4c ee 68 65 6c 6c 6f 20 3a 29"""

RES_HEAD = "zad13odp"

# SERVER_IP = "212.182.24.27"
SERVER_IP = "127.0.0.1"
SERVER_PORT = 2909

def send_result(result: str):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sockIPv4:
        sockIPv4.connect((SERVER_IP, SERVER_PORT))
        sockIPv4.send(result.encode("utf-8"))
        data = sockIPv4.recv(1024)
    print(data.decode("utf-8"))



def read_data_from_tcp():
    combined_frame = TCP_DATAGRAM\
        .replace(" ", "").replace("\n", "")

    source_port = int(combined_frame[0:4], base=16)
    destination_port = int(combined_frame[4:8], base=16)
    sequence_number = int(combined_frame[8:16], base=16)
    acknowledgement_number = int(combined_frame[16:24], base=16)
    data = bytearray.fromhex(combined_frame[64:]).decode("utf-8")


    print(source_port, destination_port, sequence_number, acknowledgement_number, data)
    send_result("%s;src;%i;dst;%i;data;%s" % (RES_HEAD, source_port, destination_port, data))

if __name__ == "__main__":
    read_data_from_tcp()