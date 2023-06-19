import socket
import random
from enum import Enum


HOST="127.0.0.1"
PORT=3103


class GuessResult(Enum):
    CORRECT = "Correct!"
    TOO_BIG = "Too big!"
    TOO_SMALL = "Too small!"
    SYNTAX_ERROR = "Syntax error"


def generate_random_number():
    return random.randint(0, 10000)


def interpret_guess(guess: str, random_number: int):
    try:
        guessValue = int(guess)

        if guessValue == random_number:
            return GuessResult.CORRECT
        elif guessValue > random_number:
            return GuessResult.TOO_BIG
        else:
            return GuessResult.TOO_SMALL
    except Exception:
        return GuessResult.SYNTAX_ERROR


def handle_guessing(client: socket, address):
    with client:
        print('Connected by', address)
        print("Generating random number...")
        random_number = generate_random_number()
        print("Random number generated: {}".format(random_number))

        while True:
            data = client.recv(1024)
            if not data:
                break

            decoded = data.decode()
            print("Received: {}".format(decoded))

            interpreted = interpret_guess(decoded, random_number)
            print("Response: ", interpreted.value)
            client.sendall(interpreted.value.encode("utf-8"))

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print("Server is listening on port {}".format(PORT))

        while True:
            try:
                client, address = server.accept()
                handle_guessing(client, address)
               
            except KeyboardInterrupt:
                print("Stopping server...")
                server.close()


if __name__ == '__main__':
    start_server()