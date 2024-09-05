import socket
import sys
import time

def run_process(host, port, process_id, r):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    for i in range(1, r + 1):
        repetition_str = f"{i:06}"
        request_msg = f"REQUEST|{process_id}|{repetition_str}"
        print(f"[PROCESS {process_id}] Sending: {request_msg}")
        client_socket.sendall(request_msg.encode())
        
        data = client_socket.recv(1024).decode()
        if data == "GRANT":
            print(f"[PROCESS {process_id}] Received: GRANT")
            
            # Entra na região crítica, escreve e aguarda
            enter_critical_section(process_id)
            time.sleep(10)  # Aguarda 10 segundos DENTRO da região crítica
            
            # Após aguardar, envia RELEASE
            release_msg = f"RELEASE|{process_id}|{repetition_str}"
            print(f"[PROCESS {process_id}] Sending: {release_msg}")
            client_socket.sendall(release_msg.encode())

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
