import socket
from enum import Enum


HOST = '127.0.0.1'
PORT = 3334

CRLF = '\r\n'


class POP3RequestKeyword(Enum):
    USER = 'USER'
    PASS = 'PASS'
    STAT = 'STAT'
    LIST = 'LIST'
    RETR = 'RETR'
    DELE = 'DELE'
    QUIT = 'QUIT'
    NOOP = 'NOOP'
    RSET = 'RSET'


class POP3ResponseState(Enum):
    OK = '+OK'
    ERR = '-ERR'


class OperationResult(Enum):
    SUCCESS = 0
    FAIL = 1

class POP3Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.password = None
        self.is_logged_in = False


    def connect(self) -> OperationResult:
        try:
            self.socket.connect((self.host, self.port))
            print('Connected to server')
            
            data = self.socket.recv(1024)
            print("Recieved: ", data.decode())

            data = data.decode().replace(CRLF, "").split(" ")
            if data[0] == POP3ResponseState.OK.value:
                return OperationResult.SUCCESS
            else:
                self.socket.close()
                return OperationResult.FAIL

        except socket.error as e:
            print('Connection error: {}'.format(e))
            return OperationResult.FAIL
        

    def collect_credentials(self) -> OperationResult:
        self.username = input('Username: ')
        self.password = input('Password: ')
        if self.username and self.password:
            return OperationResult.SUCCESS

        print('Invalid credentials')
        return OperationResult.FAIL


    def login(self) -> OperationResult:
        if self.collect_credentials() != OperationResult.SUCCESS:
            self.is_logged_in = False
            return OperationResult.FAIL

        self.socket.sendall((POP3RequestKeyword.USER.value + ' ' + self.username + CRLF).encode())
        data = self.socket.recv(1024)
        print("Recieved: ", data.decode())

        if data.decode().replace(CRLF, "").strip().split(" ")[0] != POP3ResponseState.OK.value:
            print('Invalid username')
            self.is_logged_in = False
            return OperationResult.FAIL
        
        self.socket.sendall((POP3RequestKeyword.PASS.value + ' ' + self.password + CRLF).encode())
        data = self.socket.recv(1024)
        print("Recieved: ", data.decode())

        if data.decode().replace(CRLF, "").strip().split(" ")[0] != POP3ResponseState.OK.value:
            print('Invalid password')
            self.is_logged_in = False
            return OperationResult.FAIL
        
        self.is_logged_in = True
        return OperationResult.SUCCESS
    

    def get_messages_sizes(self) -> OperationResult:
        if not self.is_logged_in:
            print('Not logged in')
            return OperationResult.FAIL

        self.socket.sendall((POP3RequestKeyword.LIST.value + CRLF).encode())
        data = self.socket.recv(1024)
        print("Recieved: ", data.decode())

        data = data.decode().strip().split(CRLF)

        header = data[0].split(" ")

        if header[0] != POP3ResponseState.OK.value:
            print('An error occurred while getting messages sizes')
            return OperationResult.FAIL
        
        if len(header) != 4:
            print('An error occurred while parsing messages sizes')
            return OperationResult.FAIL
        

        try:
            messages_count = int(header[1])

            if len(data) != messages_count + 2:
                print('An error occurred while parsing messages sizes')
                return OperationResult.FAIL
            
            data = data[1:-1]

            print('---------------------------------  Messages sizes  ---------------------------------')
            for message in data:
                message = message.split(" ")
                print('Message {} has a size of {} bytes'.format(message[0], message[1]))
            print('------------------------------------------------------------------------------------')

            return OperationResult.SUCCESS
        except ValueError:
            print('An error occurred while parsing messages sizes')
            return OperationResult.FAIL
        
    
    def close(self):
        self.socket.close()
        print('Connection closed')




if __name__ == '__main__':
    client = POP3Client(HOST, PORT)

    while client.connect() != OperationResult.SUCCESS:
        user_response = input("An error occurred while connecting to server. Do you want to try again? (y/n): ")
        if user_response.lower() != 'y':
            exit(1)
        

    while client.login() != OperationResult.SUCCESS:
        user_response = input("An error occurred while logging in. Do you want to try again? (y/n): ")
        if user_response.lower() != 'y':
            exit(1)

    while client.get_messages_sizes() != OperationResult.SUCCESS:
        user_response = input("An error occurred while retrieving message list. Do you want to try again? (y/n): ")
        if user_response.lower() != 'y':
            exit(1)  

    client.close()