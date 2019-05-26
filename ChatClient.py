import socket
import select
import sys

HOST = 'localhost'
PORT = 12001

MASTER_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
MASTER_SOCK.settimeout(200)

# Try to connect to server
try:
    MASTER_SOCK.connect((HOST, PORT))
except Exception as msg:
    print(type(msg).__name__)
    print("Unable to connect")
    sys.exit()

print("Connected to remote host. Start sending messages")

while True:
    SOCKET_LIST = [sys.stdin, MASTER_SOCK]
    # Get the list sockets which are readable
    READ_SOCKETS, WRITE_SOCKETS, ERROR_SOCKETS = select.select(SOCKET_LIST, [], [])

    # Incoming message from remote server
    for sock in READ_SOCKETS:
        if sock == MASTER_SOCK:
            data = sock.recv(4096)
            if not data:
                print('\nDisconnected from chat server')
                sys.exit()
            else: # Print data
                print(data.decode())
        else: # User entered a message
            msg = sys.stdin.readline()
            print("\x1b[1A" + "\x1b[2K") # erase last line
            MASTER_SOCK.sendall(msg.encode())
