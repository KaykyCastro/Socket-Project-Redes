import socket
import threading

HOST = '26.159.152.153'
PORT = 6060
nome = input('Digite seu nome: ')
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente.connect((HOST,PORT))
    print("Cliente conectado ao servidor com sucesso!")
except ConnectionRefusedError:
    print(f"Não foi possível estabelecer conexão com o servidor {HOST}:{PORT}")
    exit()
except Exception as e:
    print(f"Houve um erro: {e}")
    exit()

def receber_mensagem():
    while True:
        try:
            mensagem = cliente.recv(1024).decode('utf-8')
            if not mensagem:
                print("Conexão encerrada pelo servidor!")
                cliente.close()
                break
            print(mensagem)
        except:
            print("Aconteceu um erro inesperado ao receber mensagens.")
            cliente.close()
            break

def enviar_mensagem():
    while True:
        try:
            mensagem = nome + ": " + input('')
            if mensagem.lower() == "/kit":
                cliente.send(mensagem.encode('utf-8'))
                cliente.close()
                print("Você saiu do chat.")
                break
            cliente.send(mensagem.encode('utf-8'))
        except:
            print("Erro ao enviar mensagem. Encerrando conexão.")
            cliente.close()
            break

thread_receber = threading.Thread(target=receber_mensagem)
thread_receber.start()

thread_enviar = threading.Thread(target=enviar_mensagem)
thread_enviar.start()
