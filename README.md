# TPPO_Lab_1

Сервер запускается с помощью программного комплекса Microsoft Visual Studio Code на python 3.9.7. Клиент запускается через консольное приложение командой "./tppo_client_3421.py".
Клиент можеn выполнять следующие запросы:

Команда /get fan info - Получить значения скорости и угла вращения
Команда /set speed [value] - Задать скорость вращения вентилятора (0-10 rpm) 
Команда /set angle [value] - Задать угол вращения вентилятора (0-180 deg) 
Команда /stop - Выключить вентилятор 
Команда /help - Получить список всех команд
Команда /exit - отключиться от сервера

Помимо данных запросов, существуют скрытые, доступные только для администратора сети.
Для этого выполняется запрос "/admin 1111", где 1111 - это пароль.  После чего клиент получает доступ к следующим командам:
Команда /log off - Выключить сбор логов
Команда /log on - Включить сбор логов
Команда /get log - Получить информацию из файла логов

Сборка файла логов включена автоматически. Создание исполнительного файла так же происходит автоматически

Для успешной работы проекта необходимы следующие библиотеки:

import socket, re, os, time, logging

import pandas as pd

from watchdog.observers import Observer

from watchdog.events import FileSystemEventHandler

import threading as thread
