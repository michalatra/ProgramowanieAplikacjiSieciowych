#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    char * ip_addr;
    int port;

    int sockfd;
    struct sockaddr_in server_addr;

    /*
    if (argc != 3)
    {
        fprintf(stderr,"Usage: %s IP port \n", argv[0]);
        exit(1);
    }

    ip_addr = argv[1];
    port = atoi(argv[2]);

    if (port <= 0)
    {
        fprintf(stderr,"error: invalid port\n");
        exit(1);
    }*/

    ip_addr = "212.182.24.27";
    port = 22;

    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("socket");
        exit(1);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    inet_aton(ip_addr, &server_addr.sin_addr);

    if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(struct sockaddr)) == -1)
    {
        perror("connect");
        printf("Port %d is closed on server %s.\n", port, ip_addr);
        close(sockfd);
        exit(1);
    }

    char msg[] = "Just a text\n";
    char buffer[255];
    int recv_size, send_size;

    if ((send_size = send(sockfd, msg, strlen(msg), 0)) < 0)
    {
        close(sockfd);
        if (errno != 0)
        {
            perror("send");
            exit(1);
        }
    }

    if ((recv_size = recv(sockfd, buffer, 255, 0)) == 0)
    {
        close(sockfd);
        if (errno != 0)
        {
            perror("recv");
            exit(1);
        }
    }

    buffer[recv_size] = '\0';

    printf( "%-*s%-*s%-*s\n", 10, "PORT", 10, "STATE", 15, "SERVICE");
    printf( "%-*d%-*s%-*s\n", 10, port, 10, "tcp/open", 15, buffer);

    return 0;
}
