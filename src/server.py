"""
Author      :   Jackey Weng
Student ID  :   40130001
Description :   This file is the server that will handle the client request for
                file transfer
"""

from socket import *
import os
import json
import sys
from enum import Enum
from model.Request import *
from model.Response import *


class Operation(Enum):
    PUT = 0b000
    GET = 0b001
    CHANGE = 0b010
    HELP = 0b011
    BYE = 0b100
    ERROR = 0B101


def Can_filename_be_changed(old_name, new_name):
    if not os.path.isfile(old_name):
        return 'Error: Old file name cannot be found'
    if os.path.isfile(new_name):
        return 'Error: The new file name already exists'
    return None


def Does_filename_exist(folder_name, filename):
    file_path = os.path.join(os.path.dirname(
        __file__), folder_name, filename)

    if os.path.isfile(file_path):
        return True
    else:
        return False


# Print statement if it is debug mode
def DPrint(message, isDebugger):
    if (isDebugger == 1):
        print(message)


# Download file from client
def Download_client_file(folder_name, request):
    path = os.path.join(os.path.dirname(
        __file__), folder_name, request.filename)
    # open a file in write byte mode
    file = open(path, "wb")
    file_bytes = b""
    size_count = 0

    DPrint("Downloading...", debugMode)

    while size_count < request.file_size:
        data = connectionSocket.recv(4096)
        file_bytes += data
        size_count += 4096
    file.write(file_bytes)
    file.close()


# Upload file to client
def Upload_to_client(folder_name, request):
    path = os.path.join(os.path.dirname(
        __file__), folder_name, request.filename)

    file_size = os.path.getsize(path)
    # Open file in read byte mode
    file = open(path, "rb")
    data = file.read()

    DPrint(f"Sending {request.filename}...", debugMode)
    DPrint(f"File Size: {file_size} Bytes", debugMode)
    connectionSocket.sendall(data)
    #
    file.close()


def Get_file_size(folder_name, filename):
    path = os.path.join(os.path.dirname(
        __file__), folder_name, filename)

    file_size = os.path.getsize(path)
    return file_size


# -------------------------------------------------------
# Get IP address and port number from arguments
serverName = str(sys.argv[1])
serverPort = int(sys.argv[2])
debugMode = int(sys.argv[3])
# serverPort = 80
# serverName = '127.0.0.1'
# debugMode = 1
serverSocket = socket(AF_INET, SOCK_STREAM)
# Binds port number 12000 to the server’s socket
serverSocket.bind((serverName, serverPort))

# wait and listen for some client to knock on the door
# 1: the max number of queued connection
serverSocket.listen(1)
print("+-----------+")
print("|File Server|")
print("+-----------+")
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

        match req_dict['opcode']:
            # Handling PUT response
            case Operation.PUT.value:
                opcode = Operation.PUT
                put_request = Put.deserialize(request)

                # download client file
                Download_client_file("ServerFolder", put_request)

                # Create a response
                response = Response(0b000)
                DPrint(response, debugMode)
                res_serialized = json.dumps(
                    response.dictionary(), indent=4)
                connectionSocket.sendto(res_serialized.encode(),  addr)
                print(f'Response sent\n')

            # Handling GET response
            case Operation.GET.value:
                opcode = Operation.GET
                get_request = Get.deserialize(request)

                isFilename = Does_filename_exist(
                    "ServerFolder", get_request.filename)

                response = None
                if (isFilename):
                    file_size = Get_file_size(
                        "ServerFolder", get_request.filename)

                    # Create success response
                    response = Response(
                        0b001, get_request.filename_length, get_request.filename, file_size)
                    DPrint(response, debugMode)
                    res_serialized = json.dumps(
                        response.dictionary(), indent=4)
                    connectionSocket.sendto(res_serialized.encode(),  addr)

                    # Upload file to clientSocket
                    Upload_to_client("ServerFolder", get_request)
                else:
                    # Create Error response
                    response = Response(0b010)
                    res_serialized = json.dumps(
                        response.dictionary(), indent=4)
                    connectionSocket.sendto(res_serialized.encode(),  addr)
                print(f'Response sent\n')

            # Handling CHANGE response
            case Operation.CHANGE.value:
                opcode = Operation.CHANGE
                change_request = Change.deserialize(request)
                old_file_path = os.path.join(os.path.dirname(
                    __file__), 'ServerFolder', change_request.old_filename)
                new_file_path = os.path.join(os.path.dirname(
                    __file__), 'ServerFolder', change_request.new_filename)

                can_file_change = Can_filename_be_changed(
                    old_file_path, new_file_path)

                # check if filename be changed
                if (can_file_change is None):
                    # rename
                    os.rename(old_file_path, new_file_path)
                    # Create a response
                    response = Response(0b000)
                    res_serialized = json.dumps(
                        response.dictionary(), indent=4)
                else:
                    # Create a error response
                    print(can_file_change)
                    response = Response(0b101)
                    res_serialized = json.dumps(
                        response.dictionary(), indent=4)

                connectionSocket.sendto(res_serialized.encode(),  addr)
                DPrint(response, debugMode)
                print(f"Response Sent\n")

            # Handling HELP response
            case Operation.HELP.value:
                opcode = Operation.HELP
                sentence = f'Commands are: \n'\
                    f'  put\t\tUpload file \n'\
                    f'  get\t\tDownload file \n'\
                    f'  change\tChange file name\n'\
                    f'  help\t\tList all the commands\n'\
                    f'  bye\t\tClose connection'
                response = Response(0b110, Help_length=len(
                    sentence), Help_msg=sentence, Debug_mode=debugMode)
                res_serialized = json.dumps(
                    response.dictionary(), indent=4)
                connectionSocket.sendto(
                    res_serialized.encode(),  addr)
                print(f"Response Sent\n")

            # Handling BYE response
            case Operation.BYE.value:
                opcode = Operation.BYE

            # Handling ERROR response
            case _:
                # Create error unknown request
                response = Response(0b011)
                DPrint(response, debugMode)
                res_serialized = json.dumps(
                    response.dictionary(), indent=4)
                connectionSocket.sendto(res_serialized.encode(),  addr)
                print("operation does not exist")

    # Close connection BUT since serverSocket is open another client can knock
    connectionSocket.close()
    print(f'\nConnection closed')
