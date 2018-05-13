#!/usr/bin/python
import sqlite3
import threading

lock = threading.RLock()


class DBHelper:

    def add_item(self, chat_id, chat_name):
        add_list = list((chat_id, chat_name))
        with lock:
            try:
                sql = '''REPLACE INTO shiftyChats (chats_id, chats_name) VALUES(?,?)'''
                CURSOR.execute(sql, add_list)
                CONN.commit()
                last_row = CURSOR.lastrowid

                return last_row
            except sqlite3.Error as err:
                print('error:', err)

    def get_chat_count(self):
        with lock:
            try:
                CURSOR.execute("SELECT chats_id FROM shiftyChats")
                CONN.commit()
                all_rows = CURSOR.fetchall()
                count_rows = len(all_rows)

                return count_rows
            except sqlite3.Error as err:
                print('error:', err)

    def get_chat_names(self):
        with lock:
            try:
                CURSOR.execute("SELECT chats_name FROM shiftyChats")
                CONN.commit()
                all_rows = CURSOR.fetchall()

                return all_rows
            except sqlite3.Error as err:
                print('error:', err)


CONN = sqlite3.connect('chats.db', check_same_thread=False)
CONN.execute('''CREATE TABLE IF NOT EXISTS shiftyChats 
            (chats_id int NOT NULL, 
            chats_name int NOT NULL,
            UNIQUE(chats_id));''')
CURSOR = CONN.cursor()
