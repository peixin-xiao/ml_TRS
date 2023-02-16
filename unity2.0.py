import os  
import numpy as np
import struct
import matplotlib.pyplot as plt
import gc
import random
import socket
import time
import threading
import asyncio

class readpath(object):
    
    def __init__(self,N):
        self.N = N
        return None
    
    def generate_path(self):
        dict1 = {0:'.\data\\path_slab.dat',1:'C:\\Users\\Administrator\\source\\data\\path_kiwi_hard2.dat'
                ,2:'C:\\Users\\Administrator\\source\\data\\path_kiwi_soft3.dat',3:'C:\\Users\\Administrator\\source\\data\\path090_3.dat'
                ,4:'C:\\Users\\Administrator\\source\\data\\path117_3.dat',5:'C:\\Users\\Administrator\\source\\data\\path138_3.dat'
                ,6:'C:\\Users\\Administrator\\source\\data\\path156_3.dat',7:'C:\\Users\\Administrator\\source\\data\\path175_3.dat'}
        self.dict1 = dict1
        return dict1
    
    def read0(self,i):
        q = 0
        with open(self.dict1[i], "rb") as file0:
            data1 = file0.read(4)
            I = struct.unpack("i", data1)[0]
            data1 = file0.read(4)
            J = struct.unpack("i", data1)[0]
            data1 = file0.read(4)
            K = struct.unpack("i", data1)[0]
            h = []
            for i in range(I):
                a = []
                for j in range(J):
                    l = []
                    while(1):
                        data1 = file0.read(4)
                        f = struct.unpack("4s",data1)[0]
                        if (f!=b'end\x00'):
                            f = struct.unpack("f",data1)[0]
                            l.append(f)
                        else:
                            break
                    
                        

                    a.append(l)
                h.append(a)
                
        return I, h
    
    def read1(self):
        self.generate_path()
        h = [None]*self.N
        I = np.zeros((self.N,))
        for i in range(0,self.N):
            I[i],h[i] = self.read0(i)
            
        self.h = h
        self.I = I
        return h,I
    



def analysis(h,I,indexout):
    eye = [0.0225,0.015,0.015]
    #normal line vector (0.707,0.707,0)
    #euqation of surface : x+y=0.09
    N=200
    time = np.linspace(0, 2e-9, num=N)
    time_per_cell = 2e-9/N
    weight = np.zeros((N,))
    temp = pow(2,0.5)
    radius_fiber = 0.004
    threshold = 0.004
    for j in indexout[1:int(indexout[0])]:
        i=int(j)
        for k in range(len(h[i][0])):
            
            if((pow(h[i][0][k]-eye[0],2)+pow(h[i][1][k]-eye[1],2)
               +pow(h[i][2][k]-eye[2],2) < pow(radius_fiber,2)) and 
               ((h[i][0][k]-eye[0])<threshold)and((h[i][0][k]-eye[0])>0)):
                
                t = int(h[i][4][k]/time_per_cell)
                if(t<200):
                    weight[t]=weight[t]+h[i][3][k]
                else:
                    weight[0]=-114514
                break;

    return weight

def analysis_g(N, h, I,indexout):
    w2 = np.zeros((N,200))
    for i in range(0,N):
        w2[i] = analysis(h[i],I[i],indexout[:,i])

    return w2
def give_signal():
    N = 1
    s1 = readpath(N)
    h,I = s1.read1()
    

    indexout = np.zeros((5001,N))
    for n in range(N):
        j = 0
        for i in range(int(I[0])):
            if(len(h[n][i][0])!=0):
                if(max(h[n][i][0])>0.0225):
                    indexout[j+1,n] = i
                    j = j+1
        indexout[0,n]=j
    
    ########################################################################
    w2 = analysis_g(N,h,I,indexout)
    return w2
    #####################################################################

    # M=200
    # time = np.linspace(0, 2e-9, num=M)
    # plt.figure(figsize = (10,10))
    # for i in range(N):
    #     plt.subplot(3,3,i+1)
    #     plt.plot(time,w2[i])

    # plt.xlabel('time/s')
    # plt.ylabel('amount of photons')
    # plt.show()


async def run_executable(cmd):
    process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    return process

async def communicate_with_executable(data):
    # Connect to the executable
    reader, writer = await asyncio.open_connection('localhost', 12345)
    
    # Prepare the data to send
    data = struct.pack('<4f', *data)
    # Send the data
    writer.write(data)
    await writer.drain()
    
    # Receive the response
    response = await reader.read(16)
    
    # Unpack the response
    response = struct.unpack('<4f', response)
    
    # Close the connection
    writer.close()
    await writer.wait_closed()
    
    # Return the response
    return response

async def main(a):
    # Start the executable
    # process = await run_executable(['./model_generator_unity_slab0.0/x64/Debug/model_generator_slab.exe'])
    process = await run_executable(['.\model_gen_mc_slab\\x64\\Debug\\model_gen_mc_slab.exe'])
    # Communicate with the executable
    response = await communicate_with_executable(a)
    
    # Print the response
    print(response)
    
    # Wait for the process to finish
    await process.wait()

a = np.array([20e-3,0.1e2,140e2,0.85], dtype = np.float32)
# with open("C:\\Users\\Administrator\\source\\data\\para.bin", "wb") as file0:
#     for i in range(4):
#         file0.write(a[i])
os.chdir('D:\\files2\\Nagoya\\python\\kiwi_ToF_simulation\\slab_dataset_generator')
asyncio.run(main(a))

# main = ".\mc_slab_unity0.0\\x64\\Debug\\mc_slab_unity0.0.exe"
# main = ".\model_gen_mc_slab\\x64\\Debug\\model_gen_mc_slab.exe"
# r_v = os.system(main) 
# if(r_v!=0):
#     print (r_v )
print('finished')
plt.plot(give_signal()[0])
plt.show()