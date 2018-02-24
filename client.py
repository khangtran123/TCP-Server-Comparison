#!/bin/python2

'''
File: client.py
Date: February 18, 2018
Designers: Huu Khang Tran, Anderson Phan
File location: C:/xampp/htdocs/acit4850lab04/client.py
Description: This scripts covers the general client that will spawn a bunch of 
             other clients to connect to either the multi-threaded, select, or 
             epoll servers. 
'''

import threading
import socket
import sys
import time
import os
from signal import signal, SIGPIPE, SIG_DFL

global output_file
global clients
global echoedNUM
global RTT
global totalMessages
#  totalRequests - How many requests meaning connections and echoes included towards the server
global totalRequests
totalMessages = 0

#  THis function invokes multi-threading to create multiple clients
def spawn_clients(machineAddr, clients, serverAddr, serverPort, echoedMsg, echoedNUM, totalRequests, output_file):
    threadQueue = []
    clientID = 1
    for i in range(clients):
        #  threading.Thread() starts a new thread and passes in args
        thread = threading.Thread(target=start_engine, args=(machineAddr, clientID, clients, serverAddr, serverPort, echoedMsg, echoedNUM, totalRequests, output_file))
        #  now we want to load up the array "threadQueue"
        threadQueue.append(thread)
        print ("Starting Client #" + str(clientID))
        thread.start()
        clientID += 1

    #  We iterate through all the threads and join() waits for each thread to finish execution
    for thread in threadQueue:
        thread.join()

def start_engine(machineAddr, clientID, clients, serverAddr, serverPort, echoedMsg, echoedNUM, totalRequests, output_file):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serverAddr, serverPort))

    while True:
        # this iterates through the user-specified number of echoes that will be sent out
        for i in range(echoedNUM + 1):
            # start the time once msg is sent to server
            startTime = time.time()
            #echoData = "Message: " + str(echoedMsg) + " --> From Client: " + str(clientID) + "/" + str(machineAddr)
            echoData = "Message: " + str(echoedMsg)
            # totalMessages = ""
            #  totalLenData = len(echoData)
            # this condition is meant for select/epoll server: once the list of messages have been iterated and sent
            # this specific client has to send a quit so that the server can move on to another client session
            if i == echoedNUM:
                print ("Client: " + str(clientID) + " --> has iterated through total number of messages to echo out. Server will be notified.")
                s.send('done')
            else:
                s.send(echoData.encode('utf-8'))
                print ("Message was sent: " + echoData)
                # This value will continuously increment in value after every msg sent --> will output the total bytes sent to client
                totalMessages += echoData
            recvMsg = s.recv(1024)
            print ("Received Msg: " + str(recvMsg) + " Bytes")
            # once we receive the echo back from server, we end the timer
            endTime = time.time()
            # Now we gather the round trip time of the msg being sent from client to server and then from back from server to client.
            RTT = endTime - startTime
            totalRTT += RTT
            avgRTT = RTT / totalRTT
            #  now we want to output the results of this echo stats to the log file
            output_file.write("\n Client #" + str(clientID) + " sent out a total of " + str(echoedNUM) + " messages with a total roundtrip time of " + str(RTT) + " seconds.")
            result_to_file(clients, totalRTT, avgRTT, totalMessages, totalRequests, output_file)
            

def result_to_file(clients, totalRTT, avgRTT, totalMessages, totalRequests, output_file):
    output_file.write("\n Total Number of Clients: " + clients)
    output_file.write("\n Total Number of Requests: " + totalRequests)
    output_file.write("\n Total Data Sent to server: " + str(totalMessages) + " Bytes")
    output_file.write("\n Total Roundtrip Time for each echo: " + str(totalRTT) + " seconds")
    output_file.write("\n Average Roundtrip Time for each echo: " + str(avgRTT) + " seconds")
    
    
def main():
    
    serverAddr = raw_input("Enter the server ip address: ")
    serverPort = 7005

    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((serverIP, port))
    output_file = open('Client-Output.txt','w')
    signal(SIGPIPE, SIG_DFL)

    machineAddr = raw_input("What is your IP Address? (i.e. 192.168.0.X) ")
    clients = raw_input("How many clients would you like to spawn? (Enter an Integer value) ")
    echoedMsg = raw_input("What do you want to echo to the server? (Enter a string) ")
    echoedNUM = raw_input("How many times do you want this message echoed from each client to the server? (Enter an integer value) ")
    option = raw_input("Would you like to commence the echo program? (type 'begin') ")
    
    totalRequests = ((clients * echoedNUM) + clients)

    if option == "begin":
        # we want to makes sure we're not passing a null msg to the server
        if echoedMsg == "":
            print ("The message cannot be null! You must send something")
            echoedMsg = raw_input("What do you want to echo to the server? (Enter a string)")
        else:
            spawn_clients(machineAddr, int(clients), serverAddr, serverPort, echoedMsg, int(echoedNUM), totalRequests, output_file)


if __name__ == "__main__": main()
