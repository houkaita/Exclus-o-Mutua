import socket
import threading
from queue import Queue

class Coordinator:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.queue = Queue()
        self.logs = []
        self.lock = threading.Lock()
        self.process_sockets = {}

    def handle_request(self, conn, addr):
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break
                with self.lock:
                    if data.startswith("REQUEST"):
                        self.queue.put((addr, data))
                        self.logs.append(f"Received {data} from {addr}")
                        print(f"[COORDINATOR] {data} received from {addr}")
                        if self.queue.qsize() == 1:  
                            self.send_grant(addr)
                    elif data.startswith("RELEASE"):
                        self.logs.append(f"Received RELEASE from {addr}")
                        print(f"[COORDINATOR] RELEASE received from {addr}")
                        self.queue.get()  
                        if not self.queue.empty():
                            next_addr, _ = self.queue.queue[0]
                            self.send_grant(next_addr)
                self.print_logs()
            except ConnectionResetError:
                break

    def send_grant(self, addr):
        conn = self.process_sockets[addr]
        conn.sendall("GRANT".encode())
        self.logs.append(f"Sent GRANT to {addr}")
        print(f"[COORDINATOR] GRANT sent to {addr}")

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        print(f"Coordinator listening on {self.host}:{self.port}")
        
        while True:
            conn, addr = server_socket.accept()
            with self.lock:
                self.process_sockets[addr] = conn
            threading.Thread(target=self.handle_request, args=(conn, addr)).start()

    def print_logs(self):
        print("\n".join(self.logs))

if __name__ == "__main__":
    coordinator = Coordinator('127.0.0.1', 65432)
    coordinator.start()
