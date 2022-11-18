"""
Author      :   Jackey Weng
Student ID  :   40130001
User-ids:   ?
Description :   his file is the client that will request the inputs from the user
"""

from socket import *
import sys
import os
from enum import Enum
import json
from model.Request import *
from pathlib import Path

# Create a collection of actions to do
# Action.get(operation, default)


class Operation(Enum):
    PUT = 0b000
    GET = 0b001
    CHANGE = 0b010
    HELP = 0b011
    BYE = 0b100
    ERROR = 0B101


def Get_user_command(command):
    opcode = Operation.ERROR
    while opcode == Operation.ERROR:
        match command:
            case Operation.PUT.name:
                opcode = Operation.PUT
            case Operation.GET.name:
                opcode = Operation.GET
            case Operation.CHANGE.name:
                opcode = Operation.CHANGE
            case Operation.HELP.name:
                opcode = Operation.HELP
            case Operation.BYE.name:
                opcode = Operation.BYE
            case _:
                opcode = Operation.ERROR
                print(
                    f'"{command}" operation does not exit. Try again or type "help".\n')
                array = input('request: ').split()
                command = array[0].upper()
    return opcode


# -------------------------------------------------------
# Get IP address and port number from arguments
# serverName = str(sys.argv[1])
# serverPort = int(sys.argv[2])
serverName = '127.0.0.1'
serverPort = 80

# SOCK_STREAM: a TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# initiates the TCP connection between the client and server
clientSocket.connect((serverName, serverPort))
print('Session has been established')
# -------------------------------------------------------

opcode = None
print("+---------------------+")
print("|File Transfer Service|")
print("+---------------------+")

# -------------------------------------------------------
while opcode != Operation.BYE:
    sentence = input('Request: ').split()
    opcode = Get_user_command(sentence[0].upper())

    match opcode:
        case Operation.PUT:
            try:
                #
                filename_length = len(sentence[1]) + 1

                # Get file size
                path = os.path.join(os.path.dirname(
                    __file__), 'ClientFolder', sentence[1])
                file_size = os.path.getsize(path)

                request = Put(opcode.value, filename_length,
                              sentence[1], file_size)

                # Open file in read byte mode
                file = open(path, "rb")

                # Convert the sentence to byte into the TCP connection
                request_serialized = json.dumps(request.dictionary(), indent=4)
                clientSocket.sendto(request_serialized.encode(),
                                    (serverName, serverPort))
                data = file.read()
                clientSocket.sendall(data)
                #
                file.close()
                print("REQUEST MESSAGE")
                response = clientSocket.recv(1024).decode()
                print(response)

                print(request, '\n')
            except:
                opcode = Operation.ERROR
                print(
                    f'Oops, something went wrong when retrieving the file "{sentence[1]}"')

        case Operation.GET:
            filename_length = len(sentence[1]) + 1
            request = Get(opcode.value, filename_length,
                          sentence[1])
            # Convert the sentence to byte into the TCP connection
            request_serialized = json.dumps(request.dictionary(), indent=4)
            clientSocket.sendto(request_serialized.encode(),
                                (serverName, serverPort))

            path = os.path.join(os.path.dirname(
                __file__), 'ClientFolder', sentence[1])
            # open a file in write byte mode
            file = open(path, "wb")
            file_bytes = b""
            size_count = 0

            print('Downloading...')
            download_size = clientSocket.recv(1024).decode()
            while size_count < int(download_size):
                data = clientSocket.recv(4096)
                file_bytes += data
                size_count += 4096
            print("size: ", size_count)
            file.write(file_bytes)
            file.close()
            print("downloaded successfully")

        case Operation.CHANGE:
            old_filename_length = len(sentence[1]) + 1
            new_filename_length = len(sentence[2]) + 1
            request = Change(opcode.value, old_filename_length,
                             sentence[1], new_filename_length, sentence[2])
            request_serialized = json.dumps(request.dictionary(), indent=4)
            clientSocket.sendto(request_serialized.encode(),
                                (serverName, serverPort))
            response = clientSocket.recv(1024).decode()
            print(response)

        case Operation.HELP:
            request = Help(opcode.value)
            # Convert the sentence to byte into the TCP connection
            request_serialized = json.dumps(request.dictionary(), indent=4)
            clientSocket.sendto(request_serialized.encode(),
                                (serverName, serverPort))

            response = clientSocket.recv(1024).decode()
            print(response)
        case Operation.BYE:
            request = Bye(opcode.value)
            # Convert the sentence to byte into the TCP connection
            request_serialized = json.dumps(request.dictionary(), indent=4)
            clientSocket.sendto(request_serialized.encode(),
                                (serverName, serverPort))
        case _:
            print(
                f'"{sentence[0]}" operation does not exit. Try again or type "help".\n')
    # new line
    print()


# Closes the socket and the TCP connection
clientSocket.close()
print("Session terminated \n")
