#!/usr/bin/python
import sqlite3


class DBHelper:

    @staticmethod
    def add_item(chat_id, chat_name):
        add_list = list((chat_id, chat_name))
        try:
            sql = ''' REPLACE INTO shiftyChats (chats_id, chats_name) VALUES (?,?) '''
            cursor.execute(sql, add_list)
            conn.commit()
            rowId = cursor.lastrowid

            return rowId

        except sqlite3.Error:
            pass

    @staticmethod
    def get_items():
        try:
            cursor.execute("SELECT chats_id, chats_name FROM shiftyChats")
            conn.commit()
            allRecords = cursor.fetchall()
            chatsId = allRecords[0]
            countAll = len(allRecords)

            return allRecords, chatsId, countAll

        except sqlite3.Error as er:
            print('error:', er)


conn = sqlite3.connect('chats.db', check_same_thread=False)
conn.execute('''CREATE TABLE IF NOT EXISTS shiftyChats 
                (chats_id int NOT NULL, 
                chats_name int NOT NULL,
                UNIQUE(chats_id));''')

cursor = conn.cursor()
