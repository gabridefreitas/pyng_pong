import socket
import time
from helpers import recv_variable_length, send_variable_length

MESSAGE_SIZES = [10, 100, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]


def send_message_and_measure(socket, message):
    start_time = time.time()

    success, bytes_sent = send_variable_length(socket, message)
    if not success:
        print("Falha ao enviar a mensagem.")
        return None, bytes_sent, 0

    response, bytes_received = recv_variable_length(socket)
    if response is None:
        print("Falha ao receber a resposta.")
        return None, bytes_sent, bytes_received

    end_time = time.time()

    rtt = end_time - start_time

    total_bytes = bytes_sent + bytes_received
    bandwidth = total_bytes / rtt if rtt > 0 else 0

    print(f"Resposta do servidor: {bytes_received} bytes com {response.count(b"PONG")} PONGs")
    print(f"Tempo de Ida e Volta (RTT): {rtt:.6f} segundos")
    print(f"Largura de Banda Utilizada: {bandwidth:.2f} bytes/segundo")

    return rtt, bytes_sent, bytes_received

def main():
    print("Inicializando socket")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Conectando socket ao endereço localhost na porta 8765")
    client_socket.connect(("localhost", 8765))

    for msg_size in MESSAGE_SIZES:
        print("Construindo a mensagem")
        msg = " ".join(["PING"] * msg_size)

        print(f"Enviando {msg_size} PINGs")

        rtt, bytes_sent, bytes_received = send_message_and_measure(client_socket, msg)

        if rtt is not None:
            print("\n--- Resumo da Transmissão ---")
            print(f"Bytes Enviados: {bytes_sent} bytes")
            print(f"Bytes Recebidos: {bytes_received} bytes")
            print(f"RTT: {rtt:.6f} segundos")
            print(f"Largura de Banda: {bytes_sent + bytes_received} bytes / {rtt:.6f} segundos = {(bytes_sent + bytes_received) / rtt:.2f} bytes/segundo")
        else:
            print("A transmissão não foi concluída com sucesso.")

    client_socket.close()
    print("Conexão encerrada.")

if __name__ == "__main__":
    main()
