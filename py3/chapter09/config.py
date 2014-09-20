workers = 1
worker_class = 'sync'

def printout(data):
    """Print and then return the given data."""
    print(data.decode('ascii'))
    return data

class Noisy:
    def __init__(self, sock): self.sock = sock
    def recv(self, count): return printout(self.sock.recv(count))
    def send(self, data): return self.sock.send(printout(data))
    def sendall(self, data): return self.sock.sendall(printout(data))
    def __getattr__(self, name): return getattr(self.sock, name)

def post_fork(server, worker):
    def accept():
        client, addr = _accept()
        return Noisy(client), addr
    sock = worker.sockets[0]
    _accept = sock.accept
    sock.accept = accept
