import socket
import threading
import random
from queue import Queue

ip = '127.0.0.1'
porta = 2000
capacidade_teatro = 10
limite_fila = 5

# Lista de charadas
riddles = [                         
    ("O que é, o que é: quanto mais se tira, maior ele fica?", "O buraco"),
    ("O que é, o que é: tem chaves mas não abre portas?", "O piano"),
    ("O que é, o que é: nunca está completo de dia, nem de noite?", "O céu"),
    ("O que é, o que é: tem quatro patas e um braço?", "Um cavalo e um homem"),
    ("O que é, o que é: nunca volta, mesmo quando é devolvido?", "O passado"),
    ("O que é, o que é: todos têm, mas ninguém pode perder?", "Um reflexo"),
    ("O que é, o que é: vai e volta sem se mover?", "O vento"),
    ("O que é, o que é: sempre cresce e nunca envelhece?", "A árvore"),
    ("O que é, o que é: tem coroa e não é rei; tem escamas e não é peixe?", "O abacaxi"),
    ("O que é, o que é: atravessa a cidade sem mover um pé?", "A rua"),
    ("O que é, o que é: está no começo do livro e no fim do filme?", "A letra 'V'"),
    ("O que é, o que é: tem asas e não é pássaro; tem coroa e não é rei?", "A abelha"),
    ("O que é, o que é: é seu, mas outras pessoas usam mais?", "Seu nome"),
    ("O que é, o que é: sempre fica molhado, mesmo que não chova?", "O peixe"),
    ("O que é, o que é: tem cabeça e cauda, mas não tem corpo?", "A moeda"),
    ("O que é, o que é: quanto mais se tira, mais se enche?", "O furo"),
    ("O que é, o que é: é preto quando compra, vermelho quando usa e cinza quando joga fora?", "O carvão"),
    ("O que é, o que é: se joga na parede e não quebra?", "A sombra"),
    ("O que é, o que é: está no início da rua e no fim do horizonte?", "A letra 'U'"),
]

def available_chairs(teatro):
    """ 
    Retorna lista de cadeiras disponíveis
    """
    return [i for i in range(1, capacidade_teatro + 1) if i not in teatro]


def handle_client(conn, addr, teatro, fila):
    """
    Função para lidar com a comunicação entre o servidor e um cliente conectado.
    Args:
        conn (socket object): Objeto de conexão do cliente.
        addr (tuple): Tupla contendo o endereço IP e porta do cliente.
        teatro (list): Lista de cadeiras ocupadas no teatro.
        fila (Queue): Fila de espera para os clientes.
    """
    print(f'Conexão estabelecida com {addr}')
    conn.sendall("Bem-vindo ao Teatro de Piadas! Escolha uma cadeira de 1 a 10 ou digite 'sair' para encerrar.\n".encode('utf-8'))

    while True:
        msg = conn.recv(1024)
        if not msg:
            break  # Encerra a conexão se não houver mensagem

        msg = msg.decode('utf-8').strip()

        if msg.lower() == "sair":
            break
        elif msg.lower() == "sim":
            more_riddles = send_riddles(conn)
            if not more_riddles:
                conn.sendall("Obrigado por participar do Teatro de Piadas. Adeus!\n".encode('utf-8'))
                break
        elif msg.isdigit():
            chair_number = int(msg)
            available_chairs_list = available_chairs(teatro)  # Obtem a lista de cadeiras disponíveis

            if 1 <= chair_number <= 10:
                if chair_number in teatro:
                    conn.sendall(f"A cadeira {chair_number} está indisponível. Cadeiras disponíveis: {', '.join(map(str, available_chairs_list))}\n".encode('utf-8'))
                elif len(teatro) < capacidade_teatro:
                    teatro.append(chair_number)
                    conn.sendall(f"Você está na cadeira {chair_number}. Digite qualquer tecla para começar o show!\n".encode('utf-8'))
                    conn.recv(1024)  # Aguarda a confirmação do cliente
                    conn.sendall("O show está começando!\n".encode('utf-8'))
                    send_riddles(conn)
                    if msg.lower() == "sair":
                        break
                    teatro.remove(chair_number)
                    if not fila.empty():
                        next_user = fila.get()
                        conn.sendall(f"Você foi direcionado da fila para a cadeira {next_user}.\n".encode('utf-8'))
                else:
                    if fila.qsize() < limite_fila:
                        fila.put(chair_number)
                        conn.sendall(f"O teatro está cheio. Você está na fila de espera com o número {fila.qsize()}.\n".encode('utf-8'))
                    else:
                        conn.sendall("Estamos lotados no momento, por favor volte mais tarde, desculpe pelo transtorno!\n".encode('utf-8'))
            else:
                conn.sendall("Cadeira inválida. Escolha uma cadeira de 1 a 10 ou digite 'sair' para encerrar.\n".encode('utf-8'))
        else:
            conn.sendall("Comando inválido. Escolha uma cadeira de 1 a 10 ou digite 'sair' para encerrar.\n".encode('utf-8'))

    print(f'Conexão encerrada com {addr}')
    conn.close()

# Lista de Charadas
def send_riddles(conn):
    while True:
        random.shuffle(riddles)
        selected_riddles = random.sample(riddles, 5)  # Seleciona aleatoriamente 5 charadas
        for i, (riddle, answer) in enumerate(selected_riddles, start=1):
            conn.sendall(f"Charada {i}: {riddle}\n".encode('utf-8'))
            conn.recv(1024)  # Aguarda a confirmação do cliente
            conn.sendall(f"Resposta {i}: {answer}\n".encode('utf-8'))

            # Aguarda a resposta do usuário
            user_response = conn.recv(1024).decode('utf-8').strip()

            # Verifica se o usuário deseja sair
            if user_response.lower() == "sair":
                conn.sendall("Obrigado por participar do Teatro de Piadas. Adeus!\n".encode('utf-8'))
                conn.close()  # Fecha a conexão
                return False

        # Após as 5 charadas, pergunta ao usuário se ele quer ouvir mais charadas ou sair.
        conn.sendall("Deseja ouvir mais charadas? (Digite 'sim' para mais charadas ou 'sair' para encerrar)\n".encode('utf-8'))
        user_choice = conn.recv(1024).decode('utf-8').strip()

        if user_choice.lower() == "sair":
            conn.close()  # Fecha a conexão
            return False
        elif user_choice.lower() != "sim":
            conn.sendall("Opção inválida. Por favor, digite 'sim' para mais charadas ou 'sair' para encerrar.\n".encode('utf-8'))
            
        # Loop para esperar uma resposta válida
            while True:
                user_choice = conn.recv(1024).decode('utf-8').strip()
                if user_choice.lower() == "sim" or user_choice.lower() == "sair":
                    break
                conn.sendall("Opção inválida. Por favor, digite 'sim' para mais charadas ou 'sair' para encerrar.\n".encode('utf-8'))
    return True



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binda o socket a uma porta
server.bind((ip, porta))

# Fila de espera
fila_espera = Queue()

# Lista de cadeiras no teatro
cadeiras_teatro = []

# Fica escutando por conexões
server.listen()

print(f"Servidor escutando em {ip}:{porta}")

while True:
    conn, addr = server.accept()

    # Cria uma nova thread para lidar com o cliente
    client_thread = threading.Thread(target=handle_client, args=(conn, addr, cadeiras_teatro, fila_espera))
    client_thread.start()
