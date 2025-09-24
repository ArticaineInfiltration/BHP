import socket 


targetHost = "127.0.0.1" 
targetPort = 9997 


# create a socket object: 

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# AF_INET -> IPV4 addr or hostname 
# DGRAM  => UDP client 

# connect the client 


# send data
client.sendto(b"AAABBBCCC",(targetHost,targetPort))

#receive data: 
data, addr = client.recvfrom(4096)

print(data.decode())
client.close()
