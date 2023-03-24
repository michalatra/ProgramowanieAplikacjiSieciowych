import socket


TCP_DATAGRAM = """45 00 00 4e f7 fa 40 00 38 06 9d 33 d4 b6 18 1b
c0 a8 00 02 0b 54 b9 a6 fb f9 3c 57 c1 0a 06 c1
80 18 00 e3 ce 9c 00 00 01 01 08 0a 03 a6 eb 01
00 0b f8 e5 6e 65 74 77 6f 72 6b 20 70 72 6f 67
72 61 6d 6d 69 6e 67 20 69 73 20 66 75 6e"""

RES_HEAD = "zad13odp"

SERVER_IP = "212.182.25.252"
# SERVER_IP = "127.0.0.1"
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

    version = int(combined_frame[0:1], base=16)

    protocol = int(combined_frame[18:20], base=16)

    source_ip_0 = int(combined_frame[32:34], base=16)
    source_ip_1 = int(combined_frame[34:36], base=16)
    source_ip_2 = int(combined_frame[36:38], base=16)
    source_ip_3 = int(combined_frame[38:40], base=16)
    source_ip = ".".join([str(source_ip_0), str(source_ip_1), str(source_ip_2), str(source_ip_3)])

    destination_ip_0 = int(combined_frame[40:42], base=16)
    destination_ip_1 = int(combined_frame[42:44], base=16)
    destination_ip_2 = int(combined_frame[44:46], base=16)
    destination_ip_3 = int(combined_frame[46:48], base=16)
    destination_ip = ".".join([str(destination_ip_0), str(destination_ip_1), str(destination_ip_2), str(destination_ip_3)])

    source_port = int(combined_frame[48:52], base=16)
    destination_port = int(combined_frame[52:56], base=16)
    sequence_number = int(combined_frame[56:64], base=16)
    acknowledgement_number = int(combined_frame[64:72], base=16)
    # data = bytearray.fromhex(combined_frame[64:]).decode("utf-8")


    print(version, protocol, source_ip, destination_ip, source_port, destination_port, sequence_number, acknowledgement_number)
    # print(source_port, destination_port, sequence_number, acknowledgement_number, data)
    # send_result("%s;src;%i;dst;%i;data;%s" % (RES_HEAD, source_port, destination_port, data))

if __name__ == "__main__":
    read_data_from_tcp()