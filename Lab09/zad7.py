import socket
from threading import Thread
import sys
from enum import Enum 


HOST = "127.0.0.1"
PORT = 8080


class SupportedEndpoints(Enum):
    ROOT = "/"
    HELLO = "/hello"
    HELLO_NAME = "/hello/"
    FORM = "/form"
    PNG = "/png"
    JPG = "/jpg"
    POST = "/post"


class SupportedHttpMethods(Enum):
    GET = "GET"
    POST = "POST"


class ClientThread(Thread):
    def __init__(self, conn: socket, addr):
        Thread.__init__(self)
        self.conn = conn
        self.conn.settimeout(1)
        self.addr = addr

    def __del__(self):
        self.conn.close()
        print("Client thread for", self.addr, "closed")

    def handleNotFound(self, endpoint: str) -> bytes:
        print("Not found:", endpoint)
        response = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 Not Found</h1><p>The requested URL {endpoint} was not found on this server.</p>"
        return response.encode()

    def handleRootEndpoint(self) -> bytes:
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        with open("welcome.html", "r") as f:
            response += f.read()
        return response.encode()
    
    def handleHelloEndpoint(self) -> bytes:
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        with open("hello.html", "r") as f:
            response += f.read()
        return response.encode()
    
    def handleHelloNameEndpoint(self, name: str) -> bytes:
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        with open("hello_name.html", "r") as f:
            response += f.read().replace("{name}", name)
        return response.encode()
    
    def handleFormEndpoint(self) -> bytes:
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        with open("form.html", "r") as f:
            response += f.read()
        return response.encode()
    
    def handlePngEndpoint(self) -> bytes:
        file_content = b""
        with open("img.png", "rb") as f:
            file_content += f.read()
        return f"HTTP/1.1 200 OK\r\nContent-Type: image/png\r\nContent-Length: {len(file_content)}\r\n\r\n".encode() + file_content + b"\r\n"
    
    def handleJpgEndpoint(self) -> bytes:
        file_content = b""
        with open("img.jpg", "rb") as f:
            file_content += f.read()
        return f"HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nContent-Length: {len(file_content)}\r\n\r\n".encode() + file_content + b"\r\n"
    
    def handlePostEndpoint(self, data: str) -> bytes:
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        response += f"<p>POST data: {data}</p>"
        return response.encode()
    


    def handleHttpRequest(self, data: bytes) -> bytes:
        data = data.decode()
        print("Recieved: ", data, sep="\n")
        method, endpoint, httpVersion = data.split("\r\n")[0].split(" ")

        match method:
            case SupportedHttpMethods.GET.value:
                match endpoint:
                    case SupportedEndpoints.ROOT.value:
                        return self.handleRootEndpoint()
                    case SupportedEndpoints.HELLO.value:
                        return self.handleHelloEndpoint()
                    case SupportedEndpoints.FORM.value:
                        return self.handleFormEndpoint()
                    case SupportedEndpoints.PNG.value:
                        return self.handlePngEndpoint()
                    case SupportedEndpoints.JPG.value:
                        return self.handleJpgEndpoint()
                    case _:
                        if endpoint.startswith(SupportedEndpoints.HELLO_NAME.value):
                            return self.handleHelloNameEndpoint(endpoint.split("/")[-1])
                        return self.handleNotFound(endpoint)
            case SupportedHttpMethods.POST.value:
                match endpoint:
                    case SupportedEndpoints.POST.value:
                        return self.handlePostEndpoint(data.split("\r\n\r\n")[-1])
                    case _:
                        return self.handleNotFound(endpoint)
            case _:
                return self.handleNotFound(endpoint)


    def run(self):
        print("New client thread started for ", self.addr)
        try:
            request = b""
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                request = request + data
                if len(data) < 1024:
                    break
            response = self.handleHttpRequest(request)
            print("Sending response: ", response.decode(), sep="\n")
            self.conn.send(response)
            print("Response sent")
            self.conn.close()

        except Exception as e:
            self.conn.close()

class HttpServer:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))

    def start(self):
        print("Server started")
        print("Listening on port", self.port)
        while True:
            self.sock.listen(5)
            conn, addr = self.sock.accept()
            print("New connection from", addr)
            ClientThread(conn, addr).start()

if __name__ == "__main__":
    port = PORT
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    server = HttpServer(port=port)
    server.start()