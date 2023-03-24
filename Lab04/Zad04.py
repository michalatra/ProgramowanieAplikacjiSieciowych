import socket

IP = "127.0.0.1"
PORT = 9403

def get_result(data: str):
    splitted = data.split(" ")
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
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((IP, PORT))

        while True:
            message, address = server.recvfrom(4096)
            print("Received: ", message.decode())

            result = get_result(message.decode())

            server.sendto(result.encode(), address)


if __name__ == "__main__":
    start_server()