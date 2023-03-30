import socket


TCP_DATAGRAM = """45 00 00 4e f7 fa 40 00 38 06 9d 33 d4 b6 18 1b
c0 a8 00 02 0b 54 b9 a6 fb f9 3c 57 c1 0a 06 c1
80 18 00 e3 ce 9c 00 00 01 01 08 0a 03 a6 eb 01
00 0b f8 e5 6e 65 74 77 6f 72 6b 20 70 72 6f 67
72 61 6d 6d 69 6e 67 20 69 73 20 66 75 6e"""

RES_HEAD_A = "zad15odpA"
RES_HEAD_B = "zad15odpB"

# SERVER_IP = "212.182.24.27"
SERVER_IP = "127.0.0.1"
SERVER_PORT = 2911

def send_result(result: str):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sockIPv4:
        sockIPv4.connect((SERVER_IP, SERVER_PORT))
        sockIPv4.send(result.encode("utf-8"))
        data = sockIPv4.recv(1024)
    
    decodedData = data.decode("utf-8")
    print(decodedData)
    return decodedData



def read_data_from_tcp():
    combined_frame = TCP_DATAGRAM\
        .replace(" ", "").replace("\n", "")

    version = int(combined_frame[0:1], base=16)

    protocol = int(combined_frame[18:20], base=16)

    source_ip_0 = int(combined_frame[24:26], base=16)
    source_ip_1 = int(combined_frame[26:28], base=16)
    source_ip_2 = int(combined_frame[28:30], base=16)
    source_ip_3 = int(combined_frame[30:32], base=16)
    source_ip = ".".join([str(source_ip_0), str(source_ip_1), str(source_ip_2), str(source_ip_3)])

    destination_ip_0 = int(combined_frame[32:34], base=16)
    destination_ip_1 = int(combined_frame[34:36], base=16)
    destination_ip_2 = int(combined_frame[36:38], base=16)
    destination_ip_3 = int(combined_frame[38:40], base=16)
    destination_ip = ".".join([str(destination_ip_0), str(destination_ip_1), str(destination_ip_2), str(destination_ip_3)])

    source_port = int(combined_frame[40:44], base=16)
    destination_port = int(combined_frame[44:48], base=16)
    sequence_number = int(combined_frame[48:56], base=16)
    acknowledgement_number = int(combined_frame[56:64], base=16)
    heade_length = int(combined_frame[64:65], base=16)
    data = bytearray.fromhex(combined_frame[104:]).decode("utf-8")


    print("Version: ", version)
    print("Protocol: ",  protocol)
    print("Source ip: ", source_ip)
    print("Destination ip: ", destination_ip)
    print("Source port: ", source_port)
    print("Destination port: ", destination_port)
    print("Sequence number: ", sequence_number)
    print("Ack num: ", acknowledgement_number)
    print("Header length: ", heade_length)
    print("Data: ", data)

    result = send_result("%s;ver;%i;srcip;%s;dstip;%s;type;%i" % (RES_HEAD_A, version, source_ip, destination_ip, protocol))

    if result == "TAK":
        send_result("%s;srcport;%i;dstport;%i;data;%s" % (RES_HEAD_B, source_port, destination_port, data))



if __name__ == "__main__":
    read_data_from_tcp()