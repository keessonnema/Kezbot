#!/usr/bin/python
import sqlite3


class DBHelper:

    @staticmethod
    def add_item(chat_id, chat_name):
        add_list = list((chat_id, chat_name))
        try:
            sql = '''REPLACE INTO shiftyChats (chats_id, chats_name) VALUES(?,?)'''
            CURSOR.execute(sql, add_list)
            CONN.commit()
            last_row = CURSOR.lastrowid

            return last_row
        except sqlite3.Error:
            pass

    @staticmethod
    def get_chat_count():
        try:
            CURSOR.execute("SELECT chats_id, chats_name FROM shiftyChats")
            CONN.commit()
            all_rows = CURSOR.fetchall()
            chats_id = all_rows[0]
            count_rows = len(all_rows)

            return all_rows, chats_id, count_rows
        except sqlite3.Error as er:
            print('error:', er)

    @staticmethod
    def get_chat_names():
        try:
            CURSOR.execute("SELECT chats_name FROM shiftyChats")
            CONN.commit()
            all_rows = CURSOR.fetchall()

            return all_rows
        except sqlite3.Error as er:
            print('error:', er)


CONN = sqlite3.connect('chats.db', check_same_thread=False)
CONN.execute('''CREATE TABLE IF NOT EXISTS shiftyChats 
            (chats_id int NOT NULL, 
            chats_name int NOT NULL,
            UNIQUE(chats_id));''')
CURSOR = CONN.cursor()
