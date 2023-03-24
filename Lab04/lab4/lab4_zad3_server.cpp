#include <iostream>
#include <string>
#include <ctime>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <netdb.h>

#define BUFFER_SIZE 1024

int main()
{

    int server_fd, err;
    struct sockaddr_in server, client;
    char buf[BUFFER_SIZE];
    int port = 7777;

    // tworze gniazdo serwera
    server_fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (server_fd < 0)
    {
        std::cout << ("Could not create socket\n");
        perror("socket");
        return 1;
    }

    // adres i port serwera
    server.sin_family = AF_INET;
    server.sin_port = htons(port);
    server.sin_addr.s_addr = htonl(INADDR_ANY);

    // dowiazanie do danego portu
    err = bind(server_fd, (struct sockaddr *) &server, sizeof(server));
    if (err < 0)
    {
        std::cout << ("Could not bind socket\n");
        perror("socket");
        return 1;
    }

    std::cout << "Server is listening on port " << port << " ... \n";

    socklen_t clientlen = sizeof(client);

    while (1)
    {
        int read = recvfrom(server_fd, buf, BUFFER_SIZE, 0, (struct sockaddr *) &client, &clientlen);
        if (read < 0)
        {
            perror("recvfrom");
            return 1;
        }

        int write = sendto(server_fd, buf, std::string(buf).length(), 0, (struct sockaddr *) &client, clientlen);
        if (write < 0)
        {
            perror("sendto");
            return 1;
        }
    }

    close(server_fd);

    return 0;
}
