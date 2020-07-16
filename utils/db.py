#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
from threading import Lock

lock = Lock()


class DBHelper:

    def __init__(self, dbname="main.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False, timeout=20)
        self.c = self.conn.cursor()

    def setup(self):
        tbl_sessions = """CREATE TABLE IF NOT EXISTS live_sessions(id INTEGER PRIMARY KEY,sess_id INTEGER DEFAULT NULL ,group_language VARCHAR DEFAULT NULL ,bot VARCHAR DEFAULT NULL ,lesson VARCHAR DEFAULT NULL,each_time INTEGER DEFAULT NULL ,total_time INTEGER DEFAULT NULL,
                      start_time TIMESTAMP DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,questions INTEGER DEFAULT NULL,session_name VARCHAR DEFAULT NULL,status INTEGER DEFAULT 0)"""
        tbl_groups = """CREATE TABLE IF NOT EXISTS bot_groups(id INTEGER PRIMARY KEY,groupId INTEGER DEFAULT NULL,groupTitle VARCHAR DEFAULT NULL,token VARCHAR DEFAULT NULL,groupLanguage VARCHAR DEFAULT NULL,botUsername VARCHAR DEFAULT NULL,link VARCHAR DEFAULT NULL )"""
        tbl_apollo = """CREATE TABLE IF NOT EXISTS apollo(id INTEGER PRIMARY KEY,sess_id INTEGER DEFAULT NULL,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,groupId INTEGER DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,messageId INTEGER DEFAULT 0,bot VARCHAR DEFAULT NULL,status INTEGER DEFAULT 0)"""
        tbl_chances = """CREATE TABLE IF NOT EXISTS chances(id INTEGER PRIMARY KEY,userId INTEGER DEFAULT NULL ,tries INTEGER DEFAULT 0,bot DEFAULT NULL,messageId INTEGER DEFAULT NULL )"""
        tbl_correct = """CREATE TABLE IF NOT EXISTS correct(id INTEGER PRIMARY KEY,messageId INTEGER DEFAULT NULL,students INTEGER DEFAULT 0)"""
        tbl_notify = """CREATE TABLE IF NOT EXISTS notify(id INTEGER PRIMARY KEY,userid INTEGER DEFAULT NULL,rank VARCHAR DEFAULT NULL)"""
        tbl_likes = """CREATE TABLE IF NOT EXISTS likes(id INTEGER PRIMARY KEY,userid INTEGER DEFAULT NULL,liker INTEGER DEFAULT NULL ,rank VARCHAR DEFAULT NULL )"""
        tbl_seshat = """CREATE TABLE IF NOT EXISTS seshat(id INTEGER PRIMARY KEY,sess_id INTEGER DEFAULT NULL,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,instruction VARCHAR DEFAULT NULL,gif VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,messageId INTEGER DEFAULT 0,bot VARCHAR DEFAULT NULL,status INTEGER DEFAULT 0)"""
        tbl_tyche = """CREATE TABLE IF NOT EXISTS tyche(id INTEGER PRIMARY KEY,sess_id INTEGER DEFAULT NULL,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,messageId INTEGER DEFAULT 0,bot VARCHAR DEFAULT NULL,status INTEGER DEFAULT 0)"""
        tbl_leizi = """CREATE TABLE IF NOT EXISTS leizi(id INTEGER PRIMARY KEY,sess_id INTEGER DEFAULT NULL,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,answer1 VARCHAR DEFAULT NULL,answer2 VARCHAR DEFAULT NULL,instruction VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,messageId INTEGER DEFAULT 0,bot VARCHAR DEFAULT NULL,status INTEGER DEFAULT 0)"""
        tbl_odin = """CREATE TABLE IF NOT EXISTS odin(id INTEGER PRIMARY KEY,sess_id INTEGER DEFAULT NULL,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,meaning VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,messageId INTEGER DEFAULT 0,bot VARCHAR DEFAULT NULL,status INTEGER DEFAULT 0)"""
        tbl_zamo = """CREATE TABLE IF NOT EXISTS zamo(id INTEGER PRIMARY KEY,sess_id INTEGER DEFAULT NULL,quesId INTEGER DEFAULT NULL ,answer VARCHAR DEFAULT NULL,question VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,messageId INTEGER DEFAULT 0,bot VARCHAR DEFAULT NULL,status INTEGER DEFAULT 0)"""
        tbl_africa = """CREATE TABLE IF NOT EXISTS africa(id INTEGER PRIMARY KEY,sess_id INTEGER DEFAULT NULL,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,answer1 VARCHAR DEFAULT NULL,answer2 VARCHAR DEFAULT NULL,answer3 VARCHAR DEFAULT NULL,answer4 VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,messageId INTEGER DEFAULT 0,bot VARCHAR DEFAULT NULL,status INTEGER DEFAULT 0,poll_id INTEGER DEFAULT 0,correct_id INTEGER DEFAULT 0)"""
        tbl_wala = """CREATE TABLE IF NOT EXISTS wala (id INTEGER PRIMARY KEY,sess_id INTEGER DEFAULT NULL,quesId INTEGER DEFAULT NULL ,main_question VARCHAR DEFAULT NULL,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,answer1 VARCHAR DEFAULT NULL,answer2 VARCHAR DEFAULT NULL,answer3 VARCHAR DEFAULT NULL,answer4 VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,messageId INTEGER DEFAULT 0,bot VARCHAR DEFAULT NULL,status INTEGER DEFAULT 0,poll_id INTEGER DEFAULT 0,correct_id INTEGER DEFAULT 0)"""
        tbl_kadlu = """CREATE TABLE IF NOT EXISTS kadlu (id INTEGER PRIMARY KEY,sess_id INTEGER DEFAULT NULL,quesId INTEGER DEFAULT NULL ,main_question VARCHAR DEFAULT NULL,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,answer1 VARCHAR DEFAULT NULL,answer2 VARCHAR DEFAULT NULL,answer3 VARCHAR DEFAULT NULL,answer4 VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,messageId INTEGER DEFAULT 0,bot VARCHAR DEFAULT NULL,status INTEGER DEFAULT 0,poll_id INTEGER DEFAULT 0,correct_id INTEGER DEFAULT 0)"""
        tbl_nuwa = """CREATE TABLE IF NOT EXISTS nuwa(id INTEGER PRIMARY KEY,sess_id INTEGER DEFAULT NULL,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,messageId INTEGER DEFAULT 0,bot VARCHAR DEFAULT NULL,status INTEGER DEFAULT 0)"""
        tbl_gaia = """CREATE TABLE IF NOT EXISTS gaia(id INTEGER PRIMARY KEY,sess_id INTEGER DEFAULT NULL,quesId INTEGER DEFAULT NULL ,answer VARCHAR DEFAULT NULL,question VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,messageId INTEGER DEFAULT 0,bot VARCHAR DEFAULT NULL,status INTEGER DEFAULT 0)"""
        self.c.execute(tbl_notify)
        self.c.execute(tbl_likes)
        self.c.execute(tbl_sessions)
        self.c.execute(tbl_groups)
        self.c.execute(tbl_apollo)
        self.c.execute(tbl_chances)
        self.c.execute(tbl_correct)
        self.c.execute(tbl_seshat)
        self.c.execute(tbl_tyche)
        self.c.execute(tbl_leizi)
        self.c.execute(tbl_odin)
        self.c.execute(tbl_zamo)
        self.c.execute(tbl_africa)
        self.c.execute(tbl_wala)
        self.c.execute(tbl_kadlu)
        self.c.execute(tbl_nuwa)
        self.c.execute(tbl_gaia)
        self.conn.commit()
        # """Sessions"""

    def check_session(self, sess_id):
        lock.acquire(True)
        self.c.execute("SELECT sess_id FROM live_sessions WHERE sess_id=?", (sess_id,))
        lock.release()
        sess = self.c.fetchone()
        if sess is not None:
            return True
        else:
            return False

    def save_sessions(self, sess_id, group_language, bot, lesson, each_time, total_time, start_time, qlevel, questions,
                      session_name, status):

        if self.check_session(sess_id=sess_id) != True:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO live_sessions(sess_id,group_language,bot,lesson,each_time,total_time,start_time,qlevel,questions,session_name,status) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (sess_id, group_language, bot, lesson, each_time, total_time, start_time, qlevel, questions,
                 session_name, status))
            lock.release()
            self.conn.commit()

    def get_sessions(self):
        lock.acquire(True)
        self.c.execute("SELECT sess_id,session_name,bot FROM live_sessions WHERE status=0")
        lock.release()
        sess = self.c.fetchall()
        if sess is not None:
            return sess
        else:
            return False

    def update_session(self, sessId):
        lock.acquire(True)
        status = 1
        self.c.execute("UPDATE live_sessions SET status=? WHERE sess_id=?", (status, sessId))
        lock.release()
        self.conn.commit()

    def get_session_status(self,sess_id):
        self.c.execute("SELECT status FROM live_sessions WHERE sess_id=?", (sess_id,))
        sess = self.c.fetchone()
        if sess is not None:
            return sess[0]
        else:
            return False

    '''Bot Group'''

    def check_bot(self, groupId):
        self.c.execute("SELECT groupId FROM bot_groups WHERE groupId=?", (groupId,))
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_bot(self, groupId, groupTitle, token, groupLanguage, botUsername, link):
        if self.check_bot(groupId) == False:
            self.c.execute(
                "INSERT INTO bot_groups(groupId,groupTitle,token,groupLanguage,botUsername,link) VALUES (?,?,?,?,?,?)",
                (groupId, groupTitle, token, groupLanguage, botUsername, link))
            self.conn.commit()

    def get_bot(self, language):
        self.c.execute("SELECT * FROM bot_groups WHERE groupLanguage=?", (language,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]

    """questions"""

    """Gaia"""

    def check_gaia(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM gaia WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_gaia(self, sess_id, quesId,answer, question, qlevel, qlanguage, bot='gaia'):
        if self.check_gaia(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO gaia(sess_id ,quesId,answer,question ,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?,?)",
                (sess_id, quesId, answer,question, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def set_gaia_messageId(self, messageId, queId):
        lock.acquire(True)
        self.c.execute("UPDATE gaia SET messageId=? WHERE quesId=?", (messageId, queId))
        lock.release()
        self.conn.commit()

    def get_gaia_answer_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT answer FROM gaia WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_gaia_question_by_queId(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM gaia WHERE quesId=?", (queId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_gaia_by_session_id(self, session_id):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM gaia WHERE sess_id=?", (session_id,))
        lock.release()
        answer = self.c.fetchall()
        if answer is not None:
            return answer
        else:
            return False

    def get_gaia_question_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM gaia WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_gaia_level_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT qlevel FROM gaia WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_gaia_bot(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT bot FROM gaia WHERE messageId=?", (msgId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def delete_gaia(self, messageId):
        lock.acquire(True)
        self.c.execute("DELETE FROM gaia WHERE messageId=?", (messageId,))
        lock.release()
        self.conn.commit()

    def delete_gaia_by_qid(self, questionId):
        # lock.acquire(True)
        self.c.execute("DELETE FROM gaia WHERE quesId=?", (questionId,))
        # lock.release()
        self.conn.commit()

    def get_gaia_count(self, sess_id):
        self.c.execute("SELECT COUNT(*) FROM gaia WHERE sess_id=?", (sess_id,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False


    """Nuwa"""
    def check_nuwa(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM nuwa WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_nuwa(self, sess_id, quesId, question, qlevel, qlanguage,bot='nuwa'):
        if self.check_nuwa(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO nuwa(sess_id ,quesId,question ,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?)",
                (sess_id, quesId, question, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def set_nuwa_messageId(self, messageId, queId):
        lock.acquire(True)
        self.c.execute("UPDATE nuwa SET messageId=? WHERE quesId=?", (messageId, queId))
        lock.release()
        self.conn.commit()

    def get_nuwa_answer_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM nuwa WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_nuwa_question_by_queId(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM nuwa WHERE quesId=?", (queId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_nuwa_by_session_id(self, session_id):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM nuwa WHERE sess_id=?", (session_id,))
        lock.release()
        answer = self.c.fetchall()
        if answer is not None:
            return answer
        else:
            return False

    def get_nuwa_question_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM nuwa WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_nuwa_level_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT qlevel FROM nuwa WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_nuwa_bot(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT bot FROM nuwa WHERE messageId=?", (msgId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def delete_nuwa(self, messageId):
        lock.acquire(True)
        self.c.execute("DELETE FROM nuwa WHERE messageId=?", (messageId,))
        lock.release()
        self.conn.commit()

    def delete_nuwa_by_qid(self, questionId):
        # lock.acquire(True)
        self.c.execute("DELETE FROM nuwa WHERE quesId=?", (questionId,))
        # lock.release()
        self.conn.commit()

    def get_nuwa_count(self, sess_id):
        self.c.execute("SELECT COUNT(*) FROM nuwa WHERE sess_id=?", (sess_id,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    """kadlu"""

    def check_kadlu(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM kadlu WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_kadlu(self, sess_id, quesId, main_question, question, answer, answer1, answer2, answer3, answer4, qlevel,
                   qlanguage,
                   bot='kadlu'):
        if self.check_kadlu(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO kadlu(sess_id ,quesId ,main_question,question ,answer,answer1,answer2,answer3,answer4,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                sess_id, quesId, main_question, question, answer, answer1, answer2, answer3, answer4, qlevel, qlanguage,
                bot))
            lock.release()
            self.conn.commit()

    def set_kadlu_messageId_pollId_correctId(self, messageId, pollId, correctId, queId):
        lock.acquire(True)
        self.c.execute("UPDATE kadlu SET messageId=?,poll_id=?,correct_id=? WHERE quesId=?",
                       (messageId, pollId, correctId, queId))
        lock.release()
        self.conn.commit()

    def get_kadlu_answer_by_pollId(self, pollId):
        lock.acquire(True)
        self.c.execute("SELECT correct_id FROM kadlu WHERE poll_id=?", (pollId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_kadlu_question_by_queId(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM kadlu WHERE quesId=?", (queId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_kadlu_by_session_id(self, session_id):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM kadlu WHERE sess_id=?", (session_id,))
        lock.release()
        answer = self.c.fetchall()
        if answer is not None:
            return answer
        else:
            return False

    def get_kadlu_question_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM kadlu WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_kadlu_level_by_pollId(self, pollId):
        lock.acquire(True)
        self.c.execute("SELECT qlevel FROM kadlu WHERE poll_id=?", (pollId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_kadlu_bot(self, pollId):
        lock.acquire(True)
        self.c.execute("SELECT bot FROM kadlu WHERE poll_id=?", (pollId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def delete_kadlu(self, messageId):
        lock.acquire(True)
        self.c.execute("DELETE FROM kadlu WHERE messageId=?", (messageId,))
        lock.release()
        self.conn.commit()

    def delete_kadlu_by_qid(self, questionId):
        # lock.acquire(True)
        self.c.execute("DELETE FROM kadlu WHERE quesId=?", (questionId,))
        # lock.release()
        self.conn.commit()

    def get_kadlu_count(self, sess_id):
        self.c.execute("SELECT COUNT(*) FROM kadlu WHERE sess_id=?", (sess_id,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False



    """Wala"""

    def check_wala(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM wala WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False
    def save_wala(self, sess_id ,quesId ,main_question,question ,answer,answer1,answer2,answer3,answer4,qlevel ,qlanguage,
                    bot='wala'):
        if self.check_wala(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO wala(sess_id ,quesId ,main_question,question ,answer,answer1,answer2,answer3,answer4,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (sess_id ,quesId ,main_question,question ,answer,answer1,answer2,answer3,answer4,qlevel ,qlanguage,bot))
            lock.release()
            self.conn.commit()

    def set_wala_messageId_pollId_correctId(self, messageId,pollId,correctId, queId):
        lock.acquire(True)
        self.c.execute("UPDATE wala SET messageId=?,poll_id=?,correct_id=? WHERE quesId=?", (messageId,pollId,correctId, queId))
        lock.release()
        self.conn.commit()

    def get_wala_answer_by_pollId(self, pollId):
        lock.acquire(True)
        self.c.execute("SELECT correct_id FROM wala WHERE poll_id=?", (pollId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_wala_question_by_queId(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM wala WHERE quesId=?", (queId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_wala_by_session_id(self, session_id):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM wala WHERE sess_id=?", (session_id,))
        lock.release()
        answer = self.c.fetchall()
        if answer is not None:
            return answer
        else:
            return False

    def get_wala_question_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM wala WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_wala_level_by_pollId(self, pollId):
        lock.acquire(True)
        self.c.execute("SELECT qlevel FROM wala WHERE poll_id=?", (pollId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_wala_bot(self, pollId):
        lock.acquire(True)
        self.c.execute("SELECT bot FROM wala WHERE poll_id=?", (pollId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False


    def delete_wala(self, messageId):
        lock.acquire(True)
        self.c.execute("DELETE FROM wala WHERE messageId=?", (messageId,))
        lock.release()
        self.conn.commit()

    def delete_wala_by_qid(self, questionId):
        # lock.acquire(True)
        self.c.execute("DELETE FROM wala WHERE quesId=?", (questionId,))
        # lock.release()
        self.conn.commit()

    def get_wala_count(self,sess_id):
        self.c.execute("SELECT COUNT(*) FROM wala WHERE sess_id=?", (sess_id,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    """Africa"""

    def check_africa(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM africa WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_africa(self, sess_id, quesId, answer, answer1, answer2, answer3, answer4, question, qlevel, qlanguage,
                    bot='africa'):
        if self.check_africa(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO africa(sess_id ,quesId ,answer,answer1,answer2,answer3,answer4,question ,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (sess_id, quesId, answer, answer1, answer2, answer3, answer4, question, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def set_africa_messageId_pollId_correctId(self, messageId,pollId,correctId, queId):
        lock.acquire(True)
        self.c.execute("UPDATE africa SET messageId=?,poll_id=?,correct_id=? WHERE quesId=?", (messageId,pollId,correctId, queId))
        lock.release()
        self.conn.commit()

    def get_africa_answer_by_pollId(self, pollId):
        lock.acquire(True)
        self.c.execute("SELECT correct_id FROM africa WHERE poll_id=?", (pollId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_africa_question_by_queId(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM africa WHERE quesId=?", (queId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_africa_by_session_id(self, session_id):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM africa WHERE sess_id=?", (session_id,))
        lock.release()
        answer = self.c.fetchall()
        if answer is not None:
            return answer
        else:
            return False

    def get_africa_question_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM africa WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_africa_level_by_pollId(self, pollId):
        lock.acquire(True)
        self.c.execute("SELECT qlevel FROM africa WHERE poll_id=?", (pollId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_africa_bot(self, pollId):
        lock.acquire(True)
        self.c.execute("SELECT bot FROM africa WHERE poll_id=?", (pollId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def delete_africa(self, messageId):
        lock.acquire(True)
        self.c.execute("DELETE FROM africa WHERE messageId=?", (messageId,))
        lock.release()
        self.conn.commit()

    def delete_africa_by_qid(self, questionId):
        # lock.acquire(True)
        self.c.execute("DELETE FROM africa WHERE quesId=?", (questionId,))
        # lock.release()
        self.conn.commit()

    def get_africa_count(self,sess_id):
        self.c.execute("SELECT COUNT(*) FROM africa WHERE sess_id=?", (sess_id,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    """Zamo"""

    def check_zamo(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM zamo WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_zamo(self, sess_id, quesId, answer, question, qlevel, qlanguage, bot='Zamo'):
        if self.check_zamo(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO zamo(sess_id ,quesId ,answer,question ,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?,?)",
                (sess_id, quesId, answer, question, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def set_zamo_messageId(self, messageId, queId):
        lock.acquire(True)
        self.c.execute("UPDATE zamo SET messageId=? WHERE quesId=?", (messageId, queId))
        lock.release()
        self.conn.commit()

    def get_zamo_answer_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT answer FROM zamo WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_zamo_question_by_queId(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM zamo WHERE quesId=?", (queId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_zamo_by_session_id(self, session_id):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM zamo WHERE sess_id=?", (session_id,))
        lock.release()
        answer = self.c.fetchall()
        if answer is not None:
            return answer
        else:
            return False

    def get_zamo_question_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM zamo WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_zamo_level_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT qlevel FROM zamo WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_zamo_bot(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT bot FROM zamo WHERE messageId=?", (msgId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def delete_zamo(self, messageId):
        lock.acquire(True)
        self.c.execute("DELETE FROM zamo WHERE messageId=?", (messageId,))
        lock.release()
        self.conn.commit()

    def delete_zamo_by_qid(self, questionId):
        # lock.acquire(True)
        self.c.execute("DELETE FROM zamo WHERE quesId=?", (questionId,))
        # lock.release()
        self.conn.commit()

    def get_zamo_count(self,sess_id):
        self.c.execute("SELECT COUNT(*) FROM zamo WHERE sess_id=?", (sess_id,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    """Odin"""

    def check_odin(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM odin WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_odin(self, sess_id, quesId, question, meaning,qlevel, qlanguage, bot='Odin'):
        if self.check_odin(quesId) == False:
            self.c.execute(
                "INSERT INTO odin(sess_id ,quesId ,question,meaning ,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?,?)",
                (sess_id, quesId, question,meaning, qlevel, qlanguage, bot))
            self.conn.commit()

    def set_odin_messageId(self, messageId, queId):
        lock.acquire(True)
        self.c.execute("UPDATE odin SET messageId=? WHERE quesId=?", (messageId, queId))
        lock.release()
        self.conn.commit()

    def get_odin_answer_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT question,meaning FROM odin WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer
        else:
            return False

    def get_odin_question_by_queId(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM odin WHERE quesId=?", (queId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_odin_by_session_id(self, session_id):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM odin WHERE sess_id=?", (session_id,))
        lock.release()
        answer = self.c.fetchall()
        if answer is not None:
            return answer
        else:
            return False

    def get_odin_question_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM odin WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_odin_level_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT qlevel FROM odin WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_odin_bot(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT bot FROM odin WHERE messageId=?", (msgId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def delete_odin(self, messageId):
        lock.acquire(True)
        self.c.execute("DELETE FROM odin WHERE messageId=?", (messageId,))
        lock.release()
        self.conn.commit()

    def delete_odin_by_qid(self, questionId):
        # lock.acquire(True)
        self.c.execute("DELETE FROM odin WHERE quesId=?", (questionId,))
        # lock.release()
        self.conn.commit()


    def get_odin_count(self,sess_id):
        self.c.execute("SELECT COUNT(*) FROM odin WHERE sess_id=?", (sess_id,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    """Leizi"""

    def check_leizi(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM leizi WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_leizi(self, sess_id, quesId, question, answer1, answer2, instruction, qlevel, qlanguage, bot='Leizi'):
        if self.check_leizi(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO leizi(sess_id ,quesId ,question ,answer1,answer2,instruction,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?,?,?,?)",
                (sess_id, quesId, question, answer1, answer2, instruction, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def set_leizi_messageId(self, messageId, queId):
        lock.acquire(True)
        self.c.execute("UPDATE leizi SET messageId=? WHERE quesId=?", (messageId, queId))
        lock.release()
        self.conn.commit()

    def get_leizi_answer_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT answer1,answer2 FROM leizi WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer
        else:
            return False

    def get_leizi_by_session_id(self, session_id):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM leizi WHERE sess_id=?", (session_id,))
        lock.release()
        answer = self.c.fetchall()
        if answer is not None:
            return answer
        else:
            return False

    def get_leizi_question_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM leizi WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_leizi_level_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT qlevel FROM leizi WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_leizi_bot(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT bot FROM leizi WHERE messageId=?", (msgId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def delete_leizi(self, messageId):
        lock.acquire(True)
        self.c.execute("DELETE FROM leizi WHERE messageId=?", (messageId,))
        lock.release()
        self.conn.commit()

    def delete_leizi_by_qid(self, questionId):
        # lock.acquire(True)
        self.c.execute("DELETE FROM leizi WHERE quesId=?", (questionId,))
        # lock.release()
        self.conn.commit()

    def get_leizi_count(self,sess_id):
        self.c.execute("SELECT COUNT(*) FROM leizi WHERE sess_id=?", (sess_id,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    """Tyche"""

    def check_tyche(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM tyche WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_tyche(self, sess_id, quesId, question, answer, qlevel, qlanguage, bot='Tyche'):
        if self.check_tyche(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO tyche(sess_id ,quesId ,question ,answer,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?,?)",
                (sess_id, quesId, question, answer, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def set_tyche_messageId(self, messageId, queId):
        lock.acquire(True)
        self.c.execute("UPDATE tyche SET messageId=? WHERE quesId=?", (messageId, queId))
        lock.release()
        self.conn.commit()

    def get_tyche_answer_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT answer FROM tyche WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_tyche_by_session_id(self, session_id):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM tyche WHERE sess_id=?", (session_id,))
        lock.release()
        answer = self.c.fetchall()
        if answer is not None:
            return answer
        else:
            return False

    def get_tyche_question_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM tyche WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_tyche_level_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT qlevel FROM tyche WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_tyche_bot(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT bot FROM tyche WHERE messageId=?", (msgId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def delete_tyche(self, messageId):
        lock.acquire(True)
        self.c.execute("DELETE FROM tyche WHERE messageId=?", (messageId,))
        lock.release()
        self.conn.commit()

    def delete_tyche_by_qid(self, questionId):
        # lock.acquire(True)
        self.c.execute("DELETE FROM tyche WHERE quesId=?", (questionId,))
        # lock.release()
        self.conn.commit()

    def get_tyche_count(self,sess_id):
        self.c.execute("SELECT COUNT(*) FROM tyche WHERE sess_id=?", (sess_id,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False


    """Seshat"""

    def check_seshat(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM seshat WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_seshat(self, sess_id, quesId, question, answer, instruction, gif, qlevel, qlanguage, bot='Seshat'):
        if self.check_seshat(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO seshat(sess_id ,quesId ,question ,answer,instruction ,gif,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?,?,?,?)",
                (sess_id, quesId, question, answer, instruction, gif, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def set_seshat_messageId(self, messageId, queId):
        lock.acquire(True)
        self.c.execute("UPDATE seshat SET messageId=? WHERE quesId=?", (messageId, queId))
        lock.release()
        self.conn.commit()

    def get_seshat_answer_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT answer FROM seshat WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_seshat_by_session_id(self, session_id):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM seshat WHERE sess_id=?", (session_id,))
        lock.release()
        answer = self.c.fetchall()
        if answer is not None:
            return answer
        else:
            return False

    def get_seshat_question_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM seshat WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_seshat_level_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT qlevel FROM seshat WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_seshat_bot(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT bot FROM seshat WHERE messageId=?", (msgId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def delete_seshat(self, messageId):
        lock.acquire(True)
        self.c.execute("DELETE FROM seshat WHERE messageId=?", (messageId,))
        lock.release()
        self.conn.commit()

    def delete_seshat_by_qid(self, questionId):
        # lock.acquire(True)
        self.c.execute("DELETE FROM seshat WHERE quesId=?", (questionId,))
        # lock.release()
        self.conn.commit()

    def get_seshat_count(self,sess_id):
        self.c.execute("SELECT COUNT(*) FROM seshat WHERE sess_id=?", (sess_id,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    """1. Apollo"""

    def check_apollo(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM apollo WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_apollo(self, sess_id, quesId, question, answer, qlevel, qlanguage, bot='Apollo'):
        if self.check_apollo(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO apollo(sess_id ,quesId ,question ,answer ,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?,?)",
                (sess_id, quesId, question, answer, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def set_apollo_messageId(self, messageId, queId):
        lock.acquire(True)
        self.c.execute("UPDATE apollo SET messageId=? WHERE quesId=?", (messageId, queId))
        lock.release()
        self.conn.commit()

    def get_apollo_answer_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT answer FROM apollo WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_apollo_by_session_id(self, session_id):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM apollo WHERE sess_id=?", (session_id,))
        lock.release()
        answer = self.c.fetchall()
        if answer is not None:
            return answer
        else:
            return False

    def get_apollo_question_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT question FROM apollo WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_apollo_level_by_msgId(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT qlevel FROM apollo WHERE messageId=?", (msgId,))
        lock.release()
        answer = self.c.fetchone()
        if answer is not None:
            return answer[0]
        else:
            return False

    def get_apollo_bot(self, msgId):
        lock.acquire(True)
        self.c.execute("SELECT bot FROM apollo WHERE messageId=?", (msgId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def delete_apollo(self, messageId):
        lock.acquire(True)
        self.c.execute("DELETE FROM apollo WHERE messageId=?", (messageId,))
        lock.release()
        self.conn.commit()

    def delete_apollo_by_qid(self, questionId):
        # lock.acquire(True)
        self.c.execute("DELETE FROM apollo WHERE quesId=?", (questionId,))
        # lock.release()
        self.conn.commit()

    def get_apollo_count(self,sess_id):
        self.c.execute("SELECT COUNT(*) FROM apollo WHERE sess_id=?", (sess_id,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    """CHANCES"""

    def check_try(self, userId, messageId, bot):
        lock.acquire(True)
        self.c.execute("SELECT tries FROM chances WHERE userId=? and messageId=? and bot=?", (userId, messageId, bot))
        lock.release()
        tries = self.c.fetchone()
        if tries is not None:
            return tries[0]
        else:
            return False

    def create_chance(self, userId, messageId, bot, chance=1):
        lock.acquire(True)
        self.c.execute("INSERT INTO chances(userId,messageId,bot,tries) VALUES (?,?,?,?)",
                       (userId, messageId, bot, chance))
        lock.release()
        self.conn.commit()

    def delete_chance(self, messageId):
        lock.acquire(True)
        self.c.execute("DELETE FROM chances WHERE messageId=?", (messageId,))
        lock.release()
        self.conn.commit()

    def count_chances(self, userId, messageId, bot):
        lock.acquire(True)
        self.c.execute("SELECT count(*) FROM chances WHERE userid=?  and messageId=? and bot=?",
                       (userId, messageId, bot))
        lock.release()
        bot = self.c.fetchone()
        return bot[0]

        """CORRECT ANSWERS"""

    def check_correct(self, messageId):
        lock.acquire(True)
        self.c.execute("SELECT students FROM correct WHERE messageId=?", (messageId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def create_correct(self, messageId):
        lock.acquire(True)
        self.c.execute("INSERT INTO correct(messageId) VALUES (?)", (messageId,))
        lock.release()
        self.conn.commit()

    def update_correct(self, messageId):
        correct = self.check_correct(messageId=messageId)
        correct += 1
        lock.acquire(True)
        self.c.execute("UPDATE correct SET students=? WHERE messageId=?", (correct, messageId))
        lock.release()
        self.conn.commit()

    def delete_correct(self, messageId):
        lock.acquire(True)
        self.c.execute("DELETE FROM correct WHERE messageId=?", (messageId,))
        lock.release()
        self.conn.commit()

    """Mark as already notified"""

    def check_notice(self, userid, rank):
        lock.acquire(True)
        self.c.execute("SELECT rank FROM notify WHERE userid=? and rank=?", (userid, rank))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def create_notice(self, userid, rank):
        if self.check_notice(userid, rank) == False:
            lock.acquire(True)
            self.c.execute("INSERT INTO notify(userid,rank) VALUES (?,?)", (userid, rank))
            lock.release()
            self.conn.commit()

    """Notification Likes"""

    def check_likes(self, userid, liker, rank):
        lock.acquire(True)
        self.c.execute("SELECT rank FROM likes WHERE userid=? and liker=? and rank=?", (userid, liker, rank))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def create_like(self, userid, liker, rank):
        if self.check_likes(userid, liker, rank) == False:
            lock.acquire(True)
            self.c.execute("INSERT INTO likes(userid,liker,rank) VALUES (?,?,?)", (userid, liker, rank))
            lock.release()
            self.conn.commit()

    def count_likes(self, userid, rank):
        lock.acquire(True)
        self.c.execute("SELECT count(*) FROM likes WHERE userid=?  and rank=?", (userid, rank))
        lock.release()
        bot = self.c.fetchone()
        return bot[0]
    
    
    def sanitize_bots(self):
        self.c.execute('DROP TABLE IF EXISTS africa')
        self.c.execute('DROP TABLE IF EXISTS apollo')
        self.c.execute('DROP TABLE IF EXISTS seshat')
        self.c.execute('DROP TABLE IF EXISTS leizi')
        self.c.execute('DROP TABLE IF EXISTS odin')
        self.c.execute('DROP TABLE IF EXISTS tyche')
        self.c.execute('DROP TABLE IF EXISTS zamo')
        self.c.execute('DROP TABLE IF EXISTS wala')
        self.c.execute('DROP TABLE IF EXISTS kadlu')
        self.c.execute('DROP TABLE IF EXISTS nuwa')
        self.c.execute('DROP TABLE IF EXISTS gaia')
        self.c.execute('DROP TABLE IF EXISTS live_sessions')
        self.conn.commit()





