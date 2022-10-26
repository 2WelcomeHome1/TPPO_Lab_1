#!/usr/bin/env python3
import socket, time
import threading as thread 

class ip_port_checker ():
    def ip_checker(ip):
        try:
            ip = str(ip)
            if len(ip) == 0:
                ip = 'localhost'
            ip_check = ip.split ('.')
            for i in ip_check:
                int(i)
        except:
            ip = 'localhost'
        return ip
    def port_checker(port):       
        try:
            port = int(port)
            if len(port) == 0:
                port = 4000
        except:
            port = 4000
        return port

print('Enter IP')
ip = input()
print ('Enter port')
port = input()

ip = ip_port_checker.ip_checker(ip)
port = ip_port_checker.port_checker(port)
print (ip, port)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
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
