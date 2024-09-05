import sqlite3

import old_numbers
            # Открываем соединение с базой данных
with sqlite3.connect('old_number.db') as con:
    cur = con.cursor()
    
    # Убедитесь, что таблица существует
    cur.execute('CREATE TABLE IF NOT EXISTS numbers (old TEXT)')
    
    for i in old_numbers.used_numbers:
        num = i[0]# Вставляем номер в таблицу
        cur.execute('INSERT INTO numbers (old) VALUES (?)', (num,))
    
    # Сохраняем изменения
    con.commit()
    print('Номер сохранен')