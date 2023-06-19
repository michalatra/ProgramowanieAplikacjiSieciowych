import socket, ssl
from threading import Thread

HOST = "chat.freenode.net"
PORT = 7000

class Listener(Thread):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock

    def run(self):
        while True:
            message = self.sock.read(4096).decode()
            if message.startswith("PING"):
                self.sock.write(("PONG " + message.split()[1] + "\r\n").encode())
            else:
                print(message)


class Client:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


    def setupSecureConnection(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

        if ssl.HAS_SNI:
            self.secure_sock = self.context.wrap_socket(self.sock, server_hostname=self.host)
        else:
            self.secure_sock = self.context.wrap_socket(self.sock)


    def setupVerifiedConnection(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.load_default_certs()

        if ssl.HAS_SNI:
            self.secure_sock = self.context.wrap_socket(self.sock, server_hostname=self.host)
        else:
            self.secure_sock = self.context.wrap_socket(self.sock)
        
        cert = self.secure_sock.getpeercert()

        print(cert)

        self.listener = Listener(self.sock)

        if not cert or ssl.match_hostname(cert, self.host):
            raise Exception("Invalid SSL certificate")

    
    def initializeChat(self, nick = "hiperTest", channel = "#test123"):
        listener = Listener(self.secure_sock)
        setup_commands = [
            # "CAP LS 302",
            "NICK " + nick,
            "USER " + nick + " 0 * :" + nick,
            # "CAP REQ :account-notify account-tag away-notify batch cap-notify chghost extended-join invite-notify message-tags multi-prefix server-time setname userhost-in-names",
            # "CAP END",
            "WHO " + "~" + nick,
            "JOIN " + channel
        ]

        for command in setup_commands:
            self.secure_sock.write((command + "\r\n").encode())

        while True: 
            message = input("Message: ")
            self.secure_sock.write(("PRIVMSG " + channel + " :" + message + "\r\n").encode())


if __name__ == "__main__":
    client = Client()
    # client.setupSecureConnection()
    client.setupVerifiedConnection()
    client.initializeChat()