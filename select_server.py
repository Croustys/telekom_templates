from sys import argv
from socket import socket, AF_INET, SOCK_STREAM
import select

BUFFER_SIZE = 256
TIMEOUT = 1.0

class Server:
  def __init__(self, ip, port):
    self.ip = ip
    self.port = port

    self.server = self.setup_server()
    self.server.listen()

    self.inputs = [self.server]
    self.outputs = []


  def setup_server(self):
    temp_server = socket(AF_INET, SOCK_STREAM)
    # temp_server.settimeout(TIMEOUT)
    temp_server.bind((self.ip, self.port))
    return temp_server

  def handle_message(self, msg):
    if msg == "a":
      return b'b'
    elif msg == 'c':
      return b'd'

  def close_server(self):
    print("Server closing...")
    for s in self.inputs:
      s.close()
    self.inputs = []
    print("Server closed")

  def serve(self):
    while True:
      try:
        readable, writable, excep = select.select(self.inputs, self.outputs, self.inputs, TIMEOUT)

        if not any([readable, writable, excep]):
          continue

        for sock in readable:
          if sock is self.server:
            conn, address = self.server.accept()
            conn.setblocking(False)
            self.inputs.append(conn)

          else:
            data = sock.recv(BUFFER_SIZE)
            if data:
              data = data.decode()
              print(data)
              to_reply = self.handle_message(data)

              sock.sendall(to_reply)
            else:
              self.inputs.remove(sock)
              sock.close()

      except KeyboardInterrupt:
        self.close_server()


if __name__ == "__main__":
  server = Server(argv[1], int(argv[2]), int(argv[3]))
  server.serve()