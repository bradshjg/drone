import socket

# create UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

local_ipaddr = '192.168.169.2'
local_port = 56789
ipaddr = '192.168.169.1'
port = 8800

init_message = bytes.fromhex('ef000400')
s.bind((local_ipaddr, local_port))
print("send init message")
for i in range(1, 10):
  s.sendto(init_message, (ipaddr, port))

print("receiving data")
fp = open('test.stream', 'wb')
while True:
  data = s.recv(1024)
  fp.write(data)
