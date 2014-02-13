import socket
import sys
#Optionally choose which port to run on
try:
    PORT = int(sys.argv[1])
except:
    PORT = 6789
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
serverSocket.bind(('', PORT))
serverSocket.listen(8)
while True:
    print 'Ready to serve...'
    connectionSocket, addr = serverSocket.accept()
    message = connectionSocket.recv(1024)
    filename = message.split()[1][1:]
    file_found = False
    try:
        response_body = open(filename).read()
        file_found = True
        print "Serving: %s" % addr[0]
    except IOError:
        print "Failed to find file."
        response_body = "404 Not Found"
    response_headers = {
        'Content-Type': 'text/plain; encoding=utf8',
        'Content-Length': len(response_body),
        'Connection': 'close'
    }
    response_headers = ''.join('%s: %s\n' % (k, v) for k, v in \
                                            response_headers.iteritems())
    if file_found:
        connectionSocket.send("HTTP/1.1 200 OK\n")
    else:
        connectionSocket.send("HTTP/1.1 404 NO\n\r")
    connectionSocket.sendall(response_headers)
    connectionSocket.send("\n")
    connectionSocket.sendall(response_body)
    connectionSocket.close()
