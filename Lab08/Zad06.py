import socket
from _thread import *
import threading
from enum import Enum


IP = '127.0.0.1'
PORT = 1590


log_lock = threading.Lock()


class IMAPCommandEnum(Enum):
    LIST = 0
    CREATE = 1
    DELETE = 2
    RENAME = 3
    SELECT = 4
    SEARCH = 5
    FETCH = 6
    STATUS = 7
    EXPUNGE = 8
    STORE = 9
    LOGIN = 10
    LOGOUT = 11
    CLOSE = 12


class IMAPStatusDataEnum(Enum):
    MESSAGES = 0
    RECENT = 1
    UIDNEXT = 2
    UIDVALIDITY = 3
    UNSEEN = 4


class IMAPConnection:
    def __init__(self, conn: socket.socket, addr: str):
        self.conn = conn
        self.addr = addr

    def start(self):
        try:
            with self.conn:
                while True:
                    data = self.conn.recv(1024)

        except Exception as e:
            log_lock.acquire()
            print(f'Error: {e}')
            log_lock.release()


    def parse_command(self, command: binary):

def connection_thread(conn: socket.socket, addr: str):
    imap_connection = IMAPConnection(conn, addr)
    imap_connection.start()


class IMAPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()

            while True:
                conn, addr = s.accept()
                self.log_lock.acquire()
                print('Connected by', addr)
                log_lock.release()

                start_new_thread(connection_thread, (conn, addr))


if __name__ == '__main__':
    imap = IMAPServer(IP, PORT)
    imap.start()