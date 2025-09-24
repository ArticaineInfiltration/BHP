import socket,threading,sys

ip = '0.0.0.0'
port = 8888 

def main():
    # create and start the server
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(10)
    server.settimeout(1)

    print(f"[*] Listening on {ip}:{port}")


    # server listening and handling of info:
    while True:
        try: 
            client,addr = server.accept()
        except socket.timeout as t: 
            continue # just loop again, timeout is used to detect kb interrupt 
        except OSError:
            break  # server closed

        print(f'[*] Accepted Connection from {addr[0]}:{addr[1]}')
        clientHandler = threading.Thread(target=handleClient,args=(client,))
        clientHandler.start()

    
def handleClient(clientSocket):
    with clientSocket as c : 
        request = c.recv(1024).decode("utf-8")
        print(f'[*] Received: {request}')
        c.send(b'ACK')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as kb: 
        sys.exit(0)