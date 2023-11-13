from sys import argv
from socket import socket, AF_INET, SOCK_STREAM

BUFFER_SIZE = 256

class Client:
  def __init__(self):
    self.client = socket(AF_INET, SOCK_STREAM)
  
  def send(self, address, port):
    self.client.connect((address, port))

    self.client.send(b'Kerek feladatot')

    resp = self.client.recv(BUFFER_SIZE)
    print(resp.decode('utf-8'))

    if resp.decode() == "Tessek a feladat":
      self.client.send(b'Koszonjuk')
      resp = self.client.recv(BUFFER_SIZE)
      print(resp.decode('utf-8'))

    self.client.close()
    

if __name__ == "__main__":
  client = Client()
  client.send(argv[1], int(argv[2]))