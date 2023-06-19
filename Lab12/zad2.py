from threading import Thread, Lock
import socket
import sys
from datetime import datetime

HOST = '127.0.0.1'
PORT = 6790
FILE = 'file.txt'


class ClientThread(Thread):
    def __init__(self, conn, addr, lock):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.lock = lock
        print("["+ str(datetime.now()) + "] " + "New connection from: ", addr)
        
        with lock:
            with open(FILE, 'a') as f:
                f.write("["+ str(datetime.now()) + "] " + "New connection from: " + str(addr) + "\n")

    def run(self):
        try:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break

                decoded = data.decode('utf-8')

                print("["+ str(datetime.now()) + "] " + "Message from user " + str(self.addr) + ": ", decoded)
                with self.lock:
                    with open(FILE, 'a') as f:
                        f.write("["+ str(datetime.now()) + "] " + "Message from user " + str(self.addr) + ": " + decoded + "\n")

                self.conn.send(data)

                with self.lock:
                    with open(FILE, 'a') as f:
                        f.write("["+ str(datetime.now()) + "] " + "Message sent to user " + str(self.addr) + ": " + decoded + "\n")
        except Exception as e:
            print("An exception occurred: ", e)
            with self.lock:
                with open(FILE, 'a') as f:
                    f.write("["+ str(datetime.now()) + "] " + "An exception occurred: " + str(e) + "\n")
        finally:
            with self.lock:
                with open(FILE, 'a') as f:
                    f.write("["+ str(datetime.now()) + "] " + "Closing connection with user " + str(self.addr) + "\n")
            self.conn.close()



class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.lock = Lock()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        try:
            self.socket.bind((self.host, self.port))
            print("["+ str(datetime.now()) + "] " + "Server running on port: ", self.port)
            
            with self.lock:
                with open(FILE, 'a') as f:
                    f.write("["+ str(datetime.now()) + "] " + "Server running on port: " + str(self.port) + "\n")
            
            while True:
                self.socket.listen(5)
                conn, addr = self.socket.accept()
                new_thread = ClientThread(conn, addr, self.lock)
                new_thread.start()
        except Exception as e:
            print("An exception occurred: ", e)
            with self.lock:
                with open(FILE, 'a') as f:
                    f.write("["+ str(datetime.now()) + "] " + "An exception occurred: " + str(e) + "\n")
        finally:
            with self.lock:
                with open(FILE, 'a') as f:
                    f.write("["+ str(datetime.now()) + "] " + "Closing socket\n")
            self.socket.close()


if __name__ == '__main__':
    port = PORT
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    server = Server(HOST, port)
    server.run()