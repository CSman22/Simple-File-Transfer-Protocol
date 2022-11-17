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
from model.Put import *
from model.Bye import *


class Operation(Enum):
    PUT = 0b000
    GET = 0b001
    CHANGE = 0b010
    HELP = 0b011
    BYE = 0b100
    ERROR = 0B101


def Get_File(filename):
    # open file in read byte mode
    file = open(filename, "rb")
    file_size = os.path.getsize(filename)


def Get_user_command(command):
    opcode = Operation.ERROR
    while opcode == Operation.ERROR:
        print(command)
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
# # Get IP address and port number from arguments
# # serverName = str(sys.argv[1])
# # serverPort = int(sys.argv[2])
# serverName = '127.0.0.1'
# serverPort = 80

# # SOCK_STREAM: a TCP socket
# clientSocket = socket(AF_INET, SOCK_STREAM)

# # initiates the TCP connection between the client and server
# clientSocket.connect((serverName, serverPort))
# print('Session has been established')
# -------------------------------------------------------

opcode = None
print("+---------------------+")
print("|File Transfer Service|")
print("+---------------------+")

# -------------------------------------------------------
while opcode != Operation.BYE:
    request = None
    request = None
    sentence = input('request: ').split()
    opcode = Get_user_command(sentence[0].upper())

    match opcode:
        case Operation.PUT:
            print("PUT")
            filename_length = len(sentence[1]) + 1
            request = Put(opcode.value, filename_length, sentence[1], '')
        case Operation.GET:
            print("GET")
            filename_length = len(sentence[1]) + 1
        case Operation.CHANGE:
            print("CHANGE")
            old_filename_length = len(sentence[1] + 1)
        case Operation.HELP:
            print("HELP")
        case Operation.BYE:
            print("BYE")
            request = Bye(opcode.value)
        case _:
            print("ERROR")
            print(
                f'"{sentence[0]}" operation does not exit. Try again or type "help".\n')

    # # check if the user made a request
    # if request != None:
    #     request_serialized = json.dumps(request.dictionary(), indent=4)

    #     # -------------------------------------------------------
    #     # Convert the sentence to byte into the TCP connection
    #     clientSocket.sendto(request_serialized.encode(),
    #                         (serverName, serverPort))

    #     # open file in read byte mode
    #     file = open("pic.jpg", "rb")
    #     file_size = os.path.getsize(request.filename)

    #     data = file.read()
    #     clientSocket.sendall(data)
    #     clientSocket.send(b"<END>")

    #     file.close()
    #     print("finished sending pic")

    #     # Arrival of bytes from the server
    #     modifiedSentence = clientSocket.recv(1024)
    #     print("From Server: ", modifiedSentence.decode())

    # new line
    print()


# # Closes the socket and the TCP connection
# clientSocket.close()
# print("Session terminated")
