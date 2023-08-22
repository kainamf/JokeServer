import socket
import threading
import random
from queue import Queue

ip = '127.0.0.1'
porta = 2000
capacidade_teatro = 10
limite_fila = 5

# Lista de piadas
jokes = [
    "Por que o programador atravessou a rua? Para chegar ao outro lado da API.",
    "Qual é o objeto mais engraçado? O riso-cachorro.",
    "O que um elevador falou para o outro? Eu acho que estou chegando a uma fase difícil.",
    "O que aconteceu quando a geladeira foi para a terapia? Ela percebeu que estava guardando muita bagagem emocional.",
    "Por que o esqueleto não brigou com ninguém? Ele não tinha estômago para isso.",
    "Qual é o cúmulo da rapidez? Dar um beijo na boca e já estar pensando no casamento.",
    "Por que o livro de matemática estava triste? Porque tinha muitos problemas.",
    "O que uma impressora disse à outra? Essa folha é sua ou é uma impressão minha?",
    "Por que o aluno de música sempre estava calmo? Porque ele sabia lidar bem com as notas.",
    "Qual é o cúmulo da paciência? Ensinar libras para um surdo-mudo por telefone.",
    "O que o zero disse para o oito? 'Uau, seu cinto está bem apertado!'",
    "O que aconteceu com o carro quando ele chegou ao hospital? Ele foi engessado.",
    "O que o celular disse para o carregador? 'Você me acende.'",
    "Por que o lápis entrou na escola? Para melhorar a escrita.",
    "Qual é o cúmulo da rapidez? Tomar um refrigerante de lata com canudo.",
    "Por que o banheiro estava correndo? Porque estava com pressa para o número 2.",
    "O que o pé esquerdo falou para o pé direito? Nada, eles não se encontram.",
    "O que a galinha foi fazer na igreja? Assistir à missa do galo.",
    "Por que a vassoura estava cansada? Porque ela estava sempre varrendo o assunto.",
    "Qual é o cúmulo do cinema? Roubar o show.",
    "Por que a vaca foi para o espaço? Para encontrar o vácuo.",
    "O que a aranha disse para a mosca? Pode entrar, a casa é sua!",
    "Por que o computador não está feliz? Porque ele perdeu o bit da alegria.",
    "O que o advogado do frango foi fazer na delegacia? Foi soltar a franga.",
    "Por que o tigre não gosta de ir à escola? Porque ele tem medo do boletim.",
    "O que o queijo falou para o queijo ralado? 'Pare de me esfolar!'",
    "Qual é o cúmulo da maldade? Colocar uma pessoa idosa no micro-ondas e fazer um vovô-tel.",
    "O que o espermatozoide disse para o óvulo? Deixa eu morar com você porque a minha casa é um saco.",
    "O que uma pilha falou para a outra? 'Você é meu único motivo para viver.'",
    "Por que o livro de matemática estava triste? Porque tinha muitos problemas.",
    "Qual é o cúmulo do esquecimento? Esquecer o próprio aniversário.",
    "Por que a bicicleta foi para a terapia? Porque estava cansada de ser usada.",
    "O que o peixe disse quando bateu numa parede? 'Droga!'",
    "O que a água foi fazer no bar? Foi tomar um drinque.",
    "Qual é o cúmulo do alcoolismo? Tomar um porre d'água.",
    "Por que a planta não foi ao médico? Porque ela já estava bem enraizada.",
    "O que o caracol disse quando foi atropelado? 'Vou chamar a polícia, você está na minha casa!'",
    "Qual é o cúmulo da magreza? Comer uma azeitona e se afogar.",
    "O que um semáforo disse para o outro? 'Não olhe, estou mudando de roupa.'",
    "Por que a lua não usa Instagram? Porque ela quer ficar fora do foco.",
    "Qual é o cúmulo da força? Quebrar um espelho com a própria imagem.",
    "Por que o avião não pode ser amigo do helicóptero? Porque ele sempre decola a amizade.",
    "O que a caneta disse para o lápis? 'Você é muito legal, mas você não tem a minha classe.'",
    "Qual é o cúmulo da tristeza? Fazer palhaçada e ninguém rir.",
    "Por que o elefante não pega fogo? Porque já é cinza.",
    "O que o pão falou para o queijo? 'Vai na frente que eu estou seguindo.'",
    "Por que o computador não sai de casa? Porque tem medo do mouse.",
    "Qual é o cúmulo da preguiça? Mandar o cachorro latir por você.",
    "O que uma impressora disse para a outra? 'Essa folha é sua ou é uma impressão minha?'",
    "Por que a impressora não falou com ninguém? Porque ela não tem papel.",
    "O que aconteceu com o livro de matemática? Ele tirou muitos zeros.",
    "Por que o esqueleto não brigou com ninguém? Porque não tinha estômago para isso.",
    "Qual é o cúmulo da rapidez? Dar um beijo na boca e já estar pensando no casamento.",
    "O que um vaso disse para o outro? 'Você é muito bonito, mas vive cheio de frescura.'",
    "Qual é o cúmulo da força? Quebrar o vento com um soco.",
    "Por que o jogador de futebol foi ao banco? Trocar o seu Real.",
    "O que aconteceu com o nariz vermelho? Ficou bêbado de sangue.",
    "Por que o quadro ficou vermelho? Porque ele viu o boi passando no campo.",
]

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

# Função que retorna lista de cadeiras disponíveis
def available_chairs(teatro):
    return [i for i in range(1, capacidade_teatro + 1) if i not in teatro]



"""
Função para lidar com a comunicação entre o servidor e um cliente conectado.
    Args:
        conn (socket object): Objeto de conexão do cliente.
        addr (tuple): Tupla contendo o endereço IP e porta do cliente.
        teatro (list): Lista de cadeiras ocupadas no teatro.
        fila (Queue): Fila de espera para os clientes.
"""
def handle_client(conn, addr, teatro, fila):
    print(f'Conexão estabelecida com {addr}')
    conn.sendall("Bem-vindo ao Teatro de Piadas! Escolha uma cadeira de 1 a 10 ou digite 'sair' para encerrar.\n".encode('utf-8'))

    while True:
        msg = conn.recv(1024)
        if not msg:
            break  # Encerra a conexão se não houver mensagem

        msg = msg.decode('utf-8').strip()

        if msg.lower() == "sair":
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
                    send_jokes(conn)
                    send_riddle(conn)
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





def send_jokes(conn):
    random.shuffle(jokes)
    for i in range(5):
        conn.sendall(jokes[i].encode('utf-8') + b'\n')
        conn.recv(1024)  # Aguarda a confirmação do cliente

def send_riddle(conn):
    riddle, answer = random.choice(riddles)
    conn.sendall(f"Charada: {riddle}\n".encode('utf-8'))
    conn.recv(1024)  # Aguarda a confirmação do cliente
    conn.sendall(f"Resposta: {answer}\n".encode('utf-8'))

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
