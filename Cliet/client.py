import os
import socket
import sys

# Unified constant
BUFF = 1488

if len(sys.argv) != 4:
    print("Wrong arguments!")
    exit(228)

name = sys.argv[1]
SERV_IP = sys.argv[2]
SERV_PORT = sys.argv[3]

size = os.path.getsize(name)
print("Trying to connect to", SERV_IP + SERV_PORT)

# create the client socket
s = socket.socket()
s.connect((SERV_IP, SERV_PORT))
print("!!!Connected to server!!!")  # if it is not displayed ==> OOF

# Send them together, so that they do not get lost :)
msg = name + "?CON?" + str(size)
s.send(msg.encode())

# Counter initialization
sas = 0
pr_digit = '0'

# Read/Send
with open(name, "rb") as f:
    for i in range(size):
        snd = f.read(BUFF)
        if snd:

            # To make output less annoying
            msg = str(round(sas / float(size) * 100))
            if pr_digit != msg[0] and round(sas / float(size) * 100) > 9:
                print(msg, " %")
                pr_digit = msg[0]

            sas += BUFF
            s.sendall(snd)
        else:
            print("Transfer complete!!")
            break

# Cleanup
s.close()
