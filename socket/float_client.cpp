#include <stdio.h>  
#include <Winsock2.h>  
#pragma comment(lib,"ws2_32.lib")
#pragma warning(disable:4996)
#include <iostream>

std::tuple<float*,int> client(float*k)
{
	WORD wVersionRequested;
	WSADATA wsaData;
	int err;

	wVersionRequested = MAKEWORD(1, 1);

	err = WSAStartup(wVersionRequested, &wsaData);
	if (err != 0) {
		return std::make_tuple(nullptr,-1);
	}

	if (LOBYTE(wsaData.wVersion) != 1 ||
		HIBYTE(wsaData.wVersion) != 1) {
		WSACleanup();
		return std::tuple(nullptr,-1);
	}
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

	char rec[8];
	float f;
	//float* k = (float*)malloc(sizeof(float) * length);
	k = (float*)malloc(sizeof(float) * length);
	for (int i = 0;i < length;i++) {
		recv(sockClient, rec, 8, 0);
		memcpy(&f, &rec, sizeof(f));
		k[i] = f;
	}
	




	closesocket(sockClient);
	WSACleanup();

	//getchar();
	return std::make_tuple(k,length);
}

int main() {
	float* k=NULL;
	int length;
	std::tie( k,length) = client(k);
	for (int i = 0;i <length ;i++) {
		printf("severRecv %f\n", k[i]);
	}
}