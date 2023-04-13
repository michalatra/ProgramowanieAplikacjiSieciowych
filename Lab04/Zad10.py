import socket

IP = "127.0.0.1"
PORT = 9409


def get_result(message):
    try:
        if len(message) == 0:
            return "BAD_SYNTAX"
        
        splitted = message.split(";")

        if len(splitted) != 7:
            return "BAD_SYNTAX"

        if splitted[0] != "zad13odp":
            return "BAD_SYNTAX"
        
        
        if splitted[1] != "src":
            return "BAD_SYNTAX"
    
        
        if splitted[3] != "dst":
            return "BAD_SYNTAX"
        
        
        if splitted[5] != "data":
            return "BAD_SYNTAX"
        

        src = int(splitted[2])
        dst = int(splitted[4])
        data = splitted[6]

        if src == 2900 and dst == 35211 and data == "hello :)":
            return "TAK"
        else:
            return "NIE"

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