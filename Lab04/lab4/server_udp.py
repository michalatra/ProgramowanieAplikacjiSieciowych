import socket
import sys

# TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# nie bedzie bledu address already in use
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to the port
server_address = ('127.0.0.1', 8888)
sock.bind(server_address)

print 'Starting up UDP server on %s port %s' % server_address

try:
    # receive data from client - UDP
    data, client_address = sock.recvfrom(1024)
    print 'Client %s connected ... ' % str(client_address)

    if data:
        print 'received "%s"' % data

        # send data to client UDP
        sock.sendto(data, client_address)
            
finally:
    # clean up the connection
    sock.close()

