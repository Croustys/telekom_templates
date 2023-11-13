from sys import argv
from socket import socket, AF_INET, SOCK_DGRAM
from random import randint

BUFFER_SIZE = 256
TIMEOUT = 1.0

class ZHServer:
  def __init__(self, ip, port):
    self.ip = ip
    self.port = port

    self.run = True

    self.server = self.setup_server()

  def setup_server(self):
    temp_server = socket(AF_INET, SOCK_DGRAM)
    # temp_server.settimeout(TIMEOUT)
    # temp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    temp_server.bind((self.ip, self.port))
    return temp_server

  def handle_message(self, msg):
    if msg == "Keres":
      return f'feladat{randint(1,10)}'.encode()

  def serve(self):
    while self.run:
      try:
        data, addr = self.server.recvfrom(BUFFER_SIZE)
        print(data.decode())

        to_reply = self.handle_message(data.decode())

        self.server.sendto(to_reply, addr)

      except KeyboardInterrupt:
        print("Closing Server...")
        self.server.close()
        self.run = False


if __name__ == "__main__":
  server = ZHServer(argv[1], int(argv[2]))
  server.serve()