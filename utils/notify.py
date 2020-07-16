import pytz
from telegram import Bot, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, Poll
import configs
import utils
import re
import datetime
import emoji
from os import remove
from time import sleep
import random
sql=utils.DBHelper()

sched = utils.SCHED

class Notify(object):
    def __init__(self, bot=Bot(token=configs.TOKEN)):
        self.bot = bot

    def remove_html_tags(self,text):
        """Remove html tags from a string"""
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        data = re.sub(clean, '', text)
        return data.replace(".", ".\n")

    def session_start(self,bot, questions, qlevel,session_name,total_time):
        try:
            stringg = utils.remove_html_tags(utils.BotMessages(id=4).get_message()).split('.')
            heading = stringg[0]
            body = "\n".join(stringg[1:6])
            message = f"<b>{heading}</b>\n{body}"
            print(message)
            timeinmins ="{:.2f}".format(int(total_time)/60)
            payload = self.bot.send_message(chat_id=configs.GROUPID,
                                            text=emoji.emojize(message.format(bot,questions,qlevel,session_name,timeinmins),use_aliases=True),parse_mode='html')
            self.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=payload.message_id)
        except:
            pass

    def session_ongoing(self,bot, questions, qlevel,session_name,total_time):
        try:
            stringg = utils.remove_html_tags(utils.BotMessages(id=25).get_message()).split('.')
            heading = stringg[0]
            body = "\n".join(stringg[1:6])
            message = f"<b>{heading}</b>\n{body}"
            print(message)
            timeinmins ="{:.2f}".format(int(total_time)/60)
            payload = self.bot.send_message(chat_id=configs.GROUPID,
                                            text=emoji.emojize(message.format(bot,questions,qlevel,session_name,timeinmins),use_aliases=True),parse_mode='html')
            self.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=payload.message_id)
        except:
            pass

    """Apollo"""
    def apollo_post(self,queId,question,sess_id):
        string=utils.remove_html_tags(utils.BotMessages(id=6).get_message())
        message=f"<b>{string}</b>\n\n:orange_book:<i>{question}</i>\n\nTime remaining: 50 seconds."

        payload = self.bot.send_message(chat_id=configs.GROUPID,
                                        text=emoji.emojize(message,use_aliases=True), parse_mode='html')
        messageId =payload.message_id
        print("posted mess",messageId)
        sql.set_apollo_messageId(messageId=messageId,queId=queId)
        sql.create_correct(messageId=messageId)

        #sleep for 49 seconds then post answer
        local_datetime = datetime.datetime.now()
        strppp = local_datetime.astimezone(pytz.UTC)
        new_time = strppp + datetime.timedelta(seconds=int(49))
        answer_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
        sched.add_job(utils.Notify().post_apollo_answer, 'date', run_date=answer_time, args=[messageId,sess_id],id=str(messageId))
        print("post answer",answer_time)
        utils.mr_logger(f"Posting the answer at :{answer_time}")

    """Apollo"""
    def post_apollo_answer(self,messageId,sess_id):

        try:
            utils.mr_logger(f"answer was posted")
            answer = sql.get_apollo_answer_by_msgId(msgId=messageId)
            total = sql.check_correct(messageId=messageId)
            # self.bot.delete_message()
            stringg = utils.remove_html_tags(utils.BotMessages(id=3).get_message()).split('.')
            head = stringg[0]
            body = "\n".join(stringg[1:3])
            message = f"<b>{head}</b>\n{body}"

            payload = self.bot.send_message(chat_id=configs.GROUPID,
                                            text=emoji.emojize(message, use_aliases=True).format(answer, total),
                                            parse_mode='html')
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=messageId)

            sql.delete_correct(messageId=messageId)
            sql.delete_chance(messageId=messageId)
            sleep(10)
            sql.delete_apollo(messageId)
            utils.mr_logger(f"message was deleted")
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=payload.message_id)
            check_count = sql.get_apollo_count(sess_id=sess_id)
            sess_state = sql.get_session_status(sess_id=sess_id)
            utils.mr_logger(f"{check_count} apollo questions remaining")
            if check_count==0 and sess_state==0:
                sql.update_session(sessId=sess_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =self.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                self.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
        except:
            pass

    """Seshat"""
    def seshat_post(self,queId,question,instruction,gif,sess_id):
        string=utils.remove_html_tags(utils.BotMessages(id=15).get_message())
        message=f"<b>{instruction}\n<i>{question}</i>\n\n{string}</b>"

        if "gif" in gif:
            utils.mr_logger(f"posting gif: {gif}")
            payload = self.bot.send_document(chat_id=configs.GROUPID, document=gif,
                                             caption=emoji.emojize(message, use_aliases=True),
                                             parse_mode=ParseMode.HTML)
        else:
            utils.mr_logger(f"posting photo: {gif}")
            payload = self.bot.send_photo(chat_id=configs.GROUPID, photo=gif,
                                          caption=emoji.emojize(message, use_aliases=True),
                                          parse_mode=ParseMode.HTML)

        messageId = payload.message_id
        print("posted mess", messageId)
        sql.set_seshat_messageId(messageId=messageId, queId=queId)
        sql.create_correct(messageId=messageId)

        # sleep for 49 seconds then post answer
        local_datetime = datetime.datetime.now()
        strppp = local_datetime.astimezone(pytz.UTC)
        new_time = strppp + datetime.timedelta(seconds=int(20))
        answer_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
        sched.add_job(utils.Notify().post_seshat_answer, 'date', run_date=answer_time, args=[messageId,sess_id],
                          id=str(messageId))
        print("post answer", answer_time)
        utils.mr_logger(f"Posting the answer at :{answer_time}")



    """Seshat"""
    def post_seshat_answer(self, messageId,sess_id):

        try:
            utils.mr_logger(f"answer was posted")
            answer = sql.get_seshat_answer_by_msgId(msgId=messageId)
            total = sql.check_correct(messageId=messageId)
            # self.bot.delete_message()
            stringg = utils.remove_html_tags(utils.BotMessages(id=3).get_message()).split('.')
            head = stringg[0]
            body = "\n".join(stringg[1:3])
            message = f"<b>{head}</b>\n{body}"

            payload = self.bot.send_message(chat_id=configs.GROUPID,
                                            text=emoji.emojize(message, use_aliases=True).format(answer, total),
                                            parse_mode='html')
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=messageId)
            sql.delete_correct(messageId=messageId)
            sql.delete_chance(messageId=messageId)
            sleep(4)
            sql.delete_seshat(messageId)
            utils.mr_logger(f"message was deleted")
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=payload.message_id)
            check_count = sql.get_seshat_count(sess_id=sess_id)
            sess_state = sql.get_session_status(sess_id=sess_id)
            utils.mr_logger(f"{check_count} seshat questions remaining")
            if check_count==0 and sess_state==0:
                sql.update_session(sessId=sess_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =self.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                self.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
        except:
            pass

    """Tyche"""
    def tyche_post(self, queId, question,sess_id):
        string = utils.remove_html_tags(utils.BotMessages(id=12).get_message())
        message = f"<b>{string}</b>\n\n<i>{question}</i>"

        payload = self.bot.send_message(chat_id=configs.GROUPID,
                                        text=emoji.emojize(message, use_aliases=True), parse_mode='html')
        messageId = payload.message_id
        print("posted mess", messageId)
        sql.set_tyche_messageId(messageId=messageId, queId=queId)
        sql.create_correct(messageId=messageId)

        # sleep for 49 seconds then post answer
        local_datetime = datetime.datetime.now()
        strppp = local_datetime.astimezone(pytz.UTC)
        new_time = strppp + datetime.timedelta(seconds=int(30))
        answer_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
        sched.add_job(utils.Notify().post_tyche_answer, 'date', run_date=answer_time, args=[messageId,sess_id],
                          id=str(messageId))
        print("post answer", answer_time)
        utils.mr_logger(f"Posting the answer at :{answer_time}")

    """Tyche"""

    def post_tyche_answer(self, messageId,sess_id):

        try:
            utils.mr_logger(f"answer was posted")
            answer = sql.get_tyche_answer_by_msgId(msgId=messageId)
            total = sql.check_correct(messageId=messageId)
            # self.bot.delete_message()
            stringg = utils.remove_html_tags(utils.BotMessages(id=3).get_message()).split('.')
            head = stringg[0]
            body = "\n".join(stringg[1:3])
            message = f"<b>{head}</b>\n{body}"

            payload = self.bot.send_message(chat_id=configs.GROUPID,
                                            text=emoji.emojize(message, use_aliases=True).format(answer, total),
                                            parse_mode='html')
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=messageId)

            sql.delete_correct(messageId=messageId)
            sql.delete_chance(messageId=messageId)
            sleep(5)
            sql.delete_tyche(messageId)
            utils.mr_logger(f"message was deleted")
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=payload.message_id)
            check_count=sql.get_tyche_count(sess_id=sess_id)
            sess_state = sql.get_session_status(sess_id=sess_id)
            utils.mr_logger(f"{check_count} tyche questions remaining")
            if check_count==0 and sess_state==0:
                sql.update_session(sessId=sess_id)
                msg =":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =self.bot.send_message(chat_id=configs.GROUPID,text=emoji.emojize(msg,use_aliases=True))
                self.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
        except:
            pass

    """Leizi"""

    def leizi_post(self, queId, question,instruction,sess_id):
        string = utils.remove_html_tags(utils.BotMessages(id=11).get_message())
        message = f"{string}\n<b>{instruction}</b>\n\n<i>{question}</i>"

        payload = self.bot.send_message(chat_id=configs.GROUPID,
                                        text=emoji.emojize(message, use_aliases=True), parse_mode='html')
        messageId = payload.message_id
        print("posted mess", messageId)
        sql.set_leizi_messageId(messageId=messageId, queId=queId)
        sql.create_correct(messageId=messageId)

        # sleep for 49 seconds then post answer
        local_datetime = datetime.datetime.now()
        strppp = local_datetime.astimezone(pytz.UTC)
        new_time = strppp + datetime.timedelta(seconds=int(30))
        answer_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
        sched.add_job(utils.Notify().post_leizi_answer, 'date', run_date=answer_time, args=[messageId,sess_id],
                          id=str(messageId))
        print("post answer", answer_time)
        utils.mr_logger(f"Posting the answer at :{answer_time}")

    """Leizi"""

    def post_leizi_answer(self, messageId,sess_id):

        try:
            utils.mr_logger(f"answer was posted")
            answer = sql.get_leizi_answer_by_msgId(msgId=messageId)
            answer1,answer2 =answer
            total = sql.check_correct(messageId=messageId)
            # self.bot.delete_message()
            stringg = utils.remove_html_tags(utils.BotMessages(id=3).get_message()).split('.')
            head = stringg[0]
            body = "\n".join(stringg[1:3])
            message = f"<b>{head}</b>\n{body}"

            if answer2=="":
                correct_answer =f"<b>{answer1}</b>"
            else:
                correct_answer = f"<b>{answer1} or {answer2}</b>"
            payload = self.bot.send_message(chat_id=configs.GROUPID,
                                            text=emoji.emojize(message, use_aliases=True).format(correct_answer, total),
                                            parse_mode='html')
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=messageId)

            sql.delete_correct(messageId=messageId)
            sql.delete_chance(messageId=messageId)
            sleep(5)
            sql.delete_leizi(messageId)
            utils.mr_logger(f"message was deleted")
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=payload.message_id)
            check_count = sql.get_leizi_count(sess_id=sess_id)
            sess_state = sql.get_session_status(sess_id=sess_id)
            utils.mr_logger(f"{check_count} leizi questions remaining")
            if check_count==0 and sess_state==0:
                sql.update_session(sessId=sess_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =self.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                self.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
        except:
            pass

    """Odin"""

    def odin_post(self, queId,sess_id):
        key_main = [[InlineKeyboardButton(emoji.emojize(":see_no_evil:", use_aliases=True),
                                          callback_data=f"odin+{queId}")]]
        main_markup = InlineKeyboardMarkup(key_main)
        string = utils.remove_html_tags(utils.BotMessages(id=9).get_message())
        message = f"<b>{string}</b>"

        payload = self.bot.send_message(chat_id=configs.GROUPID,
                                        text=emoji.emojize(message, use_aliases=True),reply_markup=main_markup, parse_mode='html')
        messageId = payload.message_id
        print("posted mess", messageId)
        sql.set_odin_messageId(messageId=messageId, queId=queId)
        sql.create_correct(messageId=messageId)

        # sleep for 49 seconds then post answer
        local_datetime = datetime.datetime.now()
        strppp = local_datetime.astimezone(pytz.UTC)
        new_time = strppp + datetime.timedelta(seconds=int(30))
        answer_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
        sched.add_job(utils.Notify().post_odin_answer, 'date', run_date=answer_time, args=[messageId,sess_id],
                          id=str(messageId))
        print("post answer", answer_time)
        utils.mr_logger(f"Posting the answer at :{answer_time}")

    """Odin"""

    def post_odin_answer(self, messageId,sess_id):

        try:
            utils.mr_logger(f"answer was posted")
            query = sql.get_odin_answer_by_msgId(msgId=messageId)
            answer, meaning =query

            total = sql.check_correct(messageId=messageId)
            # self.bot.delete_message()
            stringg = utils.remove_html_tags(utils.BotMessages(id=26).get_message()).split('.')
            head = stringg[0]
            body = "\n".join(stringg[1:4])
            message = f"<b>{head}</b>\n{body}"
            correct_answer=f"<b>{answer}</b>"
            total =f"<b>{total}</b>"
            meaning =f"<b>{meaning}</b>"
            payload = self.bot.edit_message_text(chat_id=configs.GROUPID,message_id=messageId,
                                            text=emoji.emojize(message, use_aliases=True).format(correct_answer, meaning,total),
                                            parse_mode='html')
            sleep(5)
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=messageId)

            sql.delete_correct(messageId=messageId)
            sql.delete_chance(messageId=messageId)

            sql.delete_odin(messageId)
            utils.mr_logger(f"message was deleted")
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=payload.message_id)
            check_count = sql.get_odin_count(sess_id=sess_id)
            sess_state = sql.get_session_status(sess_id=sess_id)
            utils.mr_logger(f"{check_count} odin questions remaining")
            if check_count==0 and sess_state==0:
                sql.update_session(sessId=sess_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =self.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                self.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
        except:
            pass

    """Zamo"""

    def zamo_post(self, queId, question,sess_id):
        string = utils.remove_html_tags(utils.BotMessages(id=8).get_message())
        message = f"<b>{string}</b>"
        voice = utils.zamol_download(url=question)
        payload = self.bot.send_audio(chat_id=configs.GROUPID,audio=open(voice, 'rb'),caption=emoji.emojize(message, use_aliases=True), parse_mode='html')
        remove(voice)
        messageId = payload.message_id
        print("posted mess", messageId)
        sql.set_zamo_messageId(messageId=messageId, queId=queId)
        sql.create_correct(messageId=messageId)

        # sleep for 49 seconds then post answer
        local_datetime = datetime.datetime.now()
        strppp = local_datetime.astimezone(pytz.UTC)
        new_time = strppp + datetime.timedelta(seconds=int(30))
        answer_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
        sched.add_job(utils.Notify().post_zamo_answer, 'date', run_date=answer_time, args=[messageId,sess_id],
                          id=str(messageId))
        print("post answer", answer_time)
        utils.mr_logger(f"Posting the answer at :{answer_time}")

    """Zamo"""

    def post_zamo_answer(self, messageId,sess_id):

        try:
            utils.mr_logger(f"answer was posted")
            answer = sql.get_zamo_answer_by_msgId(msgId=messageId)
            total = sql.check_correct(messageId=messageId)
            # self.bot.delete_message()
            stringg = utils.remove_html_tags(utils.BotMessages(id=3).get_message()).split('.')
            head = stringg[0]
            body = "\n".join(stringg[1:3])
            message = f"<b>{head}</b>\n{body}"

            payload = self.bot.send_message(chat_id=configs.GROUPID,
                                            text=emoji.emojize(message, use_aliases=True).format(answer, total),
                                            parse_mode='html')
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=messageId)

            sql.delete_correct(messageId=messageId)
            sql.delete_chance(messageId=messageId)
            sleep(5)
            sql.delete_zamo(messageId)
            utils.mr_logger(f"message was deleted")
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=payload.message_id)
            check_count = sql.get_zamo_count(sess_id=sess_id)
            sess_state = sql.get_session_status(sess_id=sess_id)
            utils.mr_logger(f"{check_count} zamo questions remaining")
            if check_count==0 and sess_state==0:
                sql.update_session(sessId=sess_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =self.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                self.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
        except:
            pass



    """Africa"""

    def africa_post(self, queId, question,pick,sess_id):
        # string = utils.remove_html_tags(utils.BotMessages(id=2).get_message())
        # message = f"<b>{string}</b>\n\n<i>{question}</i>"
        answer = pick[0]

        random.shuffle(pick)
        correct = pick.index(answer)
        payload =self.bot.send_poll(chat_id=configs.GROUPID,question=question,options=pick,is_anonymous=False,type=Poll.QUIZ,correct_option_id=correct)

        message_id = payload.message_id
        poll_id = payload.poll.id
        correct_id = payload.poll.correct_option_id
        print("posted mess", message_id)
        sql.set_africa_messageId_pollId_correctId(messageId=message_id,pollId=poll_id,correctId=correct_id, queId=queId)
        # sql.create_correct(messageId=poll_id)

        # sleep for 49 seconds then post answer
        local_datetime = datetime.datetime.now()
        strppp = local_datetime.astimezone(pytz.UTC)
        new_time = strppp + datetime.timedelta(seconds=int(15))
        answer_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
        sched.add_job(utils.Notify().post_africa_answer, 'date', run_date=answer_time, args=[message_id,sess_id],
                          id=str(poll_id))
        print("post answer", answer_time)
        utils.mr_logger(f"Stopping the quiz at :{answer_time}")

    """Africa"""

    def post_africa_answer(self, messageId,sess_id):

        try:
            utils.mr_logger(f"Quiz stopped")
            self.bot.stop_poll(chat_id=configs.GROUPID,message_id=messageId)
            sleep(6)
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=messageId)

            sql.delete_africa(messageId)
            utils.mr_logger(f"message was deleted")
            # self.bot.delete_message(chat_id=configs.GROUPID, message_id=payload.message_id)
            check_count = sql.get_africa_count(sess_id=sess_id)
            sess_state = sql.get_session_status(sess_id=sess_id)
            utils.mr_logger(f"{check_count} africa questions remaining")
            if check_count==0 and sess_state==0:
                sql.update_session(sessId=sess_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =self.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                self.bot.pin_chat_message(chat_id=configs.GROUPID,message_id=sent.message_id)
        except:
            pass

    """Wala"""

    def wala_post_main(self,question):
        string = utils.remove_html_tags(utils.BotMessages(id=14).get_message()).split('.')
        fmt = ".\n".join(string)
        message = f"<b>{fmt}</b>\n\n{question}"
        payload = self.bot.send_message(chat_id=configs.GROUPID,
                                        text=emoji.emojize(message, use_aliases=True),
                                        parse_mode='html')
        messageId = payload.message_id
        local_datetime = datetime.datetime.now()
        strppp = local_datetime.astimezone(pytz.UTC)
        new_time = strppp + datetime.timedelta(minutes=int(3))
        delete_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
        sched.add_job(utils.Notify().wala_delete_main, 'date', run_date=delete_time, args=[messageId],
                          id=str(messageId))
        print("delete answer", delete_time)
        utils.mr_logger(f"deleting the main question at :{delete_time}")

    """Wala"""
    def wala_delete_main(self, messageId):
        self.bot.delete_message(chat_id=configs.GROUPID,message_id=messageId)

    """Wala"""
    def wala_post(self, queId, question,pick,sess_id):
        # string = utils.remove_html_tags(utils.BotMessages(id=2).get_message())
        # message = f"<b>{string}</b>\n\n<i>{question}</i>"
        answer = pick[0]

        random.shuffle(pick)
        correct = pick.index(answer)
        payload =self.bot.send_poll(chat_id=configs.GROUPID,question=question,options=pick,is_anonymous=False,type=Poll.QUIZ,correct_option_id=correct)

        message_id = payload.message_id
        poll_id = payload.poll.id
        correct_id = payload.poll.correct_option_id
        print("posted mess", message_id)
        sql.set_wala_messageId_pollId_correctId(messageId=message_id,pollId=poll_id,correctId=correct_id, queId=queId)
        # sql.create_correct(messageId=poll_id)

        # sleep for 49 seconds then post answer
        local_datetime = datetime.datetime.now()
        strppp = local_datetime.astimezone(pytz.UTC)
        new_time = strppp + datetime.timedelta(seconds=int(18))
        answer_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
        sched.add_job(utils.Notify().post_wala_answer, 'date', run_date=answer_time, args=[message_id,sess_id],
                          id=str(poll_id))
        print("post answer", answer_time)
        utils.mr_logger(f"Stopping the quiz at :{answer_time}")

    def post_wala_answer(self, messageId, sess_id):

        try:
            utils.mr_logger(f"Quiz stopped")
            self.bot.stop_poll(chat_id=configs.GROUPID, message_id=messageId)
            sleep(6)
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=messageId)

            sql.delete_wala(messageId)
            utils.mr_logger(f"message was deleted")
            # self.bot.delete_message(chat_id=configs.GROUPID, message_id=payload.message_id)
            check_count = sql.get_wala_count(sess_id=sess_id)
            sess_state = sql.get_session_status(sess_id=sess_id)
            utils.mr_logger(f"{check_count} wala questions remaining")
            if check_count == 0 and sess_state == 0:
                sql.update_session(sessId=sess_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent = self.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                self.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
        except:
            pass


##########################################
    """Kadlu"""

    def kadlu_post_main(self,question):
        string = utils.remove_html_tags(utils.BotMessages(id=13).get_message()).split('.')
        fmt = ".\n".join(string)
        message = f"<b>{fmt}</b>"
        voice = utils.zamol_download(url=question)
        payload = self.bot.send_audio(chat_id=configs.GROUPID,audio=open(voice, 'rb'),
                                        caption=emoji.emojize(message, use_aliases=True),
                                        parse_mode='html')
        messageId = payload.message_id
        local_datetime = datetime.datetime.now()
        strppp = local_datetime.astimezone(pytz.UTC)
        new_time = strppp + datetime.timedelta(minutes=int(3))
        delete_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
        sched.add_job(utils.Notify().wala_delete_main, 'date', run_date=delete_time, args=[messageId],
                          id=str(messageId))
        print("delete answer", delete_time)
        utils.mr_logger(f"deleting the main question at :{delete_time}")

    """Kadlu"""
    def kadlu_delete_main(self, messageId):
        self.bot.delete_message(chat_id=configs.GROUPID,message_id=messageId)

    """Kadlu"""
    def kadlu_post(self, queId, question,pick,sess_id):
        # string = utils.remove_html_tags(utils.BotMessages(id=2).get_message())
        # message = f"<b>{string}</b>\n\n<i>{question}</i>"
        answer = pick[0]

        random.shuffle(pick)
        correct = pick.index(answer)
        payload =self.bot.send_poll(chat_id=configs.GROUPID,question=question,options=pick,is_anonymous=False,type=Poll.QUIZ,correct_option_id=correct)

        message_id = payload.message_id
        poll_id = payload.poll.id
        correct_id = payload.poll.correct_option_id
        print("posted mess", message_id)
        sql.set_kadlu_messageId_pollId_correctId(messageId=message_id,pollId=poll_id,correctId=correct_id, queId=queId)
        # sql.create_correct(messageId=poll_id)

        # sleep for 49 seconds then post answer
        local_datetime = datetime.datetime.now()
        strppp = local_datetime.astimezone(pytz.UTC)
        new_time = strppp + datetime.timedelta(seconds=int(18))
        answer_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
        sched.add_job(utils.Notify().post_kadlu_answer, 'date', run_date=answer_time, args=[message_id,sess_id],
                          id=str(poll_id))
        print("post answer", answer_time)
        utils.mr_logger(f"Stopping the quiz at :{answer_time}")

    def post_kadlu_answer(self, messageId, sess_id):

        try:
            utils.mr_logger(f"Quiz stopped")
            self.bot.stop_poll(chat_id=configs.GROUPID, message_id=messageId)
            sleep(6)
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=messageId)

            sql.delete_kadlu(messageId)
            utils.mr_logger(f"message was deleted")
            # self.bot.delete_message(chat_id=configs.GROUPID, message_id=payload.message_id)
            check_count = sql.get_kadlu_count(sess_id=sess_id)
            sess_state = sql.get_session_status(sess_id=sess_id)
            utils.mr_logger(f"{check_count} kadlu questions remaining")
            if check_count == 0 and sess_state == 0:
                sql.update_session(sessId=sess_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent = self.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                self.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
        except:
            pass
#######################NUWA#############################################################


    def nuwa_post(self,question,sess_id,queId):
        string = utils.remove_html_tags(utils.BotMessages(id=10).get_message())
        message = f"<b>{string}</b>\n\n<i>{question}</i>"

        payload = self.bot.send_message(chat_id=configs.GROUPID,
                                        text=emoji.emojize(message, use_aliases=True), parse_mode='html')
        messageId = payload.message_id
        print("posted mess", messageId)
        sql.set_nuwa_messageId(messageId=messageId, queId=queId)
        sql.create_correct(messageId=messageId)

        # sleep for 49 seconds then post answer
        local_datetime = datetime.datetime.now()
        strppp = local_datetime.astimezone(pytz.UTC)
        new_time = strppp + datetime.timedelta(seconds=int(35))
        answer_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
        sched.add_job(utils.Notify().post_nuwa_answer, 'date', run_date=answer_time, args=[messageId,sess_id],
                          id=str(messageId))
        print("post answer", answer_time)
        utils.mr_logger(f"Posting the answer at :{answer_time}")

    def post_nuwa_answer(self, messageId, sess_id):

        try:
            utils.mr_logger(f"answer was posted")

            total = sql.check_correct(messageId=messageId)
            # self.bot.delete_message()
            stringg = utils.remove_html_tags(utils.BotMessages(id=3).get_message()).split('.')
            head = stringg[1]

            message = f"<b>{head}</b>"

            payload = self.bot.send_message(chat_id=configs.GROUPID,
                                            text=emoji.emojize(message, use_aliases=True).format(total),
                                            parse_mode='html')
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=messageId)

            sql.delete_correct(messageId=messageId)
            sql.delete_chance(messageId=messageId)
            sleep(5)
            sql.delete_nuwa(messageId)
            utils.mr_logger(f"message was deleted")
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=payload.message_id)
            check_count = sql.get_nuwa_count(sess_id=sess_id)
            sess_state = sql.get_session_status(sess_id=sess_id)
            utils.mr_logger(f"{check_count} nuwa questions remaining")
            if check_count == 0 and sess_state == 0:
                sql.update_session(sessId=sess_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent = self.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                self.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
        except:
            pass

###################GAIA###################################
    def gaia_post(self, queId, question,sess_id):
        string = utils.remove_html_tags(utils.BotMessages(id=7).get_message())
        message = f"<b>{string}</b>"
        voice = utils.zamol_download(url=question)
        payload = self.bot.send_audio(chat_id=configs.GROUPID,audio=open(voice, 'rb'),caption=emoji.emojize(message, use_aliases=True), parse_mode='html')
        remove(voice)
        messageId = payload.message_id
        print("MESSAGE ID##########", messageId)
        sql.set_gaia_messageId(messageId=messageId, queId=queId)
        sql.create_correct(messageId=messageId)

        # sleep for 49 seconds then post answer
        local_datetime = datetime.datetime.now()
        strppp = local_datetime.astimezone(pytz.UTC)
        new_time = strppp + datetime.timedelta(seconds=int(43))
        answer_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
        sched.add_job(utils.Notify().post_gaia_answer, 'date', run_date=answer_time, args=[messageId,sess_id],
                          id=str(messageId))
        print("post answer", answer_time)
        utils.mr_logger(f"Posting the answer at :{answer_time}")

    """Gaia"""

    def post_gaia_answer(self, messageId,sess_id):

        try:
            utils.mr_logger(f"answer was posted")
            answer = sql.get_gaia_answer_by_msgId(msgId=messageId)
            total = sql.check_correct(messageId=messageId)
            # self.bot.delete_message()
            stringg = utils.remove_html_tags(utils.BotMessages(id=3).get_message()).split('.')
            head = stringg[0]
            body = "\n".join(stringg[1:3])
            message = f"<b>{head}</b>\n{body}"

            payload = self.bot.send_message(chat_id=configs.GROUPID,
                                            text=emoji.emojize(message, use_aliases=True).format(answer, total),
                                            parse_mode='html')
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=messageId)

            sql.delete_correct(messageId=messageId)
            sql.delete_chance(messageId=messageId)
            sleep(5)
            sql.delete_gaia(messageId)
            utils.mr_logger(f"message was deleted")
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=payload.message_id)
            check_count = sql.get_gaia_count(sess_id=sess_id)
            sess_state = sql.get_session_status(sess_id=sess_id)
            utils.mr_logger(f"{check_count} gaia questions remaining")
            if check_count==0 and sess_state==0:
                sql.update_session(sessId=sess_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =self.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                self.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
        except:
            pass


def session_ender(session_id):
    apollos = sql.get_apollo_by_session_id(session_id=session_id)
    seshats = sql.get_seshat_by_session_id(session_id=session_id)
    tyches = sql.get_tyche_by_session_id(session_id=session_id)
    leizis = sql.get_leizi_by_session_id(session_id=session_id)
    odins = sql.get_odin_by_session_id(session_id=session_id)
    zamos = sql.get_zamo_by_session_id(session_id=session_id)
    africas = sql.get_africa_by_session_id(session_id=session_id)
    walas = sql.get_wala_by_session_id(session_id=session_id)
    kadlus = sql.get_kadlu_by_session_id(session_id=session_id)
    nuwas = sql.get_nuwa_by_session_id(session_id=session_id)
    gaias = sql.get_gaia_by_session_id(session_id=session_id)

    if len(apollos) > 0:
        sql.update_session(sessId=session_id)
        for question in apollos:
            sql.delete_apollo_by_qid(question[0])
            try:
                sched.remove_job(job_id=str(question[0]))
            except:
                pass


    elif len(seshats) > 0:
        sql.update_session(sessId=session_id)
        for question in seshats:
            sql.delete_seshat_by_qid(question[0])
            try:
                sched.remove_job(job_id=str(question[0]))
            except:
                pass

    elif len(leizis) > 0:
        sql.update_session(sessId=session_id)
        for question in leizis:
            print(question)
            sql.delete_leizi_by_qid(question[0])

            try:
                sched.remove_job(job_id=str(question[0]))
            except:
                pass


    elif len(tyches) > 0:
        sql.update_session(sessId=session_id)
        for question in tyches:
            sql.delete_tyche_by_qid(question[0])
            try:

                sched.remove_job(job_id=str(question[0]))
            except:
                pass


    elif len(odins) > 0:
        sql.update_session(sessId=session_id)
        for question in odins:
            sql.delete_odin_by_qid(question[0])
            try:

                sched.remove_job(job_id=str(question[0]))
            except:
                pass


    elif len(zamos) > 0:
        sql.update_session(sessId=session_id)
        for question in zamos:
            sql.delete_zamo_by_qid(question[0])

            try:

                sched.remove_job(job_id=str(question[0]))
            except:
                pass

    elif len(africas) > 0:
        sql.update_session(sessId=session_id)
        for question in africas:
            sql.delete_africa_by_qid(question[0])
            try:
                sched.remove_job(job_id=str(question[0]))
            except:
                pass

    elif len(walas) > 0:
        sql.update_session(sessId=session_id)
        for question in walas:
            sql.delete_wala_by_qid(question[0])

            try:

                sched.remove_job(job_id=str(question[0]))
            except:
                pass

    elif len(kadlus) > 0:
        sql.update_session(sessId=session_id)
        for question in kadlus:
            sql.delete_kadlu_by_qid(question[0])

            try:

                sched.remove_job(job_id=str(question[0]))
            except:
                pass

    elif len(nuwas) > 0:
        sql.update_session(sessId=session_id)
        for question in nuwas:
            sql.delete_nuwa_by_qid(question[0])

            try:

                sched.remove_job(job_id=str(question[0]))
            except:
                pass

    elif len(gaias) > 0:
        sql.update_session(sessId=session_id)
        for question in gaias:
            sql.delete_gaia_by_qid(question[0])

            try:
                sched.remove_job(job_id=str(question[0]))
            except:
                pass

