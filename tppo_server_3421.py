import socket, re, os, time, logging
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading as thread
from threading import Thread 

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print("on_created", event.src_path)
        try:
            logging.info ('Handler message: File has been created')
            sock.send ('\nFile has been created'.encode())
        except Exception as e:
            logging.exception (e)
            pass
    def on_deleted(self, event):
        print("on_deleted", event.src_path)
        logging.info ('Handler message: File has been deleted')
        sock.send ('\nFile has been deleted'.encode())
    def on_modified(self, event):
        print("on_modified", event.src_path)
        logging.info ('Handler message: File has been modified')
    def on_moved(self, event):
        print("on_moved", event.src_path)
        logging.info ('File has been moved')
        sock.send ('\nFile has been moved'.encode())
class fan_config ():
    def create_fan_file(self, speed, angle):
        params = {'Speed': [speed], 'Angle': [angle]}
        df = pd.DataFrame (params)
        df = df.set_index ('Speed')
        df.to_xml('fan.xml')
        logging.info ('Create fan file: File has been created')
        print ('File has been created')
    def get_fan_info(self):
        
        data = pd.read_xml ('fan.xml')
        speed = data.loc[0,'Speed']
        angle = data.loc[0,'Angle']

        return angle, speed 
    def set_speed(self, speed):
        data = pd.read_xml ('fan.xml')
        data.loc[0,'Speed'] = speed
        try:
            data = data.drop(["level_0"], axis = 1)
        except Exception as e:
            logging.error (e)
            pass
        data.to_xml('fan.xml')
        logging.info ('New speed accepted')
    def set_angle(self, angle):
        data = pd.read_xml ('fan.xml')
        data.loc[0,'Angle'] = angle
        try:
            data = data.drop(["level_0"], axis = 1)
        except Exception as e:
            logging.error (e)
            pass
        data.to_xml('fan.xml')
        logging.info ('New angle accepted')
    def check_fan(self):
        if not os.path.exists('./fan.xml'):
            current_speed = 0
            current_angle = 90
            logging.info ('File fan not exist')
            self.create_fan_file(current_speed, current_angle)
        else:
            angle, speed = self.get_fan_info()
            logging.info ('Fan file:ready')
            print ('Fan ready to use\n', 
                'Current speed: ' + str(speed) + ' rpm\n', 
                'Current angle: ' + str(angle)+ ' deg')
class fan_cycle ():
    def check_fan_info():
        angle, speed = fan.get_fan_info()
        message = str ('\nCurrent speed: ' + str(speed) + ' rpm\n' + 'Current angle: ' + str(angle)+ ' deg')
        sock.send (message.encode())
        logging.info (message)
    def set_speed_info(res):
        try:
            res = int(res[0])
            if res <= 10 and res >= 0:
                speed = res
                fan.set_speed(speed)
                angle, speed = fan.get_fan_info()
                message = str ('\nCurrent speed: '+ str(speed) + ' rpm\n' + 'Current angle: ' + str(angle)+ ' deg')
                sock.send (message.encode())
                logging.info (message)
            else:
                logging.warning('Incorrect speed value')
                message = '\nSorry incorrect value'
                sock.send (message.encode())
        except Exception as e:
            logging.error(e)
            logging.warning('Incorrect speed value')
            message = '\nSorry incorrect value'
            sock.send (message.encode())
    def set_angle_info(res):
        try:
            res = int(res[0])
            if res <= 180 and res >= 0:
                angle = res
                fan.set_angle(angle)
                angle, speed = fan.get_fan_info()
                message = str ('\nCurrent speed: ' + str(speed) + ' rpm\n' + 'Current angle: ' + str(angle)+ ' deg')
                sock.send (message.encode())
                logging.info (message)
            else:
                message = '\nSorry incorrect value'
                logging.warning('Incorrect angle value')
                sock.send (message.encode())
        except Exception as e:
            logging.error(e)
            logging.warning('Incorrect angle value')
            message = '\nSorry incorrect value'
            sock.send (message.encode())
    def stop():
        speed = 0
        fan.set_speed (speed)
        message = '\nFan stopped'
        sock.send (message.encode())
        logging.info (message)
    def help():
        message = "\nКоманда /get fan info - Получить значения скорости и угла вращения\nКоманда /set speed [value] - Задать скорость вращения вентилятора (0-10 rpm) \nКоманда /set angle [value] - Задать угол вращения вентилятора (0-180 deg) \nКоманда /stop - Выключить вентилятор \nКоманда /help - Получить список всех команд\nКоманда /exit - отключиться от сервера" 
        sock.send (message.encode())
    def log_fil_func (res):
        if res[0] == 'on':
            logger = logging.getLogger()
            logger.disabled = False
            message = '\nLogging enabled'
            sock.send (message.encode())
            logging.info (message)
        elif res[0] == 'off':
            logger = logging.getLogger()
            logger.disabled = True
            message = '\nLogging disabled (only warnings and errors)'
            sock.send (message.encode())
            logging.info (message)
    def send_log ():
        f = open('log.log', 'r')
        str_number = len(open('log.log').readlines())
        log_list = []
        for line in f:
            log_list.append(line)
        for message in log_list[str_number-10:str_number]:
            sock.send(str(message).encode())
        logging.info ('Client asked log info')
    def admin_panel(res):
        if res[0] == '1111':
            message = "\nКоманда /log off - Выключить сбор логов\nКоманда /log on - Включить сбор логов\nКоманда /get log - Получить информацию из файла логов" 
            sock.send (message.encode())
            logging.info ('Admin is here')
        else:
            message = "\nIncorrect password" 
            sock.send (message.encode())
            logging.info ('Incorrect Admin password')
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
def check_file():
    speed_list = []
    angle_list = []
    while True:
        try:
            data = pd.read_xml ('fan.xml')
            speed = data.loc[0,'Speed']
            speed_list.append (speed)
            angle = data.loc[0,'Angle']
            angle_list.append(angle)
            try:
                if angle_list[-1] != angle_list[-2]:
                    message =  str('\nAngle has been changed. Previous parameter: ' + str(angle_list[-2]) + 'deg.' + ' Now: ' + str (angle_list[-1]) + 'deg')
                    sock.send (message.encode())
    #                 break
                if speed_list[-1] != speed_list[-2]:
                    message  = str('\nSpeed has been changed. Previous parameter: ' + str(speed_list[-2]) + 'rpm.' + ' Now: ' + str(speed_list[-1])+ 'rpm.')
                    sock.send (message.encode())
    #                 break
            except:
                pass
            if len(speed_list) >5:
                del speed_list [:4]
            if len(angle_list) >5:
                del angle_list[:4]
        except:
            pass            

