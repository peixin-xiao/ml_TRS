import socket
import time
import struct
def sever_send(li):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 8888))
    server.listen(0)
    connection, address = server.accept()
    # print(connection, address)
    connection.send(len(li).to_bytes(4,'big'))  ## 4: sizeof(int)
    for i in range(len(li)):
    # val = struct.pack('c', li)
    # connection.send(bytes(str(li), encoding='utf-8'))
        connection.send(li[i].to_bytes(4,'big'))
    time.sleep( 0.5 )

    connection.close()
    # input("enter end") 

li = [0,1,2,3,4]
sever_send(li)
