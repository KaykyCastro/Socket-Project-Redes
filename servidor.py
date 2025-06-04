import socket
import threading

HOST = '26.159.152.153'
PORT = 6060
clientes = []


try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f'Servidor {HOST}:{PORT} rodando com sucesso.')
except Exception as e:
    print(f"Ocorreu um erro ao iniciar o servidor: {e}")
    exit()

def fluxo_mensagens(mensagem, cliente_atual):
    for cliente in clientes:
        if cliente != cliente_atual:
            try:
                cliente.send(mensagem)
            except:
                cliente.close()
                if cliente in clientes:
                    clientes.remove(cliente)

def handle(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024)
            if not mensagem:
                break

            if mensagem.decode('utf-8').lower() == '/kit':
                print("Um cliente saiu do chat.")
                cliente.send('Você saiu do chat.'.encode('utf-8'))
                cliente.close()
                if cliente in clientes:
                    clientes.remove(cliente)
                break

            fluxo_mensagens(mensagem, cliente)

        except:
            if cliente in clientes:
                clientes.remove(cliente)
            cliente.close()
            break


def conexoes():
    while True:
        cliente, endereco = server.accept()
        print(f"Conexão estabelecida com {endereco}")
        clientes.append(cliente)
        thread = threading.Thread(target=handle, args=(cliente,))
        thread.start()

conexoes()
