import socket, ssl

HOST = "httpbin.org"
PORT = 443

HTTP_REQUEST = """GET /html HTTP/1.1\r\nHost: httpbin.org\r\nUser-Agent:Safari/7.0.3\r\n\r\n"""

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
        if not cert or ssl.match_hostname(cert, self.host):
            raise Exception("Invalid SSL certificate")


    def getContent(self, filename="index.html"):
        self.secure_sock.write(HTTP_REQUEST.encode())
        with open(filename, "wb") as file:
            while True:
                received = self.secure_sock.read(4096)
                if not received:
                    break
                file.write(received)
        self.secure_sock.close()

if __name__ == "__main__":
    client = Client()
    # client.setupSecureConnection()
    # client.getContent()
    client.setupVerifiedConnection()
    client.getContent("index_verified.html")