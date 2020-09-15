import os, socket

# Unified constant
BUFF = 1488

name = "hi.txt"
size = os.path.getsize(name)
print("Trying to connect...")

# create the client socket
s = socket.socket()
s.connect(("127.0.0.1", 1488))
print("!!!Connected to server!!!")  # if it is not displayed ==> OOF

# Send them together, so that they do not get lost :)
msg = name + "?CON?" + str(size)
s.send(msg.encode())

# Counter initialization
sas = 0
pr_digit = '0'

with open(name, "rb") as f:
    for i in range(size):
        snd = f.read(BUFF)
        if snd:

            # To make output less annoying
            msg = str(round(sas / float(size) * 100))
            if pr_digit != msg[0]:
                print(msg, " %")
                pr_digit = msg[0]

            sas += BUFF
            s.sendall(snd)
        else:
            print("Transfer complete!!")
            break

# Cleanup
s.close()
