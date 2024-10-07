import socket
import struct

def recv_all(sock, length):
    """Receber exatamente `length` bytes do socket."""
    data = b''
    while len(data) < length:
        try:
            packet = sock.recv(length - len(data))
            if not packet:
                raise ConnectionError("Socket foi encerrado inesperadamente")
            data += packet
        except (ConnectionError, socket.error) as e:
            print(f"Erro ao receber dados: {e}")
            return None
    return data

def recv_variable_length(sock):
    """Receber uma mensagem de comprimento variável do socket."""
    # Primeiro, recebe os 4 bytes que representam o comprimento da mensagem
    data = recv_all(sock, 4)
    if data is None:
        print("Erro: Não foi possível receber o comprimento da mensagem")
        return None, 0  # Retorna None e 0 bytes recebidos

    # Descompacta o comprimento da mensagem (espera um inteiro de 4 bytes)
    try:
        (msg_len,) = struct.unpack("i", data)
    except struct.error as e:
        print(f"Erro ao descompactar o comprimento da mensagem: {e}")
        return None, 0

    # Agora, recebe a mensagem completa de comprimento `msg_len`
    message = recv_all(sock, msg_len)
    if message is None:
        print("Erro: Não foi possível receber a mensagem completa")
        return None, msg_len  # Retorna None e bytes esperados

    return message, 4 + msg_len  # Retorna a mensagem e total de bytes recebidos

def send_variable_length(sock, message):
    """Enviar uma mensagem de comprimento variável para o socket."""
    # Garante que a mensagem está em bytes
    if isinstance(message, str):
        message = message.encode('utf-8')

    msg_len = len(message)
    total_bytes_sent = 0

    try:
        # Envia o comprimento da mensagem (4 bytes, empacotados como inteiro)
        packed_len = struct.pack("i", msg_len)
        sock.sendall(packed_len)
        total_bytes_sent += len(packed_len)

        # Envia os dados reais da mensagem
        sock.sendall(message)
        total_bytes_sent += msg_len

    except socket.error as e:
        print(f"Erro ao enviar os dados: {e}")
        return False, total_bytes_sent

    return True, total_bytes_sent
