import os, socket

# Unified constant
BUFF = 1488

# Creating the server
s = socket.socket()
s.bind(("0.0.0.0", 1488))
s.listen()
print("Waiting for clients...")

# Waiting for connection
client, cli_ip = s.accept()
print("!!!Client connected!!!")

# Unpack the metadata
received = client.recv(BUFF).decode()
filename, filesize = received.split("?CON?")

# Make the data actually useful
filename = os.path.basename(filename)
filesize = int(filesize)

# Counter initialization
sas = 0.0
pr_digit = '0'

# Receive/Write
with open(filename, "wb") as f:
    for i in range(filesize):

        # Will return zero when done
        rcv = client.recv(BUFF)
        if rcv:

            # To make output less annoying
            msg = str(round(sas / float(filesize) * 100))

            if pr_digit != msg[0]:
                print(msg, " %")
                pr_digit = msg[0]

            sas += BUFF
            f.write(rcv)
        else:
            print("Transfer complete!!")
            break

# Cleanup
client.close()
s.close()
