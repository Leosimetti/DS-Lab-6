import socket
from threading import Thread
import os
import re

@todo #55:45min
clients = []
BUFF = 1488 # Unified constant

# @todo #228:15m/DEV Me noam
# TODO #ABOBA:15m/DEV AAAAAAAAAA I boba
# TODO #234:15m/DEV AAAAAAAAAA I boba

/**
 * @todo #228:5m/DEV ABOBA
 */

/**
 * @todo #234:15m/DEV This is something to do later
 *  in one of the next releases. I can't figure out
 *  how to implement it now, that's why the puzzle.
 */

# Thread to listen one particular client
class ClientListener(Thread):
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name

    # clean up
    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')

    def run(self):

        # Unpack the metadata that goes as the first package
        received = self.sock.recv(BUFF).decode()
        filename, filesize = received.split("?CON?")

        print(f"[{self.name}] Starting transfer of {filename}")

        # Account for duplicates
        for _, _, files in os.walk("."):

            # Going through all files in the directory
            for name in files:

                # If duplicate is located
                if name == filename:

                    # Find the original name
                    base, ext = name.split(".")

                    # if it is already a copy
                    if "_copy" in name:

                        # FInd name without _copy
                        base, _ = name.split("_copy")

                        # searching for numbers at the end
                        temp = re.search(r'(\d+)[.]', name)
                        if temp:
                            num = int(temp.group(1))
                            filename = base + "_copy" + str(num+1) + '.' + ext
                        else:
                            filename = base + "_copy1" + '.' + ext

                    # if there are no copies
                    else:
                        filename = base + "_copy" + '.' + ext



        # Make the data actually useful
        filename = os.path.basename(filename)
        filesize = int(filesize)

        # Counter initialization
        sas = 0.0

        # Receive/Write

        with open(filename, "wb") as f:

            for i in range(filesize):
                # Will return zero when done
                rcv = self.sock.recv(BUFF)
                if rcv:
                    # Write received data
                    sas += BUFF
                    f.write(rcv)
                else:
                    print(f"[{self.name}] Transfer complete!!")
                    break
        self._close()


def main():
    next_name = 1

    # AF_INET – IPv4, SOCK_STREAM – TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # reuse address; in OS address will be reserved after app closed for a while
    # so if we close and imidiatly start server again – we'll get error
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # listen to all interfaces at 8800 port
    sock.bind(('', 1488))
    sock.listen()
    print("Waiting for clients...")
    while True:
        # blocking call, waiting for new client to connect
        con, addr = sock.accept()
        clients.append(con)
        name = 'u' + str(next_name)
        next_name += 1
        print(f"[{name}] " + str(addr) + ' connected')
        # start new thread to deal with client
        ClientListener(name, con).start()


if __name__ == "__main__":
    main()



