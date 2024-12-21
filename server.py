import socket
from threading import Thread
import logging

# Настройки сервера
HOST = ''  # Слушаем все доступные интерфейсы
PORT = 5000  # Порт для подключения
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Максимум 5 подключений

clients = {}  # Словарь клиентов с никнеймами

# Настройка логирования
logging.basicConfig(filename='chat_history.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def handle_client(client_socket):
    """Обработка сообщений от клиента."""
    nickname = client_socket.recv(1024).decode('utf-8')
    clients[client_socket] = nickname
    broadcast(f"{nickname} зашёл в чат.")
    logging.info(f"{nickname} зашёл в чат.")
    
    # Отправка истории сообщений новому клиенту
    with open('chat_history.log', 'r') as f:
        history = f.read()
        client_socket.send(history.encode('utf-8'))

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == "{quit}":
                break
            
            # Формируем полное сообщение с никнеймом и логируем его.
            full_message = f"{nickname}: {message}"
            broadcast(full_message)
            logging.info(full_message)
        except:
            break

    remove(client_socket)

def broadcast(message):
    """Рассылка сообщения всем клиентам."""
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            remove(client)

def remove(client_socket):
    """Удаление клиента из списка."""
    if client_socket in clients:
        nickname = clients[client_socket]
        del clients[client_socket]
        broadcast(f"{nickname} вышел из чата.")
        logging.info(f"{nickname} вышел из чата.")

def accept_connections():
    """Принимаем входящие соединения."""
    while True:
        client_socket, addr = server_socket.accept()
        print(f"{addr} присоединился к чату.")
        Thread(target=handle_client, args=(client_socket,)).start()

print("Сервер запущен...")
accept_connections()
