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

def dwld(file_name):
    # Download given file
    print("Downloading file: {}".format(file_name))
    try:
        # Send server request
        s.send("DWLD".encode())
    except:
        print("Couldn't make server request. Make sure a connection has bene established.")
        return
    try:
        # Wait for server ok, then make sure file exists
        s.recv(BUFFER_SIZE)
        # Send file name length, then name
        s.send(struct.pack("i", os.path.getsize(file_name)))
        s.send(file_name)
        # Get file size (if exists)
        file_size = struct.unpack("i", s.recv(4))[0]
        if file_size == -1:
            # If file size is -1, the file does not exist
            print("File does not exist. Make sure the name was entered correctly")
            return
    except:
        print("Error checking file")
    try:
        # Send ok to recieve file content
        s.send("1")
        # Enter loop to recieve file
        output_file = open(file_name, "wb")
        bytes_recieved = 0
        print("\nDownloading...")
        while bytes_recieved < file_size:
            # Again, file broken into chunks defined by the BUFFER_SIZE variable
            l = s.recv(BUFFER_SIZE)
            output_file.write(l)
            bytes_recieved += BUFFER_SIZE
        output_file.close()
        print("Successfully downloaded {}".format(file_name))
        # Tell the server that the client is ready to recieve the download performance details
        s.send("1")
        # Get performance details
        time_elapsed = struct.unpack("f", s.recv(4))[0]
        print("Time elapsed: {}s\nFile size: {}b".format(time_elapsed, file_size))
    except:
        print("Error downloading file")
        return
    return
def upld():

    file_name = input("\nEnter file name: ")
    print("uploading file: {}...".format(file_name))

    try:
        file = open(file_name, "rb")
    except:
        print("couldn´t find the file")
        return
    try:
        s.send("UPLD".encode())
        #print(s.recv(BUFFER_SIZE).decode('utf-8', 'ignore'))
    except:
        print("couldnt make server request")
        return


    try:
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", len(file_name.encode())))
        s.send(file_name.encode())
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("i", os.path.getsize(file_name)))
    except:
        print("Error sending file details")
    try:
        l = file.read(BUFFER_SIZE)
        print("\nSending...")
        while l:
            s.send(l)
            l = file.read(BUFFER_SIZE)
        file.close()
        upload_time = struct.unpack("f", s.recv(4))[0]
        upload_size = struct.unpack("i", s.recv(4))[0]
        print(")\nSent file: {}\nTime elapsed: {}s\nFile size: {}b".format(file_name, upload_time, upload_size))
    except:
        print("Error sending file")
        return
    return

print("\n\nWelcome to the FTP client.")
conn()
while True:
    # Listen for a command
    prompt = input("\nEnter a command: ")
    if prompt[:4].upper() != "QUIT":
        if prompt[:4].upper() == "UPLD":

            upld()
        elif prompt[:4].upper() == "DWLD":
            filedwld = input("\nEnter the name of the file to download: ")
            filedwld = filedwld.encode()
            #print(s.recv(BUFFER_SIZE).decode('utf-8', 'ignore'))
            dwld(filedwld)
    prompt = None

