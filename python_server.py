import socket
import threading

def handle_client(client_socket):
    # Replace this with your logic to fetch values from an external source
    temp2 = [100, 200, 300, 400]
    response = ','.join(map(str, temp2)).encode()
    client_socket.send(response)
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print("[*] Listening on 0.0.0.0:12345")

    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == '__main__':
    start_server()
