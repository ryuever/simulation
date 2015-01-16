import sys
from socket import *              # portable socket interface plus constants
# serverHost = '127.0.0.1'          # server name, or: 'starship.python.net'
# serverPort = 50008                # non-reserved port used by the server
if len(sys.argv) == 3:
    serverHost = sys.argv[1]
    serverPort = sys.argv[2]
else:
    serverHost = 'localhost'
    serverPort = 50000


# message = [b'Hello network world']          # default text to send to server
                                            # requires bytes: b'' or str,encode()
if len(sys.argv) > 1:       
    serverHost = sys.argv[1]                # server from cmd line arg 1
    if len(sys.argv) > 2:                   # text from cmd line args 2..n
        message = (x.encode() for x in sys.argv[2:])  

sockobj = socket(AF_INET, SOCK_STREAM)      # make a TCP/IP socket object

while True:
    text = input()
    print(text)
    sockobj.connect((serverHost, eval(serverPort)))   # connect to server machine + port
    bytesThing = text.encode(encoding='UTF-8')
    sockobj.send(bytesThing)
#    sockobj.send(line)                      # send line to server over socket
    data = sockobj.recv(1024)               # receive line from server: up to 1k
    response = data.decode()
    print('Client received:', response)         # bytes are quoted, was `x`, repr(x)

sockobj.close()                             # close socket to send eof to server
