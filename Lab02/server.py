import socketserver

HOST = ''
PORT = 2900

def start_server():
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()


if __name__ == '__main__':
    start_server()