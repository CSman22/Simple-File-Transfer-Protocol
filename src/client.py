"""
Author      :   Jackey Weng
Student ID  :   40130001
User-ids:   ?
Description :   his file is the client that will request the inputs from the user
"""

from socket import *
import sys

serverName = str(sys.argv[1])
serverPort = int(sys.argv[2])
# serverName = '127.0.0.1'
# serverPort = 12000

# SOCK_STREAM: a TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# initiates the TCP connection between the client and server
clientSocket.connect((serverName, serverPort))
print('Session has been established')

sentence = input("Input lowercase sentence:")

# Convert the sentence to byte into the TCP connection
clientSocket.sendto(sentence.encode(), (serverName, serverPort))

# Arrival of bytes from the server
modifiedSentence = clientSocket.recv(1024)
print("From Server: ", modifiedSentence.decode())

# Closes the socket and the TCP connection
clientSocket.close()
