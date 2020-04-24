#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
from threading import Lock

lock= Lock()
class DBHelper:

    def __init__(self, dbname="main.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False,timeout=20)
        self.c = self.conn.cursor()

    def setup(self):
        tbl_sessions ="""CREATE TABLE IF NOT EXISTS live_sessions(id INTEGER PRIMARY KEY,sess_id INTEGER DEFAULT NULL ,group_language VARCHAR DEFAULT NULL ,bot VARCHAR DEFAULT NULL ,lesson VARCHAR DEFAULT NULL,each_time INTEGER DEFAULT NULL ,total_time INTEGER DEFAULT NULL,
                      start_time TIMESTAMP DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,questions INTEGER DEFAULT NULL,session_name VARCHAR DEFAULT NULL,status INTEGER DEFAULT 0)"""
        tbl_groups ="""CREATE TABLE IF NOT EXISTS bot_groups(id INTEGER PRIMARY KEY,groupId INTEGER DEFAULT NULL,groupTitle VARCHAR DEFAULT NULL,token VARCHAR DEFAULT NULL,groupLanguage VARCHAR DEFAULT NULL,botUsername VARCHAR DEFAULT NULL,link VARCHAR DEFAULT NULL )"""
        tbl_apollo ="""CREATE TABLE IF NOT EXISTS apollo(id INTEGER PRIMARY KEY,sess_id INTEGER DEFAULT NULL,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,groupId INTEGER DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,messageId INTEGER DEFAULT 0,bot VARCHAR DEFAULT NULL,status INTEGER DEFAULT 0)"""
        tbl_chances ="""CREATE TABLE IF NOT EXISTS chances(id INTEGER PRIMARY KEY,userId INTEGER DEFAULT NULL ,tries INTEGER DEFAULT 0,bot DEFAULT NULL,messageId INTEGER DEFAULT NULL )"""
        tbl_correct ="""CREATE TABLE IF NOT EXISTS correct(id INTEGER PRIMARY KEY,messageId INTEGER DEFAULT NULL,students INTEGER DEFAULT 0)"""
        self.c.execute(tbl_sessions)
        self.c.execute(tbl_groups)
        self.c.execute(tbl_apollo)
        self.c.execute(tbl_chances)
        self.c.execute(tbl_correct)
        self.conn.commit()
        #"""Sessions"""

    def check_session(self,sess_id):
        self.c.execute("SELECT sess_id FROM live_sessions WHERE sess_id=?", (sess_id,))
        sess = self.c.fetchone()
        if sess is not None:
            return True
        else:
            return False

    def save_sessions(self,sess_id,group_language,bot,lesson,each_time,total_time,start_time,qlevel,questions,session_name,status):
        if self.check_session(sess_id=sess_id)!=True:
            self.c.execute("INSERT INTO live_sessions(sess_id,group_language,bot,lesson,each_time,total_time,start_time,qlevel,questions,session_name,status) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (sess_id,group_language,bot,lesson,each_time,total_time,start_time,qlevel,questions,session_name,status))
            self.conn.commit()


    '''Bot Group'''
    def check_bot(self,groupId):
        self.c.execute("SELECT groupId FROM bot_groups WHERE groupId=?", (groupId,))
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_bot(self,groupId,groupTitle,token,groupLanguage,botUsername,link):
        if self.check_bot(groupId)==False:
            self.c.execute("INSERT INTO bot_groups(groupId,groupTitle,token,groupLanguage,botUsername,link) VALUES (?,?,?,?,?,?)",(groupId,groupTitle,token,groupLanguage,botUsername,link))
            self.conn.commit()

    def get_bot(self,language):
        self.c.execute("SELECT * FROM bot_groups WHERE groupLanguage=?", (language,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]


    """questions"""
    """1. Apollo"""
    def check_apollo(self,queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM apollo WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False


    def save_apollo(self,sess_id ,quesId ,question ,answer ,qlevel ,qlanguage,bot='Apollo'):
        if self.check_apollo(quesId)==False:
            self.c.execute(
                "INSERT INTO apollo(sess_id ,quesId ,question ,answer ,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?,?)",
                (sess_id, quesId, question, answer, qlevel, qlanguage, bot))
            self.conn.commit()

    def set_apollo_messageId(self,messageId,queId):
        lock.acquire(True)
        self.c.execute("UPDATE apollo SET messageId=? WHERE quesId=?",(messageId,queId))
        lock.release()
        self.conn.commit()

    def get_apollo_answer_by_msgId(self,msgId):
        lock.acquire(True)
        self.c.execute("SELECT answer FROM apollo WHERE messageId=?",(msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_apollo_question_by_msgId(self,msgId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM apollo WHERE messageId=?",(msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_apollo_level_by_msgId(self,msgId):
        lock.acquire(True)
        self.c.execute("SELECT qlevel FROM apollo WHERE messageId=?",(msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False


    def get_apollo_bot(self,msgId):
        self.c.execute("SELECT bot FROM apollo WHERE messageId=?",(msgId,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False


    def delete_apollo(self,messageId):
        self.c.execute("DELETE FROM apollo WHERE messageId=?", (messageId,))
        self.conn.commit()

    """CHANCES"""
    def check_try(self,userId,messageId,bot):
        self.c.execute("SELECT tries FROM chances WHERE userId=? and messageId=? and bot=?", (userId,messageId,bot))
        tries = self.c.fetchone()
        if tries is not None:
            return tries[0]
        else:
            return False

    def create_chance(self,userId,messageId,bot,chance=1):
        self.c.execute(
            "INSERT INTO chances(userId,messageId,bot,tries) VALUES (?,?,?,?)", (userId,messageId, bot,chance))
        self.conn.commit()

    def delete_chance(self,messageId):
        self.c.execute("DELETE FROM chances WHERE messageId=?", (messageId,))
        self.conn.commit()



        """CORRECT ANSWERS"""

    def check_correct(self,messageId):
        self.c.execute("SELECT students FROM correct WHERE messageId=?", (messageId,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def create_correct(self,messageId):
        self.c.execute("INSERT INTO correct(messageId) VALUES (?)", (messageId,))
        self.conn.commit()

    def update_correct(self,messageId):
        correct =self.check_correct(messageId=messageId)
        correct +=1
        self.c.execute("UPDATE correct SET students=? WHERE messageId=?", (correct,messageId))
        self.conn.commit()

    def delete_correct(self,messageId):
        self.c.execute("DELETE FROM correct WHERE messageId=?", (messageId,))
        self.conn.commit()
