import socket

def start_client(IP):
    #IP = 'PUT IP ADDRESS OF PC HERE'
    PORT = 5005
    BS = 1024

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, PORT))
    sock.send("CLIENT: THIS IS A SIMPLE TEST TO SEE IF I CAN SEND DATA BETWEEN RASPBERRY PI AND COMPUTER OVER ETHERNET")
    data = sock.recv(BS)
    sock.close()

    print(f"received: {data}")

if __name__ == "__main__":
    ip_addr = input("Please provide an IP address for the client")
    start_client(ip_addr)