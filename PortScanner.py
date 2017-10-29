#!/usr/bin/env python
# Abraham Ruiz 2017
# based on http://www.pythonforbeginners.com/code-snippets-source-code/port-scanner-in-python with added functionallity

import socket, subprocess, sys, signal, time, os, shutil
from datetime import datetime
def printHelp():
    print("#" * 60)
    print("Simple python scanner")
    print("Abraham Ruiz 2017")
    print("Help\nUsage: scan | s <IP Address> [port] [port]\nTo define a port, enter a port. To define a range, enter the\ntwo ports separated by a \"space\". If no ports are defined it\nwill scan 1 through 1025.\nTo scan a range of hosts type xxx.xxx.xxx.aaa-bbb, where aaa\nis the starting address and bbb is the ending address\n")
    print("file | f <path/to/file>    reads from a file as described above\n")
    print("cd <arg>    changes directory to arg1\n")
    print("pwd    returns the full path of the current directory\n") 
    print("ls    lists the fiels and folders in current directory\n")
    print("help | h  show help\n")
    print("exit    exits the script")
    print("#" * 60)
def Split(splitWord):
    #IP address
    remoteServer = splitWord[1]
    try:
        #find port
        rangeStart = int(splitWord[2])
        try:
            #find port range end
            rangeEnd = int(splitWord[3])
        except IndexError:
            #if no end port is defined use the port start as end 
            rangeEnd = rangeStart
    except IndexError:
        #if no port is defined
        rangeStart = 1
        rangeEnd = 1025
    
    #check if a range was used for IP addresses
    IPrange = remoteServer.split('-')
    IPsplit = IPrange[0].split('.')
    IPStart = IPsplit[3]
    IPsub = IPsplit[0]+'.'+IPsplit[1]+'.'+IPsplit[2]+'.'
    try:
        IPEnd = IPrange[1]
    except IndexError:
        IPEnd = IPStart

    for ip in range(int(IPStart) ,int(IPEnd)+1):

        remoteServer =  str(IPsub) + str(ip)       
        Scan(remoteServer,rangeStart,rangeEnd)

def Scan(remoteServer,rangeStart,rangeEnd):
    
    remoteServerIP  = socket.gethostbyname(remoteServer)
    #Print a nice banner with information on which host we are abou to scan
    print ("-" * 60)
    print "Please wait, scanning remote host", remoteServerIP
    # output += ("-" * 60 + '\rscanned host: ' + remoteServerIP + '\r') 
    print ("-" * 60)

    #Check what time the scan started

    t1 = datetime.now()

    #Using the range function to spcify ports

    try:
        for port in range(rangeStart,rangeEnd+1):

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            sock.settimeout(10)

            result = sock.connect_ex((remoteServerIP,port))
            sock.settimeout(None)

            if result == 0:
                print "Port {}:     Open".format(port)
                # output += "Port {}:     Open".format(port) + '\r'
            sock.close()

    except KeyboardInterrupt:
        print "User exit (Ctrl + C)"
        sys.exit()

    # except socket.gaierror:
    #     print "Hostname could not be resolved."

    # except socket.error:
    #     print "Couldn't connect to server"

    #Check time again
    t2 = datetime.now()

    #Calculate difference of tiem

    total = t2-t1
    print "Scanning completed in ",total
    print "+" * 60
    print "\n\n\n\n"
    return;

#Clear the screen
subprocess.call('clear', shell=True)

while True:
    # output = ''''''
    # toFile = 0
    #get command
    line = raw_input("Enter a command: ")

    if line != "":
        


        splitWord = line.split()

        if splitWord[0] == "exit":
            print("Goodbye")
            sys.exit()
        elif splitWord[0] == "help" or splitWord[0] == "h" or splitWord[0] == "-h":
            printHelp()
        elif splitWord[0] == "file" or splitWord[0] == "f" or splitWord[0] == "-f":
            path = line[3:]
            with open(path) as f:
                for fileLine in f:

                    Split(fileLine.split())
        elif splitWord[0] == "pwd":
        	print("Current directory is: %s" % os.getcwd())
        elif splitWord[0] == "cd":
            path = line[3:]
            os.chdir(path)
        elif splitWord[0] == "ls":
        	print("list")
        	print("%s" % os.listdir(os.getcwd()))    
        elif splitWord[0] == "scan" or splitWord[0] == "s" or splitWord[0] == "-s":

            Split(splitWord)
        else:
            printHelp()
