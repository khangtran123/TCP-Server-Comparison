#! /usr/bin/python3
'''
File: Multithread-Server.py
Date: February 16, 2018
Designers: Huu Khang Tran, Anderson Phan
File location: C:/xampp/htdocs/acit4850lab04/Multithread-Server.py
Description: This scripts covers multithreading for a server.
'''

import socket
import select
import time
import sys
from socket import error as SocketError

exitFlag = 0
LineEnd1 = b"\n\n"
LineEnd2 = b"\n\r\n"
echoEnd = b'done'

global clientConnection
global serverSocket
global dataBuffer
global epoll
global dataReceive
global dataSent
global connections
connections = {}; requests = {}; responses = {}

dataBuffer = 2048
dataSent = 0
dataReceive = 0
clientConnection = 0
epoll = select.epoll()

#the function that will be implemented will be the "echo" server
#  That means this will act as the worker function that will implement the echo
# means it will send and recv datagrams from the client
#def echo_server(newSocket):
#    #declaring these as global variables so it can be accessed in another function
#    global recvMsg
#    global sentMsg

#    print ("Thread is online")
    #this makes sure the server is always receiving a message from the client
    #purpose of an echo server
#    while True:
        # Server receives msg from client
#        data = newSocket.recv(1024)
#        totalLenData = len(data)
#        recvMsg += totalLenData
        #if the data received is greater than 0 bytes, send it back to the client
#        if totalLenRecv > 0:
#            output_file.write("\n Data received from the client: " + str(recvMsg))
#            newSocket.send(data)
#            totalSentData = len(data)
#            sentMsg += totalSentData
#            output_file.write("\n Data sent to the client: " + str(sentMsg))
#        else:
#            print ("Still waiting for client message")

# s = socket created, opened, and initialized for when a client connects
# clientConnection = how many client sessions connect to this server
# recvMsg = total amount of data received from the client
# sentMsg = total amount of data sent back to the client
#def kill_server(s, clientConnection, recvMsg, sentMsg):
#    output_file = open('Multithreading_Server-Output.txt','w')

#    output_file.write("\n Total connections: " + str(clientConnection))
#    output_file.write("\n Total amount of data received from the client" + str(recvMsg))
#    output_file.write("\n Total amount of data sent to the client" + str(sentMsg))
    #now we have to close/end the session if the server was to be terminated
#    s.close()
#    print ("The client socket session is now closed.")
    #to avoid getting a SystemExit exception which can be viewed as an error,
    # we use sys.exit() to get around it
#    sys.exit()

#defining a function that will having all new connections that's coming to the server
def newConnection():
    global serverSocket
    global clientConnection
    global connections

    while True:
        try:
            clientSocket, clientAddress = serverSocket.accept()
            clientConnection += 1
            clientSocket.setblocking(0)
            connections.update({clientSocket.fileno(): clientSocket})
            epoll.register(clientSocket, select.EPOLLIN | select.EPOLLET)
            print ("client connection received: \n" + str(clientSocket))
            output_file.write("\n The client machine is now connected with an ip address of: " + str(clientSocket))
        except:
            break

#defining a function that will handle incoming data and echo it back.
def dataEcho(fileno):
    global epoll
    global connections
    global dataSent
    global dataReceive
    global dataBuffer

    clientSocket = connections.get(fileno)
    try:
        data = clientSocket.recv(dataBuffer)
        dataReceive += len(data)
        print ("received data from a client: " + str(data.decode()))
        if(data != "" and data != "done"):
            clientSocket.sendall(data)
            dataSent += len(data)
        elif(data == "done"):
            print("Client reponse of finished responses, releasing client socket.")
            epoll.modify(clientSocket, select.EPOLLHUP | select.EPOLLET)
            clientSocket.shutdown()
            clientSocket.close()
    except SocketError as e:
        print ("socket error occured.")
        if e.errno != errno.ECONNRESET:
            raise
        pass

'''
Now we need to use locks to synchronize access to shared resources.
If you have multiple threads running at the same time who all needs resources,
a lock has to be aquired by the first thread which means other threads can't use
it until the first thread is done with it.
'''

def main():
    global serverSocket
    global epoll
    global connections
    global dataBuffer
    global dataReceive
    global dataSent
    global clientConnection

    #startTime = time.ctime(time.time())
    #start = time.time()
    # clientConnection is a list to keep track of all the clients who connect to this server
    output_file = open('Multithreading_Server-Output.txt','w')
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = '0.0.0.0'
    port = 7005
    #listens up to 50 connections/clients. depending on how many incoming connections this may be raised
    epoll.register(serverSocket.fileno(), select.EPOLLIN | select.EPOLLET)
    connections.update({serverSocket.fileno(): serverSocket})
    serverSocket.bind((host,port))
    serverSocket.listen(socket.SOMAXCONN)
    serverSocket.setblocking(0)
    print ("Server Started")

    try:
        while True:
            events = epoll.poll(-1)
            #listens on 1 second intervals
            for fileno, event in events:
                #accepts a new incoming connection
                if fileno == serverSocket.fileno():
                    newConnection()
                elif event & select.EPOLLIN:
                    #this is where epoll gets messages flagged as inbound
                    dataEcho(fileno)
                elif event & select.EPOLLHUP:
                    #once echoing is done, close the socket connection
                    epoll.unregister(fileno)
                    connections[fileno].close()
                    del connections[fileno]
				# This section will write to the file for client info
                output_file.write("\n Number of sessions: " + str(clientConnection))
				#if userOption == 'connect':

    except KeyboardInterrupt as e:
        # s = socket created, opened, and initialized for when a client connects
        # clientConnection = how many client sessions connect to this server
        # recvMsg = total amount of data received from the client
        # sentMsg = total amount of data sent back to the client
        #kill_server(s, clientConnection, 0, 0)
        print ("\n terminal interruption of server via control+c, \n shutting down server and server sockets")
        epoll.unregister(serverSocket.fileno())
        epoll.close()
        serverSocket.close()
        sys.exit(0)


    #endTime = time.ctime(time.time())
    #finish = time.time()
    #print ("Start Time: " + str(startTime) + " - End Time: " + str(endTime))
    #secondsToFinish = finish - start
    #print ("Using multi-threading, it took: " + str(secondsToFinish) + " seconds to factorize the given number.")


if __name__ == "__main__": main()
