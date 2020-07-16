#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
from threading import Lock

lock = Lock()


class DBManager:

    def __init__(self, dbname="solo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False, timeout=20)
        self.c = self.conn.cursor()

    def setup(self):
        tbl_africa = """CREATE TABLE IF NOT EXISTS africa(id INTEGER PRIMARY KEY,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,answer1 VARCHAR DEFAULT NULL,answer2 VARCHAR DEFAULT NULL,answer3 VARCHAR DEFAULT NULL,answer4 VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,bot VARCHAR DEFAULT NULL)"""
        tbl_apollo = """CREATE TABLE IF NOT EXISTS apollo(id INTEGER PRIMARY KEY,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,bot VARCHAR DEFAULT NULL)"""
        tbl_users = """CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,userid INTEGER DEFAULT NULL,answer VARCHAR DEFAULT NULL,message_id INTEGER DEFAULT NULL,poll_id INTEGER DEFAULT NULL,session VARCHAR DEFAULT NULL,tries INTEGER DEFAULT NULL,correct INTEGER DEFAULT 0)"""
        tbl_gaia = """CREATE TABLE IF NOT EXISTS gaia(id INTEGER PRIMARY KEY,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,bot VARCHAR DEFAULT NULL)"""
        tbl_kadlu = """CREATE TABLE IF NOT EXISTS kadlu (id INTEGER PRIMARY KEY,quesId INTEGER DEFAULT NULL ,main_id INTEGER DEFAULT NULL ,main_question VARCHAR DEFAULT NULL,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,answer1 VARCHAR DEFAULT NULL,answer2 VARCHAR DEFAULT NULL,answer3 VARCHAR DEFAULT NULL,answer4 VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,bot VARCHAR DEFAULT NULL)"""
        self.c.execute(tbl_africa)
        self.c.execute(tbl_gaia)
        self.c.execute(tbl_apollo)
        self.c.execute(tbl_kadlu)
        self.c.execute(tbl_users)
        self.conn.commit()

    ###########Kadlu###################
    def check_kadlu(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM kadlu WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False


    def save_kadlu(self, quesId,main_id,main_question,question, answer, answer1, answer2, answer3, answer4,  qlevel, qlanguage,
                    bot='kadlu'):
        if self.check_kadlu(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO kadlu(quesId,main_id,main_question,question, answer, answer1, answer2, answer3, answer4,  qlevel, qlanguage,bot) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (quesId,main_id,main_question,question, answer, answer1, answer2, answer3, answer4,  qlevel, qlanguage,bot))
            lock.release()
            self.conn.commit()

    def get_kadlu_main(self):
        self.c.execute("SELECT main_id,main_question FROM kadlu ORDER BY RANDOM() LIMIT 1")
        que = self.c.fetchone()
        if que is not None:
            return que
        else:
            return False

    def get_kadlu_min_qstn_id(self,main_id):
        self.c.execute("SELECT min(id) FROM kadlu WHERE main_id=?",(main_id,))
        min_id = self.c.fetchone()
        if min_id is not None:
            return min_id[0]
        else:
            return False
    def get_kadlu_qstn_by_id(self,tid):
        self.c.execute("SELECT question, answer1, answer2, answer3, answer4 FROM kadlu WHERE id=?", (tid,))
        min_id = self.c.fetchone()
        if min_id is not None:
            return min_id
        else:
            return False
    def get_kadlu_count_main_id(self,main_id):
        self.c.execute("SELECT count(*) FROM kadlu WHERE main_id=?", (main_id,))
        min_id = self.c.fetchone()
        if min_id is not None:
            return min_id[0]
        else:
            return False

    def get_kadlu_next_id(self,tid):
        self.c.execute("SELECT id FROM kadlu WHERE id>? ORDER BY id LIMIT 1",(tid,))
        group = self.c.fetchone()
        if group is not None:
            return group[0]
        else:
            return False

    def get_kadlu_next_question(self,tid):
        self.c.execute("SELECT question, answer1, answer2, answer3, answer4 FROM kadlu WHERE id>? ORDER BY id LIMIT 1",(tid,))
        group = self.c.fetchone()
        if group is not None:
            return group
        else:
            return False

    ###########End Kadlu############################
    ###########GAIA############################
    def check_gaia(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM gaia WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False


    def save_gaia(self,quesId ,question,answer,qlevel ,qlanguage,bot='gaia'):
        if self.check_gaia(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO gaia(quesId ,question,answer,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?)",
                (quesId ,question,answer,qlevel ,qlanguage,bot))
            lock.release()
            self.conn.commit()

    def get_gaia_question(self):
        self.c.execute("SELECT question,answer FROM gaia ORDER BY RANDOM() LIMIT 1")
        que = self.c.fetchone()
        if que is not None:
            return que
        else:
            return False
    ############END GAIA######################
    ################APOLLO######################
    def check_apollo(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM apollo WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_apollo(self,quesId ,question,answer,qlevel ,qlanguage,bot='apollo'):
        if self.check_apollo(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO apollo(quesId ,question,answer,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?)",
                (quesId ,question,answer,qlevel ,qlanguage,bot))
            lock.release()
            self.conn.commit()

    def get_apollo_question(self):
        self.c.execute("SELECT question,answer FROM apollo ORDER BY RANDOM() LIMIT 1")
        que = self.c.fetchone()
        if que is not None:
            return que
        else:
            return False

    ################END APPOLLO######################
    ################AFRICA######################

    def check_africa(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM africa WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False
    def get_africa_message_id(self,pollid):
        self.c.execute("SELECT userid,message_id,session FROM users WHERE poll_id=?", (pollid,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot
        else:
            return False


    def save_africa(self, quesId, answer, answer1, answer2, answer3, answer4, question, qlevel, qlanguage,
                    bot='africa'):
        if self.check_africa(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO africa(quesId ,answer,answer1,answer2,answer3,answer4,question ,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (quesId, answer, answer1, answer2, answer3, answer4, question, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def get_africa_question(self):
        self.c.execute("SELECT question,answer, answer1, answer2, answer3, answer4 FROM africa ORDER BY RANDOM() LIMIT 1")
        que = self.c.fetchone()
        if que is not None:
            return que
        else:
            return False

################AFRICA######################

################USERS######################
    def check_user(self, userid):
        lock.acquire(True)
        self.c.execute("SELECT userid FROM users WHERE userid=?", (userid,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def create_user(self,userid):
        if self.check_user(userid) == False:
            self.c.execute("INSERT INTO users(userid) VALUES (?)",(userid,))
            self.conn.commit()

    def update_user_question(self,userid,answer,session,message_id=None,poll_id=None,tries=None,correct=None):
        self.create_user(userid)
        lock.acquire(True)
        self.c.execute("UPDATE users SET answer=?,session=?,message_id=?,poll_id=?,tries=?,correct=? WHERE userid=?",(answer,session,message_id,poll_id,tries,correct,userid))
        lock.release()
        self.conn.commit()



    def get_tries(self,userid):
        self.c.execute("SELECT session,tries FROM users WHERE userid=?", (userid,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot
        else:
            return False

    def get_answer(self,userid):
        self.c.execute("SELECT answer FROM users WHERE userid=?", (userid,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def update_tries(self,user_id,tries):
        self.c.execute("UPDATE users SET tries=? WHERE userid=?",(tries,user_id))
        self.conn.commit()

    def update_correct(self,user_id,correct):
        self.c.execute("UPDATE users SET correct=? WHERE userid=?",(correct,user_id))
        self.conn.commit()

    def get_correct(self, userid):
        self.c.execute("SELECT correct FROM users WHERE userid=?", (userid,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def get_answer_msgid(self,userid,msgid):
        lock.acquire(True)
        self.c.execute("SELECT answer FROM users WHERE userid=? AND message_id=?", (userid,msgid))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False


    def get_session_type(self,userid,msgid):
        lock.acquire(True)
        self.c.execute("SELECT session FROM users WHERE userid=? AND message_id=?", (userid,msgid))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def update_user_msg_id(self,user_id,msgid):
        self.c.execute("UPDATE users SET correct=? WHERE userid=?",(msgid,user_id))
        self.conn.commit()

    def get_user_nextqstn_id(self, userid):
        self.c.execute("SELECT correct FROM users WHERE userid=?", (userid,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False