import socket


TCP_IP = socket.gethostname()
TCP_PORT = 8000


def run_client(ip, port):
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as sock:
        server = ip, port
        sock.connect((ip, port))
        print(f'Connection established {server}')
        message = input('--> ')

        while message.lower().strip() != 'end':
            sock.send(message.encode())
            data = sock.recv(2048).decode()
            print(f'Received message: {data}')
            if data == 'OK':
                continue
            message = input('--> ')
        sock.close()
    print(f'The connection to the server is complete.')


if __name__ == '__main__':
    run_client(TCP_IP, TCP_PORT)
