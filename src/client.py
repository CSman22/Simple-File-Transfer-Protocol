"""
Author      :   Jackey Weng
Student ID  :   40130001
Description :   This file is the client that will request the inputs from the user
"""

from socket import *
import sys
import os
from enum import Enum
import json
from model.Request import *
from model.Response import *


class Operation(Enum):
    PUT = 0b000
    GET = 0b001
    CHANGE = 0b010
    HELP = 0b011
    BYE = 0b100
    ERROR = 0B101


class Res_Code(Enum):
    SUCCESS_PUT_CHANGE = 0b000
    SUCCESS_GET = 0b001
    ERROR_FILE_NOT_FOUND = 0b010
    ERROR_UNKNOWN_REQUEST = 0b011
    UNSUCCESSFUL_CHANGE = 0B101
    SERVER_HELP = 0B110


# Check if the the command entered corresponds to a instruction
def Get_user_command(command):
    operation = Operation.ERROR
    match command:
        case Operation.PUT.name:
            operation = Operation.PUT
        case Operation.GET.name:
            operation = Operation.GET
        case Operation.CHANGE.name:
            operation = Operation.CHANGE
        case Operation.HELP.name:
            operation = Operation.HELP
        case Operation.BYE.name:
            operation = Operation.BYE
        case _:
            operation = Operation.ERROR
    return operation


# Setup the TCP connection  by passing the server address and port number
def Setup_TCP_Connection(serverName, serverPort):
    # SOCK_STREAM: a TCP socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # initiates the TCP connection between the client and server
    clientSocket.connect((serverName, serverPort))
    print('Session has been established')
    return clientSocket


# Print statement if it is debug mode
def DPrint(message, isDebugger):
    if (isDebugger == 1):
        print(message)


# Get the size of the file by passing the folder name and filename
def Get_file_size(folder_name, filename):
    path = os.path.join(os.path.dirname(
        __file__), folder_name, filename)

    file_size = os.path.getsize(path)
    return file_size


# Download file from server
def Download_file(folder_name, response):
    path = os.path.join(os.path.dirname(
        __file__), folder_name, response.Filename)
    # open a file in write byte mode
    file = open(path, "wb")
    file_bytes = b""
    size_count = 0

    DPrint(f'Downloading...', debugMode)
    while size_count < response.File_size:
        data = clientSocket.recv(4096)
        file_bytes += data
        size_count += 4096
    file.write(file_bytes)
    file.close()


# Upload a file to the server folder
def Upload_to_server(folderName, filename):
    # Get file size
    path = os.path.join(os.path.dirname(
        __file__), folderName, filename)

    # Open file in read byte mode
    file = open(path, "rb")
    data = file.read()
    clientSocket.sendall(data)
    file.close()

    DPrint(f'Uploading...', debugMode)


opcode = None
print("+---------------------+")
print("|File Transfer Service|")
print("+---------------------+")

# Get IP address and port number from arguments
serverName = str(sys.argv[1])
serverPort = int(sys.argv[2])
debugMode = int(sys.argv[3])
# serverName = '127.0.0.1'
# serverPort = 80
# debugMode = 1
clientSocket = Setup_TCP_Connection('127.0.0.1', 80)

