import socket
import threading
from helpers import recv_variable_length, send_variable_length

def main():
    print("Inicializando socket")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Atribuindo socket ao endereço localhost na porta 8765")
    server_socket.bind(("localhost", 8765))

    server_socket.listen(5)
    print("Pronto para conexões na porta 8765")

    client_num = 0

    while True:
        print("Aguardando cliente...")

        client_socket, client_address = server_socket.accept()  # Unpacking the tuple
        print(f"Cliente conectado: {client_address}")

        # Use t.start() to properly start the thread
        t = threading.Thread(target=handle_client, args=(client_socket, client_num))
        t.start()

        client_num += 1

def handle_client(socket, ident):
    print(f"Cliente {ident} conectado")

    data, bytes_received = recv_variable_length(socket)

    if data is None:
        print(f"Cliente {ident} - Erro ao receber dados do cliente {ident}")
        return

    count = data.count(b"PING")  # Count PINGs in bytes

    print(f"Cliente {ident} - Recebido: {count} PINGs")  # Decode bytes to string

    message = " ".join(["PONG"] * count)

    send_variable_length(socket, message)

    print(f"Cliente {ident} - Enviado: {count} PONGs")

if __name__ == "__main__":
    main()
