import socket
from enum import Enum

HOST = "httpbin.org"
HOST = "127.0.0.1"
PORT = 80

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    PATCH = "PATCH"
    

def generateHttpRequest(method: HTTPMethod, host: str, path: str, headers: dict[str, str] = None) -> str:
    return f"{method.value} {path} HTTP/1.1\r\nHost: {host}\r\n" + ('\r\n'.join([f"{key}: {value}" for key, value in headers.items()]) if len(headers) else "") + "\r\n\r\n"


class Client:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


    def getContent(self, filename="index.html"):
        request = generateHttpRequest(HTTPMethod.GET, HOST, "/html", {"User-Agent": "Safari/7.0.3"})
        print("Request:", request, sep="\n")
        self.sock.sendall(request.encode())
        response = b""
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            response = response + data
        self.sock.close()

        header, response = response.split(b"\r\n\r\n")
        print("Response:", header.decode(), sep="\n")

        self.writeToFile(filename, response)

    def writeToFile(self, filename, data):
        with open(filename, "wb") as f:
            f.write(data)


if __name__ == "__main__":
    client = Client()
    client.getContent("index.html")