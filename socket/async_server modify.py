import asyncio
import struct

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

async def main():
    # Start the executable
    # process = await run_executable(['D:\\files2\\Nagoya\\python\\kiwi_ToF_simulation\\slab_dataset_generator\\gpt_client\\x64\Debug\\gpt_client.exe'])
    process = await run_executable(['D:\\files2\\Nagoya\\python\\kiwi_ToF_simulation\\slab_dataset_generator\\model_generator_unity_slab0.0\\x64\\Debug\\model_generator_slab.exe'])
    # Communicate with the executable
    response = await communicate_with_executable([1.1, 2.2, 3.3, 4.5])
    
    # Print the response
    print(response)
    
    # Wait for the process to finish
    await process.wait()

asyncio.run(main())