## Create a log file ##
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'log.log')

## Create a fan file ##
fan = fan_config()
fan.check_fan()

## Create a socket ##
print('Enter IP')
ip = input()
print ('Enter port')
port = input()
ip = ip_port_checker.ip_checker(ip)
port = ip_port_checker.port_checker(port)
print (ip, port)


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    print ("Working ...")
    s.listen(5)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except Exception as e:
    logging.exception(e)


## Create an observer ##
observer = Observer()
observer.schedule(MyHandler(), path='./fan.xml', recursive=True)
observer.start()

clients = set()
clients_lock = thread.Lock()

## Start file checker##
check_file_th = Thread (target = check_file, args = ())
check_file_th.start ()

## Start a cycle ##
while True:
    sock, addr = s.accept()
    print ('Get connected ', addr)
    logging.info ('Client has connected ' + str(addr))
    pid = os.fork()
    if pid != 0:
        continue
    while True:

        try:
            content = "If you don't know what to do - write '/help'". encode()
            sock.send (content)
            line = sock.recv(1024).decode()
            line = line.rstrip()
            # Check fan file
            if not os.path.exists('./fan.xml'):
                logging.info ('Fan file not exist. Start creating')
                current_speed = 0
                current_angle = 90
                fan.create_fan_file(current_speed, current_angle)
                     
            # Check fan info
            if re.findall(r"/get fan info", line):
                print(re.findall(r"/get fan info", line))
                logging.info ('Get "/get fan info" command')
                fan_cycle.check_fan_info()

            # Set speed
            elif re.findall(r"/set speed (\w+)", line):
                res = re.findall(r"/set speed (\w+)", line)
                print(res)
                logging.info ('Get "/set speed" command with value ' + str(res[0]))
                fan_cycle.set_speed_info(res)
                
            # Set angle
            elif re.findall(r"/set angle (\w+)", line):
                res = re.findall(r"/set angle (\w+)", line)
                print(res)
                logging.info ('Get "/set angle" command with value ' + str(res[0]))
                fan_cycle.set_angle_info(res)
            
            # Stop
            elif  re.findall(r"/stop", line):
                print(re.findall(r"/stop", line))
                logging.info ('Get "/stop" command ')
                fan_cycle.stop()
        
            # Help
            elif re.findall(r"/help", line):
                print(re.findall(r"/help", line))
                logging.info ('Get "/help" command ')
                fan_cycle.help()
            
            # Exit
            elif re.findall(r"/exit", line):
                print(re.findall(r"/exit", line))
                logging.info ('Get "/exit" command. Client went out ')
                print ('Client went out ')
                sock.close()
                break

            ## En/Disable a log file ##
            elif re.findall(r"/log (\w+)", line):
                print (re.findall(r"/log (\w+)", line))
                res = re.findall(r"/log (\w+)", line)
                logging.info ('Get "/log"' + str(res[0]) + 'command ')
                fan_cycle.log_fil_func(res)
            
            ## Get log file ##
            elif re.findall(r"/get log", line):
                print (re.findall(r"/get log", line))
                logging.info ('Get "/get" log command ')
                fan_cycle.send_log()
            
            ## Admin panel ##
            elif re.findall(r"/admin (\w+)", line):
                print (re.findall(r"/admin (\w+)", line))
                res = re.findall(r"/admin (\w+)", line)
                logging.info ('Get "/admin" command with pass value: ' +  str(res[0]))
                fan_cycle.admin_panel(res)
            
            # Check command
            else:
                print ('Incorrect command')
                logging.warning ('Incorrect command')
                message = '\nSorry, No such command'
                sock.send (message.encode())
            
            logging.info ('Everything is ok')
            time.sleep(0.1)
        except Exception as e:
            logging.exception (e)
