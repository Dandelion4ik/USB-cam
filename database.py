import sqlite3
from datetime import date
from itertools import islice
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
from xlsxwriter import Workbook

import pandas as pd

import openpyxl as ox
import shutil
import cv2

from openpyxl import load_workbook

conn = sqlite3.connect('AllPersons.db')
curr = conn.cursor()
curr.execute("""CREATE TABLE IF NOT EXISTS consumer(
    userid INT PRIMARY KEY,
    fname TEXT,
    lname TEXT,
    post TEXT,
    file TEXT,
    status TEXT
    )""")
curr.execute("""CREATE TABLE IF NOT EXISTS time_tracking(
    userid INT,
    dates DATE,
    status BIT
    )""")
conn.commit()

if __name__ == "__main__":
    command = ""
    while command != 'end':
        command = input()
        user = ''
        if command == 'insert':  # СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ В ТАБЛИЦЕ
            print("Enter userID, fname, lname, post")
            user = input()
            user = user.split()
            user.append('db/identify/%s' % user[0])
            user.append('Работает')
            curr.execute("INSERT INTO consumer VALUES(?,?,?,?,?,?)", user)
            conn.commit()
        if command == 'delete':  # УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ ИЗ ТАБЛИЦЫ
            print("Enter userID")
            user = input()
            curr.execute("DELETE FROM consumer WHERE consumer.userid = ?", user)
            conn.commit()
        if command == 'status':  # ОБНОВИТЬ СТАТУС РАБОТНИКА
            print("Enter userID")
            userID = input()
            print("Enter status")
            user_status = input()
            curr.execute("UPDATE consumer SET status = ? WHERE consumer.userid = ?",
                         (user_status, userID))
            conn.commit()
        if command == 'tabel':
            print("Enter userID")
            userID = input()
            try:
                curr.execute("SELECT userid FROM consumer WHERE userid = ?", userID)
            except:
                print('userID not found')
                continue
            shutil.copyfile('Tabel.xlsx',
                            'db/Tabels/%sTabel.xlsx' % str(userID))  # CКОПИРОВАЛИ НЕЗАПОЛНЕННЫЙ ТАБЕЛЬ В ПАПКУ ЮЗЕРА
            wb = ox.load_workbook('db/Tabels/%sTabel.xlsx' % str(userID))
            # НОМЕР ТАБЕЛЯ
            wb['стр.1'].cell(1, 79).value = userID
            # ПЕРИОД
            wb['стр.1'].cell(4, 70).value = '30'
            wb['стр.1'].cell(4, 77).value = 'Ноября'
            wb['стр.1'].cell(4, 100).value = '22'
            # УЧРЕЖДЕНИЕ
            wb['стр.1'].cell(5, 25).value = 'МГТУ им. Баумана'
            # СТРУКТУРНОЕ ПОДРАЗДЕЛЕНИЕ
            wb['стр.1'].cell(6, 25).value = 'ИУ8-73'
            # ВИД ТАБЕЛЯ
            wb['стр.1'].cell(7, 25).value = 'Первичный'
            # СТАТИСТИКА РАБОЧИХ ДНЕЙ ИЗ БД
            curr.execute("""select dates, status from time_tracking where userid = ?""", userID)
            statistic_days = curr.fetchall()
            half_day_cof = 0
            count_working_day = 0
            for i in statistic_days:
                if i[0] == 16:
                    half_day_cof = 7
                    wb['стр.1'].cell(13, 94).value = count_working_day
                if i[1]:
                    count_working_day += 1
                wb['стр.1'].cell(13, 34 + (int(i[0]) - 1) * 4 + half_day_cof).value = i[1]
            wb['стр.1'].cell(13, 165).value = count_working_day
            # ИМЯ ФАМИЛИЯ ДОЛЖНОСТЬ ID
            curr.execute("""select fname from consumer where userid = ?""", userID)
            fname = curr.fetchall()
            curr.execute("""select lname from consumer where userid = ?""", userID)
            lname = curr.fetchall()
            curr.execute("""select post from consumer where userid = ?""", userID)
            post = curr.fetchall()
            wb['стр.1'].cell(13, 1).value = fname[0][0] + ' ' + lname[0][0]
            wb['стр.1'].cell(13, 25).value = post[0][0]
            wb['стр.1'].cell(13, 13).value = userID
            # ДАТА ФОРМИРОВАНИЯ ДОКУМЕНТА
            wb['стр.1'].cell(8, 157).value = date.today()

            wb.save('db/Tabels/%sTabel.xlsx' % str(userID))
