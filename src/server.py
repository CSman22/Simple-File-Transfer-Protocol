"""
Author      :   Jackey Weng
Student ID  :   40130001
User-ids:   ?
Description :   his file is the server that will handle the client request for
                file transfer
"""

from socket import *
import os
import json
from enum import Enum
from model.Put import *
# import tqdm


class Operation(Enum):
    PUT = 0b000
    GET = 0b001
    CHANGE = 0b010
    HELP = 0b011
    BYE = 0b100
    ERROR = 0B101


# -------------------------------------------------------
serverPort = 80
serverName = '127.0.0.1'
serverSocket = socket(AF_INET, SOCK_STREAM)
# Binds port number 12000 to the server’s socket
serverSocket.bind((serverName, serverPort))

# wait and listen for some client to knock on the door
# 1: the max number of queued connection
serverSocket.listen(1)
print("+--------------------+")
print("|File Transfer Server|")
print("+--------------------+")
print("The server is ready to receive.")
# -------------------------------------------------------

while True:
    print("--------------------------------")
    # .accept: creates a new socket in the server
    # connection socket: the new socket for that user.
    # Handshaking now complete
    connectionSocket, addr = serverSocket.accept()
    print(f'connection established\n')

    opcode = None
    request = None

    while opcode != Operation.BYE:
        # Retrieve the message
        request = connectionSocket.recv(1024).decode()

        print(f'Request received')
        req_dict = json.loads(request)

        if req_dict['opcode'] == Operation.PUT.value:
            print("PUT operation")
            opcode = Operation.PUT
            print(req_dict)

            # open a file in write byte mode
            file = open("pic2.jpg", "wb")
            file_bytes = b""
            done = False
            while not done:
                data = connectionSocket.recv(1024)
                if data[-5:] == b"<END>":
                    print(data)
                    done = True
                else:
                    file_bytes += data
            file.write(file_bytes)
            file.close()
        else:
            opcode = Operation.BYE

        sentence = "SERVER DONE"
        connectionSocket.sendto(sentence.encode(), addr)
        print(f'Response sent\n')

    # Close connection BUT since serverSocket is open another client can knock
    connectionSocket.close()
    print(f'Connection closed')
