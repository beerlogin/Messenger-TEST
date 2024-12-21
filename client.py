import socket
from threading import Thread
import tkinter as tk
from tkinter import scrolledtext

# Настройки клиента
HOST = input("Введите адрес сервера: ")  # Адрес сервера
PORT = 5000  # Порт сервера
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Запрашиваем никнейм у пользователя
nickname = input("Введите ваш никнейм: ")
client_socket.send(nickname.encode('utf-8'))  # Отправляем никнейм на сервер

# Функция для получения сообщений от сервера
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                msg_list.config(state=tk.NORMAL)  # Разрешаем редактирование текстового поля
                msg_list.insert(tk.END, message + '\n')  # Вставляем сообщение
                msg_list.config(state=tk.DISABLED)  # Запрещаем редактирование текстового поля
                msg_list.yview(tk.END)  # Прокручиваем вниз
            else:
                break
        except Exception as e:
            print("Ошибка при получении сообщения:", e)
            client_socket.close()
            break

# Функция для отправки сообщений на сервер
def send(event=None):
    msg = my_msg.get()
    if msg:  # Проверяем, что сообщение не пустое
        if msg.lower() == "{quit}":
            client_socket.send(bytes("{quit}", "utf-8"))
            client_socket.close()
            top.quit()
        else:
            full_message = f"{msg}"  # Формируем полное сообщение без никнейма
            client_socket.send(bytes(full_message, "utf-8"))  # Отправляем только сообщение без ника
            my_msg.set("")  # Очищаем поле ввода

# Функция для закрытия приложения
def on_closing():
    my_msg.set("{quit}")
    send()

# Создаем главное окно
top = tk.Tk()
top.title("Чат")

# Создаем текстовое поле для отображения сообщений
msg_list = scrolledtext.ScrolledText(top, state=tk.DISABLED)
msg_list.pack(padx=10, pady=10)

# Создаем поле ввода для сообщений
my_msg = tk.StringVar()  # Переменная для хранения текста сообщения
entry_field = tk.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack(padx=10, pady=10)

# Создаем кнопку отправки сообщений
send_button = tk.Button(top, text="Отправить", command=send)
send_button.pack(pady=5)

top.protocol("WM_DELETE_WINDOW", on_closing)

# Запускаем поток для получения сообщений
Thread(target=receive_messages).start()

# Запускаем главный цикл приложения
tk.mainloop()
