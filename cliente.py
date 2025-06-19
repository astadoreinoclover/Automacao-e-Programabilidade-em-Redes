import os
import socket
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

while True:
    menu = cliente.recv(4096).decode()
    print(menu)

    opcao = input(">> ")
    cliente.sendall(opcao.encode())

    if opcao == '2':
        lista_times = cliente.recv(8192).decode()
        print(lista_times)
        escolha = input(">> ")
        cliente.sendall(escolha.encode())

        resposta = cliente.recv(8192).decode()
        print(resposta)

    else:
        resposta = cliente.recv(8192).decode()
        print(resposta)

    if "Encerrando" in resposta:
        break

cliente.close()
