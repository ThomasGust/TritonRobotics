import socket

IP = 'PUT SERVER IP (RASPI) HERE'
PORT = 5005
BS = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((IP, PORT))
sock.listen(1)

connection, address = sock.accept()

print(f"ADDR: {address}")

while 1:
    data = connection.recv(BS)
    if not data: break
    print(f"received: {data}")
    connection.send(data)
connection.close()
