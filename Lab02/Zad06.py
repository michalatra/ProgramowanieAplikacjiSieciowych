import socket


# Dla testów w lokalnym środowisku
SERVER_IP = "127.0.0.1"

# SERVER_IP = "212.182.24.27"
SERVER_PORT = 2902


def connect_to_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sockIPv4:
        sockIPv4.connect((SERVER_IP, SERVER_PORT))

        print("Enter 'exit' to finish")
        inputMesage: str = input("Enter message: ")

        while inputMesage != "exit":
            splitted = inputMesage.split(' ')
            if len(splitted) == 3:
                sockIPv4.send(splitted[0].encode("utf-8"))
                sockIPv4.send(splitted[1].encode("utf-8"))
                sockIPv4.send(splitted[2].encode("utf-8"))
                data = sockIPv4.recv(1024)
                print(data.decode("utf-8"))
            else:
                print("Wrong input")

            inputMesage = input("Enter message: ")

        print("Connection closed")


if __name__ == "__main__":
    connect_to_server()