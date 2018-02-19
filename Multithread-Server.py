'''
File: Multithread-Server.py
Date: February 16, 2018
Designers: Huu Khang Tran, Anderson Phan
File location: C:/xampp/htdocs/acit4850lab04/Multithread-Server.py
Description: This scripts covers multithreading for a server. 
'''

import socket
import threading
import time
import sys

exitFlag = 0

#the function that will be implemented will be the "echo" server
#  That means this will act as the worker function that will implement the echo
# means it will send and recv datagrams from the client
def echo_server(newSocket):
    #declaring these as global variables so it can be accessed in another function
    global recvMsg
    global sentMsg
    
    print "Thread is online"
    #this makes sure the server is always receiving a message from the client
    #purpose of an echo server 
    while True:
        # Server receives msg from client
        data = newSocket.recv(1024)
        totalLenData = len(data)
        recvMsg += totalLenData
        #if the data received is greater than 0 bytes, send it back to the client
        if totalLenRecv > 0:
            output_file.write("\n Data received from the client: " + str(recvMsg))
            newSocket.send(data)
            totalSentData = len(data)
            sentMsg += totalSentData
            output_file.write("\n Data sent to the client: " + str(sentMsg))
        else:
            print "Still waiting for client message"

# s = socket created, opened, and initialized for when a client connects
# clientConnection = how many client sessions connect to this server
# recvMsg = total amount of data received from the client
# sentMsg = total amount of data sent back to the client
def kill_server(s, clientConnection, recvMsg, sentMsg):
    
    output_file.write("\n Total connections: " + str(clientConnection))
    output_file.write("\n Total amount of data received from the client" + str(recvMsg))
    output_file.write("\n Total amount of data sent to the client" + str(sentMsg))
    #now we have to close/end the session if the server was to be terminated
    s.close()
    print "The client socket session is now closed."
    #to avoid getting a SystemExit exception which can be viewed as an error, 
    # we use sys.exit() to get around it
    sys.exit()
'''
Now we need to use locks to synchronize access to shared resources.
If you have multiple threads running at the same time who all needs resources,
a lock has to be aquired by the first thread which means other threads can't use
it until the first thread is done with it.
'''

def main():
    
    #startTime = time.ctime(time.time())
    #start = time.time()
    # clientConnection is a list to keep track of all the clients who connect to this server
    clientConnection = 0
    
    output_file = open('Multithreading_Server-Output.txt','w')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'
    port = 7005
    s.bind((host,port))
    
    print "Server Started"
    
    #listens up to 50 connections/clients
    s.listen(50)
    
    try:
        while True:
            # accept() accepts an incoming connection
            connectionSocket, clientAddress = s.accept()
            print "The client machine is now connected with an ip address of: " + str(clientAddress)
            clientConnection += 1
            #userOption is the data recieved from the client: client is to send data in a string of either 
            #"get", "send", or "q"
            userOption = connectionSocket.recv(1024)
            # This section will write to the file for client info
            output_file.write("\n The client machine is now connected with an ip address of: " + str(clientAddress))
            output_file.write("\n Number of sessions: " + str(clientConnection))
            if userOption == 'connect':
                thread = threading.Thread(target=echo_server, args=(connectionSocket,))
                #  now since this is a server that should always stay online, if a thread was to be killed
                #  the daemon should still be active for other clients
                thread.setDaemon(True)
                thread.start()
    except KeyboardInterrupt:
        # s = socket created, opened, and initialized for when a client connects
        # clientConnection = how many client sessions connect to this server
        # recvMsg = total amount of data received from the client
        # sentMsg = total amount of data sent back to the client
        kill_server(s, clientConnection, recvMsg, sentMsg)
        
    #endTime = time.ctime(time.time())
    #finish = time.time()
    #print ("Start Time: " + str(startTime) + " - End Time: " + str(endTime))
    #secondsToFinish = finish - start
    #print ("Using multi-threading, it took: " + str(secondsToFinish) + " seconds to factorize the given number.")
    
    
if __name__ == "__main__": main()
