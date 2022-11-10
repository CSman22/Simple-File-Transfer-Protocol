"""
Author      :   Jackey Weng
Student ID  :   40130001
User-ids:   ?
Description :   his file is the server that will handle the client request for
                file transfer
"""

from socket import *

# -------------------------------------------------------
serverPort = 80
serverName = '127.0.0.1'
serverSocket = socket(AF_INET, SOCK_STREAM)
# Binds port number 12000 to the server’s socket
serverSocket.bind((serverName, serverPort))

# wait and listen for some client to knock on the door
# 1: the max number of queued connection
serverSocket.listen(1)
print("The server is ready to receive")
# -------------------------------------------------------

while True:
    # .accept: creates a new socket in the server
    # connection socket: the new socket for that user.
    # Handshaking now complete
    connectionSocket, addr = serverSocket.accept()
    print(f'\nconnection established')

    # Retrieve the message and capitalize to return back
    sentence = connectionSocket.recv(1024).decode()
    print(f'Request received')

    capitalizedSentence = sentence.upper()
    connectionSocket.sendto(capitalizedSentence.encode(), addr)
    print(f'Response sent')

    # Close connection BUT since serverSocket is open another client can knock
    connectionSocket.close()
    print(f'Connection closed\n')
