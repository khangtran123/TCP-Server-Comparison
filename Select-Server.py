#!/bin/python3
'''
File: client.py
Date: February 18, 2018
Designers: Huu Khang Tran, Anderson Phan
File location: C:/xampp/htdocs/acit4850lab04/ePoll-Server.py
Description: This scripts covers a select (level-triggered) multiplexed server.
             Utilizes the select and poll functions
1. start with non-blocking I/O for sockets
2. Then get into multiplexing
'''

import socket
import select
import sys

#declaring these as global variables so it can be accessed in another function
global output_file
#global recvMsg
#global sentMsg


# s = socket created, opened, and initialized for when a client connects
# clientConnection = how many client sessions connect to this server
# recvMsg = total amount of data received from the client
# sentMsg = total amount of data sent back to the client
def kill_server(input, clientConnection, recvMsg, sentMsg, output_file):

    output_file.write("\n Total connections: " + str(clientConnection))
    output_file.write("\n Total amount of data received from the client" + str(recvMsg))
    output_file.write("\n Total amount of data sent to the client" + str(sentMsg))
    print ("\n Total connections: " + str(clientConnection))
    print ("\n Total amount of data received from the client: " + str(recvMsg))
    print ("\n Total amount of data sent to the client: " + str(sentMsg))
    #for x in input:
        #  now we have to close/end the session if the server was to be terminated
    input.close()
    print ("The client socket session is now closed.")
    #  to avoid getting a SystemExit exception which can be viewed as an error,
    #  we use sys.exit() to get around it
    sys.exit()

def main():

    #startTime = time.ctime(time.time())
    #start = time.time()
    # clientConnection is a list to keep track of all the clients who connect to this server
    clientConnection = 0
    recvMsg = 0
    sentMsg = 0

    output_file = open('Select_Server-Output.txt','w')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'
    port = 7005
    s.bind((host,port))

    print ("Server Started")

    #listens up to 50 connections/clients
    s.listen(socket.SOMAXCONN)

    # now we want to set the server connections to a non blocking I/O mode
    # 0 means setting the flag to false in which turns blocking I/O off
    # 1 means setting the flag to true in which turns blocking I/O on
    s.setblocking(0)
    #  sys.sdin is anything coming in from the client to be considered part of
    #  socket standard input stack
    input = [s, ]

    try:
        while True:
            readSockets,writeSockets,errorSockets = select.select(input, [], [])
            #  makes sure there is data incoming to the server
            for x in readSockets:
                #  condition to check if select returns serverSocket which means
                #  a new socket is trying to connect to us
                if x == s:
                    # accept() accepts an incoming connection
                    connectionSocket, clientAddress = s.accept()
                    #  now we add it to the existing socket list
                    input.append(connectionSocket)
                    print ("The client machine is now connected with an ip address of: " + str(clientAddress))
                    clientConnection += 1

                    print ("Total number of clients: " + str(clientConnection))
                    # userOption is the data recieved from the client: client is to send data in a string of either
                    # "get", "send", or "q"
                    # userOption = connectionSocket.recv(1024)
                    # This section will write to the file for client info
                    output_file.write("\n The client machine is now connected with an ip address of: " + str(clientAddress))
                    output_file.write("\n Number of sessions: " + str(clientConnection))
                else:
                    data = x.recv(2048)
                    actualData = data.decode()
                    #print ("YOUR FRICKEN DATA BRUH: " + str(actualData))
                    #  Once client sends a msg with 'done' in it, client wants
                    #  to disconnect and close the socket and remove the socket
                    #  from input
                    if actualData != 'done':
                        totalLenData = len(data)
                        recvMsg += totalLenData
                        output_file.write("\n Data received from the client --> " + str(recvMsg) + " Bytes")
                        #  print ("\n Data received from the client with size of: " + str(recvMsg) + " Bytes")
                        print ("\n Data received from the client --> " + str(actualData))
                        #dataToSend = data.encode('utf-8')
                        x.send(data)
                        print ("\n Data sent back to the client: " + str(actualData))
                        totalSentData = len(data)
                        sentMsg += totalSentData
                        output_file.write("\n Data sent to the client: " + str(sentMsg) + " Bytes")
                        #print ("\n Data sent back to the client with size of: " + str(sentMsg) + " Bytes")
                    else:
                        print ("\n Client machine: " + str(clientAddress) + ":" + str(connectionSocket) + " has disconnected")
                        x.close()
                        input.remove(x)
                        clientConnection -= 1

    except KeyboardInterrupt:
        # s = socket created, opened, and initialized for when a client connects
        # clientConnection = how many client sessions connect to this server
        # recvMsg = total amount of data received from the client
        # sentMsg = total amount of data sent back to the client
        kill_server(input, clientConnection, recvMsg, sentMsg, output_file)

    #endTime = time.ctime(time.time())
    #finish = time.time()
    #print ("Start Time: " + str(startTime) + " - End Time: " + str(endTime))
    #secondsToFinish = finish - start
    #print ("Using multi-threading, it took: " + str(secondsToFinish) + " seconds to factorize the given number.")


if __name__ == "__main__": main()
