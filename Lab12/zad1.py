import threading
import socket
import sys

HOST = '127.0.0.1'
PORT = 6780

class ClientThread(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        print("New connection from: ", addr)

    def run(self):
        try:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break

                decoded = data.decode('utf-8')

                print("Message from user " + str(self.addr) + ": ", decoded)
                self.conn.send(data)
        except Exception as e:
            print("An exception occurred: ", e)
        finally:
            self.conn.close()


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        try:
            self.socket.bind((self.host, self.port))
            print("Server running on port: ", self.port)
            while True:
                self.socket.listen(5)
                conn, addr = self.socket.accept()
                new_thread = ClientThread(conn, addr)
                new_thread.start()
        except Exception as e:
            print("An exception occurred: ", e)
        finally:
            self.socket.close()


if __name__ == '__main__':
    port = PORT
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    server = Server(HOST, port)
    server.run()