#!/usr/bin/env python3
import socket, time
import threading as thread 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("0.0.0.0", 4000))
print ('Connected')

def receiver ():
    while True:
        try:
            message = s.recv(1024).decode()
            message = message.rstrip()
            print (message)
        except:
            break
        
def sender ():
    while True:
        cmd = input ('\n Write a command: ')
        if cmd == '/exit':
            s.send (cmd.encode())
            s.close()
            break
        s.send (cmd.encode())
        time.sleep(0.2)
        

sender = thread.Thread(target=sender)
receiver = thread.Thread(target= receiver)

receiver.start()
time.sleep(0.2)
sender.start()