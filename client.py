'''
File: client.py
Date: February 18, 2018
Designers: Huu Khang Tran, Anderson Phan
File location: C:/xampp/htdocs/acit4850lab04/client.py
Description: This scripts covers the general client that will spawn a bunch of 
             other clients to connect to either the multi-threaded, select, or 
             epoll servers. 
'''

import socket
import sys
import time


# THis function invokes multi-threading to create multiple clients
def spawn_clients(machineAddr, clients, serverAddr, serverPort, echoedMsg, echoedNUM):
    threadQueue = []
    clientID = 1
    for i in range(clients):
        #  threading.Thread() starts a new thread and passes in args
        thread = threading.Thread(target=start_engine, args=(machineAddr, clientID, serverAddr, serverPort, echoedMsg, echoedNUM))
        #  now we want to load up the array "threadQueue"
        threadQueue.append(thread)
        print ("Starting Client #" + str(threadID))
        thread.start()
        clientID += 1

    #  We iterate through all the threads and join() waits for each thread to finish execution
    for thread in threadQueue:
        thread.join()

def start_engine(machineAddr, clientID, serverAddr, serverPort, echoedMsg, echoedNUM):
    global timeRoundtrip
    global finalMsgCount
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serverAddr, serverPort))
    
    while True:
        # this iterates through the user-specified number of echoes that will be sent out
        for i in range(echoedNUM + 1):
            # start the time once msg is sent to server
            startTime = time.time()
            echoData = "Message: " + str(echoedMsg) + " --> From Client: " + str(clientID) + "/" + str(machineAddr)
            #  totalLenData = len(echoData)
            # this condition is meant for select/epoll server: once the list of messages have been iterated and sent
            # this specific client has to send a quit so that the server can move on to another client session
            if i == echoedNUM:
                print ("Client: " + str(clientID) + " --> has iterated through total number of messages to echo out. Server will be notified.")
                s.send('done')
            else:
                s.send(echoData)
                print ("Message sent!")
                # This value will continuously increment in value after every msg sent --> will output the total bytes sent to client
                finalMsgCount += echoData
            recvMsg = s.recv(1024)
            print ("Received Msg: " + str(recvMsg))
            # once we receive the echo back from server, we end the timer
            endTime = time.time()
            # Now we gather the round trip time of the msg being sent from client to server and then from back from server to client. 
            timeRoundtrip = endTime - startTime
        #now we want to output the results of this echo stats to the log file
        output_file.write("\n Client #" + str(clientID) + " sent out a total of " + str(echoedNUM) + " messages with a total roundtrip time of " + str(timeRoundtrip) + " seconds.")
                
            
def result_to_file():
    return

def main():
    global clients
    global echoedNUM
    
    serverAddr = raw_input("Enter the server ip address: ")
    serverPort = 7005
    
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((serverIP, port))
    output_file = open('Client-Output.txt','w')
    
    machineAddr = raw_input("What is your IP Address? (i.e. 192.168.0.X) ")
    clients = raw_input("How many clients would you like to spawn? (Enter an Integer value) ")
    echoedMsg = raw_input("What do you want to echo to the server? (Enter a string)")
    echoedNUM = raw_input("How many times do you want this message echoed from each client to the server? (Enter an integer value) ")
    option = raw_input("Would you like to commence the echo program? (type 'begin')")
    
    if option == "begin":
        # we want to makes sure we're not passing a null msg to the server
        if echoedMsg == "":
            print ("The message cannot be null! You must send something")
            echoedMsg = raw_input("What do you want to echo to the server? (Enter a string)")
        else:
            spawn_clients(machineAddr, clients, serverAddr, serverPort, echoedMsg, echoedNUM)

if __name__ == "__main__": main()
