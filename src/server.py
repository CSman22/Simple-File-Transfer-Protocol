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
from model.Request import *


class Operation(Enum):
    PUT = 0b000
    GET = 0b001
    CHANGE = 0b010
    HELP = 0b011
    BYE = 0b100
    ERROR = 0B101


def Does_file_exist(old_name, new_name):
    if not os.path.isfile(old_name):
        return 'Error: Old file name does not exist'
    if os.path.isfile(new_name):
        return 'Error: The new file name already exists'
    return None


# -------------------------------------------------------
serverPort = 80
serverName = '127.0.0.1'
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
            case Operation.PUT.value:
                opcode = Operation.PUT
                put_request = Put.deserialize(request)

                path = os.path.join(os.path.dirname(
                    __file__), 'ServerFolder', put_request.filename)
                # open a file in write byte mode
                file = open(path, "wb")
                file_bytes = b""
                size_count = 0

                print('Downloading...')

                while size_count < put_request.file_size:
                    data = connectionSocket.recv(4096)
                    file_bytes += data
                    size_count += 4096
                print("size: ", size_count)
                file.write(file_bytes)
                file.close()

                sentence = f"{put_request.filename} has been uploaded successfully."
                connectionSocket.sendto(sentence.encode(), addr)
                print(f'Response sent\n')
            case Operation.GET.value:
                opcode = Operation.GET
                get_request = Get.deserialize(request)

                path = os.path.join(os.path.dirname(
                    __file__), 'ServerFolder', get_request.filename)
                file_size = os.path.getsize(path)
                # Open file in read byte mode
                file = open(path, "rb")

                connectionSocket.sendto(str(file_size).encode(),
                                        (serverName, serverPort))
                data = file.read()
                connectionSocket.sendall(data)
                #
                file.close()

            case Operation.CHANGE.value:
                opcode = Operation.CHANGE
                change_request = Change.deserialize(request)
                old_name = os.path.join(os.path.dirname(
                    __file__), 'ServerFolder', change_request.old_filename)
                new_name = os.path.join(os.path.dirname(
                    __file__), 'ServerFolder', change_request.new_filename)

                response = Does_file_exist(old_name, new_name)
                # Rename the file
                if (response is None):
                    os.rename(old_name, new_name)
                    response = 'Filename successfully changed'
                connectionSocket.sendto(
                    response.encode(), (serverName, serverPort))

            case Operation.HELP.value:
                opcode = Operation.HELP
                sentence = f'Commands are \n'\
                    f'  put\t\tUpload file \n'\
                    f'  get\t\tDownload file \n'\
                    f'  change\tChange file name\n'\
                    f'  help\t\tList all the commands\n'\
                    f'  bye\t\tClose connection'
                connectionSocket.sendto(sentence.encode(), addr)
            case Operation.BYE.value:
                opcode = Operation.BYE

    # Close connection BUT since serverSocket is open another client can knock
    connectionSocket.close()
    print(f'\nConnection closed')
