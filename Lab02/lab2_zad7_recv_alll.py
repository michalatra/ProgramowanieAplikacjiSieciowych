#!/usr/bin/env python
import socket
import sys

def recvall(sock, msgLen):
    msg = ""
    bytesRcvd = 0

    while bytesRcvd < msgLen:

        chunk = sock.recv(msgLen - bytesRcvd)

        if chunk == "": break

        bytesRcvd += len(chunk)
        msg += chunk

    return msg

#remoteServer    = raw_input("Enter a remote host to scan: ")
#remoteServerIP  = socket.gethostbyname(remoteServer)
#remotePort = raw_input("Enter remote port: ")
#port = int(remotePort)

remoteServerIP = "212.182.24.27"
port = 22

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))
        sock.send('Just a text \n') 
        bytes = recvall(sock, 4096)
        
        if result == 0:
            print "Port {} is open, data = {}".format(port, bytes)
	else:
		print "Port {} is closed, data = {}".format(port, bytes)
        sock.close()

except KeyboardInterrupt:
    print "You pressed Ctrl+C"
    sys.exit()

except socket.gaierror:
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

except socket.error:
    print "Couldn't connect to server"
    sys.exit()
