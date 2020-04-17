import socket
import sys
import win32com.client as wincl
import threading
import time
import os


HOST = '192.168.1.24'
PORT = 10000


def countdown(data : str) -> None:
    speak = wincl.Dispatch('SAPI.SpVoice')
    speak.Speak(f'Attention, tu as droit à {data} minutes de jeu !')
    duration = int(data) * 60
    if duration > 300:
        time.sleep(duration - 300)
        speak.Speak(f'Attention, il te reste 5 minutes !')
        duration = 300
    time.sleep(duration - 60)
    speak.Speak(f'Attention, il ne te reste plus que 1 minute !')
    time.sleep(60)
    speak.Speak('ça va être tout noir !')
    os.system('shutdown /s /t 1')
   

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print('Starting up on {} port {}'.format(HOST, PORT))
        sock.bind((HOST, PORT))
        sock.listen(1)

        while True:
            connection, client_address = sock.accept()
            try:
                data = connection.recv(1024).decode()
                if data != '':
                    thread = threading.Thread(target=countdown, args=(data,))
                    thread.start()
                    break
            except:
                connection.close()
