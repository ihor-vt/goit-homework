import socket
from concurrent import futures


TCP_IP = socket.gethostname()
TCP_PORT = 8000


def run_server(ip, port):
    def handle(sock: socket.socket, address: str):
        print(f'Connection established {address}')
        while True:
            received = sock.recv(2048)
            if not received:
                break

            data = received.decode()
            print(f'Received message form {sock.getsockname()}: {data}')
            message = 'OK'  # input('--> ')
            sock.send(message.encode())

    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(4)
    print(f'Start server {server_socket.getsockname()}')
    with futures.ThreadPoolExecutor(4) as client_pool:
        try:
            while True:
                new_sock, address = server_socket.accept()
                client_pool.submit(handle, new_sock, address)
        except KeyboardInterrupt:
            print(f'Destroy server')
        finally:
            print(f'Socket connection closed {address}')
            server_socket.close()


if __name__ == '__main__':
    run_server(TCP_IP, TCP_PORT)
