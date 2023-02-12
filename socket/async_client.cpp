#include <winsock.h>
#include <iostream>

int main() {
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);
    
    SOCKET server_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    sockaddr_in server_address;
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);
    server_address.sin_port = htons(12345);
    bind(server_socket, (sockaddr*) &server_address, sizeof(server_address));
    listen(server_socket, 1);
    
    SOCKET client_socket = accept(server_socket, nullptr, nullptr);
    
    int data[5];
    recv(client_socket, (char*) &data, sizeof(data), 0);
    
    std::cout << "Received data: ";
    for (int i = 0; i < 5; i++) {
        std::cout << data[i] << " ";
    }
    std::cout << std::endl;
    
    int response[5] = {2 * data[0], 2 * data[1], 2 * data[2], 2 * data[3], 2 * data[4]};
    send(client_socket, (char*) &response, sizeof(response), 0);
    
    closesocket(client_socket);
    WSACleanup();
    
    return 0;
}
