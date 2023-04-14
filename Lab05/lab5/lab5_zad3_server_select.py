13
#!/usr/bin/python

import socket, select, time
from time import gmtime, strftime

HOST = '127.0.0.1'
TCP_PORT = 2913
UDP_PORTS = [34666, 17666, 53666]


def gettime():
    return str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))


def set_up_udp_ports(host, ports):
    udpsockets = []
    for port in ports:
        udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpsock.bind((host, port))
        udpsock.setblocking(0)
        udpsockets.append(udpsock)
    return udpsockets


def open_tcp_port(host, port):
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((host, port))
    tcpsock.listen(1)
    conn, addr = tcpsock.accept()
    while True:
        data = conn.recv(1024)
        if not data: break
        print '[%s] Server got %s at TCP: %s' % (gettime(), data, port)
        conn.send("Congratulations! You found the hidden")
    conn.close()
    print "[%s] Port knocking successful ... " % gettime()


def clients_are_the_same(clients_list):
    return clients_list[0] == clients_list[1] == clients_list[2]


def run(host, tcpport):
    i = 0
    clients_list = []

    for udpsock in udpsockets:
        try:
            ready = select.select([udpsock], [], [], 5)
            if ready[0]:
                data, client = udpsock.recvfrom(100)
                if not data: continue
                if data == 'PING':
                    print '[%s] Server got PING ... ' % gettime()
                    udpsock.sendto('PONG', client)
                    clients_list.append(client)
                    i += 1
        except socket.timeout, e:
            err = e.args[0]
            if err == 'timed out':
                time.sleep(1)
                clients_list[:] = []
                continue
            else:
                clients_list[:] = []
        except socket.error, e:
            clients_list[:] = []
            break

    if i == 3:
        if clients_are_the_same(clients_list):
            open_tcp_port(host, tcpport)


if __name__ == '__main__':

    udpsockets = set_up_udp_ports(HOST, UDP_PORTS)
    print "[%s] Server started...UDP port sequence: %s, TCP port to open: %s ... \n" % (gettime(), UDP_PORTS, TCP_PORT)

    while True:
        run(HOST, TCP_PORT)

    for udpsock in udpsockets:
        udpsock.close()
