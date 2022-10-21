import sqlite3

conn = sqlite3.connect('AllPersons.db')
curr = conn.cursor()
curr.execute("""CREATE TABLE IF NOT EXISTS consumer(
    userid INT PRIMARY KEY,
    fname TEXT,
    lname TEXT,
    file TEXT,
    status TEXT
    )""")
curr.execute("""CREATE TABLE IF NOT EXISTS time_tracking(
    userid INT PRIMARY KEY,
    dates DATE,
    status BIT,
    FOREIGN KEY(userid) REFERENCES consumer (userid)
    )""")
conn.commit()

if __name__ == "__main__":
    command = ""
    while command != 'end':
        command = input()
        user = ''
        if command == 'insert':  # СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ В ТАБЛИЦЕ
            print("Enter userID, fname, lname")
            user = input()
            user = user.split()
            user.append('db/identify/%s' % user[0])
            user.append('Работает')
            curr.execute("INSERT INTO consumer VALUES(?,?,?,?,?)", user)
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
        #if command == ''