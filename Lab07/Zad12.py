import socket
from enum import Enum
from functools import reduce
import json


HOST = '127.0.0.1'
PORT = 3334

CRLF = '\r\n'


class POP3ErrorMessage(Enum):
    BAD_SYNTAX = 'Bad syntax'
    INVALID_COMMAND = 'Invalid command'
    INVALID_ARGUMENTS = 'Invalid arguments'
    INVALID_STATE = 'Invalid state'
    INVALID_USERNAME = 'Invalid username'
    INVALID_PASSWORD = 'Invalid password'
    INVALID_MESSAGE_NUMBER = 'Invalid message number'
    UNKNOWN_ERROR = 'Unknown error'


class POP3Message(Enum):
    WELCOME = 'POP3 server ready'


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


class POP3ConnectionState(Enum):
    AUTHORIZATION = 0
    TRANSACTION = 1
    UPDATE = 2


class POP3Response:
    def __init__(self, message: str, isQuit: bool = False):
        self.message = message
        self.isQuit = isQuit


class POP3RequestCommand:
    def __init__(self, keyword: POP3RequestKeyword, args: list[str]):
        self.keyword = keyword
        self.args = args

    def __str__(self):
        return self.keyword + ' ' + self.args + '\r\n'
    

class POP3Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_state = POP3ConnectionState.AUTHORIZATION
        self.username = None
        self.password = None
        self.logged_user_emails = None
        self.deleted_emails = []
        self.read_db()

    def read_db(self):
        with open('db.json', 'r') as f:
            self.db = json.load(f)


    def __del__(self):
        self.socket.close()


    def start_server(self):
        print("Strarting server...")
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print('Listening on port', self.port)
        while True:
            try:
                connection, address = self.socket.accept()
                print('Connected by', address)
                self.handle_connection(connection)
                connection.close()
                self.connection_state = POP3ConnectionState.AUTHORIZATION
                self.username = None
                self.password = None
                self.logged_user_emails = None
                self.deleted_emails = []
                print('Connection closed')
            except Exception as e:
                print("An exception occurred:", e)
                if connection:
                    connection.close()
                self.connection_state = POP3ConnectionState.AUTHORIZATION
                self.username = None
                self.password = None
                self.logged_user_emails = None
                self.deleted_emails = []


    def handle_connection(self, connection: socket.socket):
        connection.sendall(bytes(" ".join([POP3ResponseState.OK.value,  POP3Message.WELCOME.value, CRLF]), 'utf-8'))
        while True:
            request = connection.recv(1024)
            if not request:
                break
            response = self.handle_request(request.decode('utf-8'))
            connection.sendall(bytes(response.message, 'utf-8'))

            if response.isQuit:
                break


    def handle_request(self, request: str) -> POP3Response:
        print("Recieved request:", request)
        request = request.replace(CRLF, '')
        request = request.split(' ')

        match request[0].upper():
            case POP3RequestKeyword.USER.value:
                return self.handle_user_request(request)
            case POP3RequestKeyword.PASS.value:
                return self.handle_pass_request(request)
            case POP3RequestKeyword.STAT.value:
                return self.handle_stat_request(request)
            case POP3RequestKeyword.LIST.value:
                return self.handle_list_request(request)
            case POP3RequestKeyword.RETR.value:
                return self.handle_retr_request(request)
            case POP3RequestKeyword.DELE.value:
                return self.handle_dele_request(request)
            case POP3RequestKeyword.NOOP.value:
                return self.handle_noop_request(request)
            case POP3RequestKeyword.RSET.value:
                return self.handle_rset_request(request)
            case POP3RequestKeyword.QUIT.value:
                return self.handle_quit_request(request)
        
        return self.handle_unknown_request(request)
        

    def handle_user_request(self, request: str) -> POP3Response:
        if self.connection_state != POP3ConnectionState.AUTHORIZATION:
            return self.handle_invalid_state()
        if len(request) != 2:
            return self.handle_invalid_arguments()
        self.username = request[1]
        if self.username not in map(lambda x: x['username'], self.db['users']):
            self.username = None
            return self.handle_invalid_username()
        return self.handle_ok("User accepted")
    

    def handle_pass_request(self, request: str) -> POP3Response:
        if self.connection_state != POP3ConnectionState.AUTHORIZATION:
            return self.handle_invalid_state()
        if len(request) != 2:
            return self.handle_invalid_arguments()
        self.password = request[1]
        if self.username is not None:
            userIndex = list(map(lambda x: x['username'], self.db['users'])).index(self.username)
            if self.db['users'][userIndex]['password'] != self.password:
                self.password = None
                return self.handle_invalid_password()
    
            self.connection_state = POP3ConnectionState.TRANSACTION
            self.logged_user_emails = self.db['users'][userIndex]['emails']
            return self.handle_ok("Password accepted")
        return self.handle_invalid_state()
    

    def handle_stat_request(self, request: str) -> POP3Response:
        if self.connection_state != POP3ConnectionState.TRANSACTION:
            return self.handle_invalid_state()
        if len(request) != 1:
            return self.handle_invalid_arguments()
        
        filtered_emails = list(filter(lambda x: not x["isDeleted"], self.logged_user_emails))

        emails_count = len(filtered_emails)
        emails_size = reduce(lambda x, y: x + y, map(lambda x: x["size"], filtered_emails))

        return self.handle_ok(str(emails_count) + " messages " +  "(" + str(emails_size) + ")")
    

    def handle_list_request(self, request: str) -> POP3Response:
        if self.connection_state != POP3ConnectionState.TRANSACTION:
            return self.handle_invalid_state()
        if len(request) != 1:
            return self.handle_invalid_arguments()
        
        filtered_emails = list(filter(lambda x: not x["isDeleted"], self.logged_user_emails))

        emails_count = len(filtered_emails)
        emails_size = reduce(lambda x, y: x + y, map(lambda x: x["size"], filtered_emails))

        emails = str(emails_count) + " messages " +  "(" + str(emails_size) + ")" + CRLF
        for email in filtered_emails:
            emails += str(email["id"]) + " " + str(email["size"]) + CRLF

        emails += "."

        return self.handle_ok(emails)
        

    def handle_retr_request(self, request: str) -> POP3Response:
        if self.connection_state != POP3ConnectionState.TRANSACTION:
            return self.handle_invalid_state()
        if len(request) != 2:
            return self.handle_invalid_arguments()
        
        try:
            emailIdx = list(map(lambda x: x['id'], self.logged_user_emails)).index(int(request[1]))
            email = self.logged_user_emails[emailIdx]

            if email["isDeleted"]:
                return self.handle_invalid_message_number()

            emailContent = CRLF + "Date: " + email["sendDate"] + CRLF + "From: " + email["sender"] + CRLF + "To: " + email["recipient"] + CRLF + "Subject: " + email["title"] + CRLF + CRLF + email["content"] + CRLF + "."
            return self.handle_ok(emailContent)
        except ValueError:
            return self.handle_invalid_message_number()

    
    def handle_dele_request(self, request: str) -> POP3Response:
        if self.connection_state != POP3ConnectionState.TRANSACTION:
            return self.handle_invalid_state()
        if len(request) != 2:
            return self.handle_invalid_arguments()
        
        try:
            emailIdx = list(map(lambda x: x['id'], self.logged_user_emails)).index(int(request[1]))
            self.logged_user_emails[emailIdx]["isDeleted"] = True
            self.deleted_emails.append(self.logged_user_emails[emailIdx])
            return self.handle_ok("Message deleted")
        except ValueError:
            return self.handle_invalid_message_number()
        

    def handle_noop_request(self, request: str) -> POP3Response:
        if self.connection_state != POP3ConnectionState.TRANSACTION:
            return self.handle_invalid_state()
        if len(request) != 1:
            return self.handle_invalid_arguments()
        
        return self.handle_ok()
    

    def handle_rset_request(self, request: str) -> POP3Response:
        if self.connection_state != POP3ConnectionState.TRANSACTION:
            return self.handle_invalid_state()
        if len(request) != 1:
            return self.handle_invalid_arguments()
        
        for email in self.deleted_emails:
            email["isDeleted"] = False
        self.deleted_emails = []

        return self.handle_ok("Maildrop has " + str(len(self.logged_user_emails)) + " messages (" + str(reduce(lambda x, y: x + y, map(lambda x: x["size"], filter(lambda x: not x["isDeleted"], self.logged_user_emails)))) + " octets)")
    

    def handle_quit_request(self, request: str) -> POP3Response:
        if len(request) != 1:
            return self.handle_invalid_arguments()
        
        self.connection_state = POP3ConnectionState.UPDATE
        return self.handle_ok("Goodbye", True)
    

    def handle_invalid_username(self) -> POP3Response:
        return self.handle_error(POP3ErrorMessage.INVALID_USERNAME)
    

    def handle_invalid_password(self) -> POP3Response:
        return self.handle_error(POP3ErrorMessage.INVALID_PASSWORD)
    

    def handle_unknown_request(self, request: str) -> POP3Response:
        return self.handle_error(POP3ErrorMessage.INVALID_COMMAND)
    

    def handle_ok(self, comment: str = "", isQuit: bool = False) -> POP3Response:
        return POP3Response(" ".join([POP3ResponseState.OK.value, comment, CRLF]), isQuit)
    

    def handle_invalid_state(self) -> POP3Response:
        return self.handle_error(POP3ErrorMessage.INVALID_STATE)
    

    def handle_invalid_arguments(self) -> POP3Response:
        return self.handle_error(POP3ErrorMessage.INVALID_ARGUMENTS)
    

    def handle_invalid_message_number(self) -> POP3Response:
        return self.handle_error(POP3ErrorMessage.INVALID_MESSAGE_NUMBER)
    

    def handle_error(self, error: POP3ErrorMessage) -> POP3Response:
        return POP3Response(" ".join([POP3ResponseState.ERR.value, error.value, CRLF]))


if __name__ == "__main__":
    server = POP3Server(HOST, PORT)
    server.start_server()