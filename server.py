from sys import argv
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
import select

BUFFER_SIZE = 256
TIMEOUT = 1.0

class Server:
  def __init__(self, ip, port, student_minimum = 1):
    self.ip = ip
    self.port = port
    self.student_minimum = student_minimum
    self.student_counter = 0

    self.server = self.setup_server()
    self.server.listen()

    self.udp = self.setup_zh()
    self.udp_address = (ip, 5005)

    self.inputs = [self.server]
    self.outputs = []


  def setup_server(self):
    temp_server = socket(AF_INET, SOCK_STREAM)
    temp_server.settimeout(TIMEOUT)
    temp_server.bind((self.ip, self.port))
    return temp_server
  
  def setup_zh(self):
    temp = socket(AF_INET, SOCK_DGRAM)
    temp.settimeout(TIMEOUT)
    return temp

  def handle_message(self, msg):
    if msg == "Kerek feladatot":
      self.student_counter += 1
      if self.student_minimum <= self.student_counter:
        self.udp.sendto(b'Keres', self.udp_address)
        resp, addr = self.udp.recvfrom(BUFFER_SIZE)
        print(resp.decode())
        return b'Tessek a feladat'
      else:
        return b'Meg nincs'
    elif msg == 'Koszonjuk':
      return b'Szivesen'

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