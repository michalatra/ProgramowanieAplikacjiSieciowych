import socket


HOST = "127.0.0.1"
PORT = 3103


def get_number_from_user(client: socket.socket):
    while True:
        try:
            number = int(input("Please enter a number: "))
            client.sendall(str(number).encode())
            response = client.recv(1024)
            decoded = response.decode()
            print(decoded)

            if decoded == "Correct!":
                print("You won!")
                break
            elif decoded == "Too big!":
                print("Your number is too big!")
            else:
                print("Your number is too small!")

        except ValueError:
            print("Not a number")


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        get_number_from_user(client)


if __name__ == "__main__":
    start_client()