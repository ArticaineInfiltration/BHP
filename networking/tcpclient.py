import socket 


targetHost = "192.168.18.4" 
targetPort = 8888 


# create a socket object: 

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# AF_INET -> IPV4 addr or hostname 
# SOCK Stream => TCP client 

# connect the client 

client.connect((targetHost,targetPort))

# send data
client.send(b"&")

#receive data: 
response = client.recv(4096)

print(response.decode())
client.close()
