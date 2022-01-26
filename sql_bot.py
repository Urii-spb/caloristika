import sqlite3

DB = 'daily_food.db'

def insert_menu(date, course_0, course_1, course_2, course_3):  # записываем еду в базу
    if not(select_menu(date)):
        try:
            condb = sqlite3.connect(DB)
            cursor = condb.cursor()

            sql_insert = """INSERT INTO date_menu
                                      (date, course_0, course_1, course_2, course_3)
                                  VALUES (?, ?, ?, ?, ?);"""

            data_tuple = (date, course_0, course_1, course_2, course_3)
            cursor.execute(sql_insert, data_tuple)
            condb.commit()

            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)


def select_menu(date):  # получаем еду из базы по дате
    try:
        condb = sqlite3.connect(DB)
        cursor = condb.cursor()

        sql_query = """SELECT course_0, course_1, course_2, course_3 FROM date_menu
                              WHERE date = ?;"""

        cursor.execute(sql_query, (date,))
        record = cursor.fetchall()

        cursor.close()
        return(record)

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
 