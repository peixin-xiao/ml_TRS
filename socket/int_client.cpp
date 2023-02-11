#include <stdio.h>  
#include <Winsock2.h>  
#pragma comment(lib,"ws2_32.lib")
#pragma warning(disable:4996)
#include <iostream>

int main()
{
	WORD wVersionRequested;
	WSADATA wsaData;
	int err;

	wVersionRequested = MAKEWORD(1, 1);

	/*err = WSAStartup(wVersionRequested, &wsaData);
	if (err != 0) {
		return -1;
	}

	if (LOBYTE(wsaData.wVersion) != 1 ||
		HIBYTE(wsaData.wVersion) != 1) {
		WSACleanup();
		return -1;
	}*/
	SOCKET sockClient = socket(AF_INET, SOCK_STREAM, 0);

	SOCKADDR_IN addrSrv;
	addrSrv.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
	addrSrv.sin_family = AF_INET;
	addrSrv.sin_port = htons(8888);
	connect(sockClient, (SOCKADDR*)&addrSrv, sizeof(SOCKADDR));

	char recvBuf[4];
	recv(sockClient, recvBuf, 4, 0);
	int length = int((unsigned char)(recvBuf[0]) << 24 |
		(unsigned char)(recvBuf[1]) << 16 |
		(unsigned char)(recvBuf[2]) << 8 |
		(unsigned char)(recvBuf[3]));

	int* k = (int*)malloc(sizeof(int) * length);
	for (int i = 0;i < length;i++) {
		recv(sockClient, recvBuf, 4, 0);
		k[i] = int((unsigned char)(recvBuf[0]) << 24 |
			(unsigned char)(recvBuf[1]) << 16 |
			(unsigned char)(recvBuf[2]) << 8 |
			(unsigned char)(recvBuf[3]));

	}
	for (int i = 0;i < length;i++) {
		printf("severRecv %d\n", k[i]);
	}




	closesocket(sockClient);
	WSACleanup();

	//getchar();
	return 0;
}