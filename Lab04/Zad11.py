import socket

IP = "127.0.0.1"
PORT = 9410

def get_result_a(splitted):
    try:
        if (len(splitted) != 9 
            or splitted[1] != "ver" 
            or splitted[3] != "srcip" 
            or splitted[5] != "dstip"
            or splitted[7] != "type"
         ):
            return "BAD_SYNTAX"

        version = int(splitted[2])
        srcIp = splitted[4]
        dstIp = splitted[6]
        type = int(splitted[8])

        if version == 4 and srcIp == "212.182.24.27" and dstIp == "192.168.0.2" and type == 6:
            return "TAK"
        else:
            return "NIE"
    except Exception:
        return "BAD_SYNTAX"


def get_result_b(splitted):
    try:
        if (len(splitted) != 7
            or splitted[1] != "srcport" 
            or splitted[3] != "dstport" 
            or splitted[5] != "data"
         ):
            return "BAD_SYNTAX"

        src = int(splitted[2])
        dst = int(splitted[4])
        data = splitted[6]

        if src == 2900 and dst == 47526 and data == "network programming is fun":
            return "TAK"
        else:
            return "NIE"
    except Exception:
        return "BAD_SYNTAX"


def get_result(message):
    try:
        if len(message) == 0:
            return "BAD_SYNTAX"
        
        splitted = message.split(";")

        if splitted[0] == "zad15odpA":
            return get_result_a(splitted)
        elif splitted[0] == "zad15odpB":
            return get_result_b(splitted)
        else:
            return "BAD_SYNTAX"

    except Exception:
        return "BAD_SYNTAX"


def start_server():
    print("Starting server...")

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
                server.bind((IP, PORT))
                server.settimeout(5)

                message, address = server.recvfrom(4096)
                print("Received: ", message.decode())

                result = get_result(message.decode())

                server.sendto(result.encode(), address)

        except TimeoutError:
            print("Timeout")
            continue
        except InterruptedError:
            print("Interrupted")
            exit(0)


if __name__ == "__main__":
    start_server()