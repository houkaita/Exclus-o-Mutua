import socket
import sys
import time

def run_process(host, port, process_id, r):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    for _ in range(r):
        request_msg = f"REQUEST|{process_id}|000000"
        print(f"[PROCESS {process_id}] Sending: {request_msg}")
        client_socket.sendall(request_msg.encode())
        
        data = client_socket.recv(1024).decode()
        if data == "GRANT":
            print(f"[PROCESS {process_id}] Received: GRANT")
            enter_critical_section(process_id)
            
            release_msg = f"RELEASE|{process_id}|000000"
            print(f"[PROCESS {process_id}] Sending: {release_msg}")
            client_socket.sendall(release_msg.encode())
        
        time.sleep(2)

    client_socket.close()

def enter_critical_section(process_id):
    with open("resultado.txt", "a") as file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file.write(f"Process {process_id} entered at {timestamp}\n")
        print(f"[PROCESS {process_id}] Wrote to resultado.txt")

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 65432
    process_id = sys.argv[1]
    r = int(sys.argv[2])

    run_process(host, port, process_id, r)
