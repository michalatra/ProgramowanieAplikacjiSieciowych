import socket
from enum import Enum
import time
import urllib.parse

# HOST = "httpbin.org"
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
    

def generateHttpRequestHeader(method: HTTPMethod, host: str, path: str, headers: dict[str, str] = None) -> str:
    return f"{method.value} {path} HTTP/1.1\r\nHost: {host}\r\n" + ('\r\n'.join([f"{key}: {value}" for key, value in headers.items()]) if len(headers) else "") + "\r\n\r\n"

def generateHttpRequestFormData(keys: list[str], values: list[str]) -> str:
    return "&".join([f"{key}={urllib.parse.quote(value)}" for key, value in zip(keys, values)])

class Client:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    
    def getData(self):
        self.custname  = input("Enter customer name: ").strip()
        self.custtel = input("Enter telephone: ").strip()
        self.custemail = input("Enter email: ").strip()
        self.size = input("Enter pizza size (small / medium / large): ").strip()
        self.toppings = input("Enter pizza toppings (bacon, extra cheese, onion, mushroom) (delimeter: ','): ").strip()
        self.delivery = input("Enter delivery time: ").strip()
        self.comments = input("Enter delivery instructions: ").strip()

        keys = [
            "custname", 
            "custtel", 
            "custemail", 
            "size", 
            "delivery", 
            "comments"
        ]

        values = [
            self.custname,
            self.custtel,
            self.custemail,
            self.size,
            self.delivery,
            self.comments
        ]

        for topping in self.toppings.split(","):
            keys.append("topping")
            values.append(topping)


        self.reqBody = generateHttpRequestFormData(keys, values)


    def getContent(self):
        self.reqBody = "custname=asd&custtel=asd&custemail=asd&size=%40%40&delivery=asd&comments=asd&topping=asd"
        requestBodyLength = len(self.reqBody)
        request = generateHttpRequestHeader(HTTPMethod.POST, HOST, "/post", {"User-Agent": "Safari/7.0.3", "Content-Type": "application/x-www-form-urlencoded", "Content-Length": str(requestBodyLength)})
        request = request + self.reqBody
        print("Request:", request, sep="\n")

        self.sock.send(request.encode())


        content = b""
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            content = content + data
        self.sock.close()

        print(content.decode())

if __name__ == "__main__":
    client = Client()
    client.getData()
    client.getContent()