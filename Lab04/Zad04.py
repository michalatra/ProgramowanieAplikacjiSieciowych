import socket

IP = "127.0.0.1"
PORT = 9403

def get_result(data: str):
    if len(data) == 0:
        return "Invalid input"
    
    splitted = data.split(" ")

    if len(splitted) != 3:
        return "Invalid input"

    first_num = int(splitted[0])
    second_num = int(splitted[2])
    operator = splitted[1]

    match operator:
        case "+": return str(first_num + second_num)
        case "-": return str(first_num - second_num)
        case "*": return str(first_num * second_num)
        case "/": return str(first_num / second_num)
        case "%": return str(first_num % second_num)
        case "^": return str(first_num ** second_num)
        case _: return "Invalid operator"


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