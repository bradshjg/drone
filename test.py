import socket

# create UDP socket
s = socket.socket(socket.AF_INET, socket.DGRAM)

ipaddr = '192.168.169.1'
port = 8800
# send data to server
init_message = bytes.fromhex('ef08080001000000')
s.bind((ipaddr, port))
print("send init message")
for i in range(1, 4):
  s.send(init_message, (ipaddr, port))

print("receiving data")
fp = open('test.stream', 'w')
while True:
  data = s.recv(1024)
  fp.write(data)