# -------------------------------------------------------
while opcode != Operation.BYE:
    sentence = input('Request: ').split()
    print()
    opcode = Get_user_command(sentence[0].upper())

    match opcode:
        # Handling PUT request
        case Operation.PUT:
            try:
                filename_length = len(sentence[1]) + 1

                if (filename_length > 31):
                    print(f"Error| Filename should not exceed 31 characters\n")
                    continue

                # Create request
                file_size = Get_file_size("ClientFolder", sentence[1])
                request = Put(opcode.value, filename_length,
                              sentence[1], file_size)
                DPrint(request, debugMode)

                # Convert the sentence to byte into the TCP connection
                request_serialized = json.dumps(request.dictionary(), indent=4)
                clientSocket.sendto(request_serialized.encode(),
                                    (serverName, serverPort))

                # Upload file
                Upload_to_server("ClientFolder", sentence[1])

                # Retrieve Response
                response = clientSocket.recv(1024).decode()
                response_obj = Response.deserialize(response)

                if response_obj.Response_code == Res_Code.SUCCESS_PUT_CHANGE.value:
                    print(f"{sentence[1]} has been uploaded successfully.\n")

            except:
                opcode = Operation.ERROR
                print(
                    f'\nOops, something went wrong when retrieving the file "{sentence[1]}"\n')

        # Handling GET request
        case Operation.GET:
            filename_length = len(sentence[1]) + 1

            if (filename_length > 31):
                print(f"Error| Filename should not exceed 31 characters\n")
                continue

            request = Get(opcode.value, filename_length,
                          sentence[1])
            DPrint(request, debugMode)
            # Convert the sentence to byte to be sent
            request_serialized = json.dumps(request.dictionary(), indent=4)
            clientSocket.sendto(request_serialized.encode(),
                                (serverName, serverPort))

            # Retrieve response
            response = clientSocket.recv(1024).decode()
            response_obj = Response.deserialize(response)

            if response_obj.Response_code == Res_Code.SUCCESS_GET.value:
                Download_file("ClientFolder", response_obj)
                print(f"{response_obj.Filename} has been downloaded successfully \n")
            if response_obj.Response_code == Res_Code.ERROR_FILE_NOT_FOUND.value:
                print(f"Error| File not found \n")

        # Handling CHANGE request
        case Operation.CHANGE:
            old_filename_length = len(sentence[1]) + 1
            if (old_filename_length > 31):
                print(f"Error| Old filename should not exceed 31 characters\n")
                continue
            new_filename_length = len(sentence[2]) + 1
            if (new_filename_length > 31):
                print(f"Error| New filename should not exceed 31 characters\n")
                continue

            # Create request
            request = Change(opcode.value, old_filename_length,
                             sentence[1], new_filename_length, sentence[2])
            DPrint(request, debugMode)
            # Convert the sentence to byte to be sent
            request_serialized = json.dumps(request.dictionary(), indent=4)
            clientSocket.sendto(request_serialized.encode(),
                                (serverName, serverPort))

            # Retrieve Response
            response = clientSocket.recv(1024).decode()
            response_obj = Response.deserialize(response)

            if response_obj.Response_code == Res_Code.SUCCESS_PUT_CHANGE.value:
                print(
                    f'"{sentence[1]}" has been changed into "{sentence[2]}".\n')
            if response_obj.Response_code == Res_Code.UNSUCCESSFUL_CHANGE.value:
                print(
                    f'Error| Unsuccessful change\n')

        # Handling HELP request
        case Operation.HELP:
            request = Help(opcode.value)
            DPrint(request, debugMode)
            # Convert the sentence to byte into the TCP connection
            request_serialized = json.dumps(request.dictionary(), indent=4)
            clientSocket.sendto(request_serialized.encode(),
                                (serverName, serverPort))

            response = clientSocket.recv(1024).decode()
            response_obj = Response.deserialize(response)
            print(response_obj, '\n')

        # Handling BYE request
        case Operation.BYE:
            request = Bye(opcode.value)
            # Convert the sentence to byte into the TCP connection
            request_serialized = json.dumps(request.dictionary(), indent=4)
            clientSocket.sendto(request_serialized.encode(),
                                (serverName, serverPort))

        # Handling ERROR request
        case _:
            opcode = Operation.ERROR
            # Create request
            request = Error(opcode.value)
            DPrint(request, debugMode)
            # Convert the sentence to byte into the TCP connection
            request_serialized = json.dumps(request.dictionary(), indent=4)
            clientSocket.sendto(request_serialized.encode(),
                                (serverName, serverPort))

            # Get response from server
            response = clientSocket.recv(1024).decode()
            response_obj = Response.deserialize(response)
            if response_obj.Response_code == Res_Code.ERROR_UNKNOWN_REQUEST.value:
                print(
                    f'"{sentence[0]}" operation does not exit. Try again or type "help".\n')


# Closes the socket and the TCP connection
clientSocket.close()
print("Session terminated \n")
