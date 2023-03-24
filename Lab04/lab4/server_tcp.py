import socket
import sys

# TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# nie bedzie bledu address already in use
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to the port
server_address = ('127.0.0.1', 6666)
sock.bind(server_address)

print 'Starting up TCP server on %s port %s' % server_address

# listen for incoming connections
# the argument specifies the maximum number of queued connections and should be at least 0; the maximum value is system-dependent
sock.listen(1)

# accept client
connection, client_address = sock.accept()
print 'Client %s connected ... ' % str(client_address)

try:
    # receive data from client - TCP
    data = connection.recv(1024)
    if data:
        print 'received "%s"' % data
        # send data to client TCP
        connection.sendall(data)
            
finally:
    # clean up the connection
    connection.close()

