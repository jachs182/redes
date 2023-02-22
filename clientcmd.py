import socket
import os
import struct

# Initialise socket stuff
TCP_IP = "127.0.0.1" # Only a local server
TCP_PORT = 1456 # Just a random choice
BUFFER_SIZE = 1024 # Standard chioce
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conn():
    # Connect to the server
    print("Sending server request...")
    try:
        s.connect((TCP_IP, TCP_PORT))
        print("Connection sucessful")
    except:
        print("Connection unsucessful. Make sure the server is online.")


def quit():
    s.send("QUIT".encode())
    # Wait for server go-ahead
    s.recv(BUFFER_SIZE)
    s.close()
    print("Server connection ended")
    return

def upld():

    file_name = input("\nEnter file name: ")
    file = open(file_name, "rb")
    file_size = os.path.getsize(file_name)
    new_name = input("\nEnter file new name: ")
    s.send(new_name.encode())
    s.send(str(file_size).encode())
    data = file.read(file_size)
    s.sendall(data)
    s.send(b"<END>")
    print("aqui")
    file.close()
    return

print("\n\nWelcome to the FTP client.")
conn()
while True:
    # Listen for a command
    print("reingreso")
    prompt = input("\nEnter a command: ")
    if prompt[:4].upper() == "QUIT":
        quit()
        break
    s.send(prompt.upper().encode())
    if prompt[:4].upper() == "UPLD":
        # Wait for server response
        print(s.recv(BUFFER_SIZE).decode('utf-8', 'ignore'))
        upld()
    elif prompt[:4].upper() == "LIST":
        print(s.recv(BUFFER_SIZE).decode('utf-8', 'ignore'))
    elif prompt[:4].upper() == "DWLD":
        print(s.recv(BUFFER_SIZE).decode('utf-8', 'ignore'))
    elif prompt[:4].upper() == "DELF":
        print(s.recv(BUFFER_SIZE).decode('utf-8', 'ignore'))
    prompt = None

