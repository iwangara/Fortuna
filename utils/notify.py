import pytz
from telegram import Bot, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
import configs
import utils
import re
import datetime
import emoji
from os import remove
from time import sleep
import random
sql=utils.DBHelper()

scheduler = utils.SCHED
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
    def apollo_post(self,queId,question):
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
        scheduler.add_job(utils.Notify().post_apollo_answer, 'date', run_date=answer_time, args=[messageId],id=str(messageId))
        print("post answer",answer_time)
        utils.mr_logger(f"Posting the answer at :{answer_time}")

    """Apollo"""
    def post_apollo_answer(self,messageId):

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
        except:
            pass

    """Seshat"""
    def seshat_post(self,queId,question,instruction,gif):
        string=utils.remove_html_tags(utils.BotMessages(id=15).get_message())
        message=f"<b>{instruction}\n<i>{question}</i>\n\n{string}</b>"
        try:

            payload =self.bot.send_photo(chat_id=configs.GROUPID, photo=gif,
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
            scheduler.add_job(utils.Notify().post_seshat_answer, 'date', run_date=answer_time, args=[messageId],
                              id=str(messageId))
            print("post answer", answer_time)
            utils.mr_logger(f"Posting the answer at :{answer_time}")
        except:

            paylod =self.bot.send_document(chat_id=configs.GROUPID, document=gif,
                                             caption=emoji.emojize(message, use_aliases=True),
                                             parse_mode=ParseMode.HTML)
            message_Id = paylod.message_id
            print("posted mess", message_Id)
            sql.set_seshat_messageId(messageId=message_Id, queId=queId)
            sql.create_correct(messageId=message_Id)

            # sleep for 49 seconds then post answer
            local_datetime = datetime.datetime.now()
            strppp = local_datetime.astimezone(pytz.UTC)
            new_time = strppp + datetime.timedelta(seconds=int(20))
            answer_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
            scheduler.add_job(utils.Notify().post_seshat_answer, 'date', run_date=answer_time, args=[message_Id],
                              id=str(message_Id))
            print("post answer", answer_time)
            utils.mr_logger(f"Posting the answer at :{answer_time}")



    """Seshat"""
    def post_seshat_answer(self, messageId):

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
        except:
            pass

    """Tyche"""
    def tyche_post(self, queId, question):
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
        scheduler.add_job(utils.Notify().post_tyche_answer, 'date', run_date=answer_time, args=[messageId],
                          id=str(messageId))
        print("post answer", answer_time)
        utils.mr_logger(f"Posting the answer at :{answer_time}")

    """Tyche"""

    def post_tyche_answer(self, messageId):

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
        except:
            pass

    """Leizi"""

    def leizi_post(self, queId, question,instruction):
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
        scheduler.add_job(utils.Notify().post_leizi_answer, 'date', run_date=answer_time, args=[messageId],
                          id=str(messageId))
        print("post answer", answer_time)
        utils.mr_logger(f"Posting the answer at :{answer_time}")

    """Leizi"""

    def post_leizi_answer(self, messageId):

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
        except:
            pass

    """Odin"""

    def odin_post(self, queId):
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
        scheduler.add_job(utils.Notify().post_odin_answer, 'date', run_date=answer_time, args=[messageId],
                          id=str(messageId))
        print("post answer", answer_time)
        utils.mr_logger(f"Posting the answer at :{answer_time}")

    """Odin"""

    def post_odin_answer(self, messageId):

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
        except:
            pass

    """Zamo"""

    def zamo_post(self, queId, question):
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
        scheduler.add_job(utils.Notify().post_zamo_answer, 'date', run_date=answer_time, args=[messageId],
                          id=str(messageId))
        print("post answer", answer_time)
        utils.mr_logger(f"Posting the answer at :{answer_time}")

    """Zamo"""

    def post_zamo_answer(self, messageId):

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
        except:
            pass



    """Africa"""

    def africa_post(self, queId, question,pick):
        string = utils.remove_html_tags(utils.BotMessages(id=2).get_message())
        message = f"<b>{string}</b>\n\n<i>{question}</i>"
        button_list = [
            InlineKeyboardButton(pick[0], callback_data=f"africa+{pick[0]}"),
            InlineKeyboardButton(pick[1], callback_data=f"africa+{pick[1]}"),
            InlineKeyboardButton(pick[2], callback_data=f"africa+{pick[2]}"),
            InlineKeyboardButton(pick[3], callback_data=f"africa+{pick[3]}")
        ]
        random.shuffle(button_list)
        reply_markup = InlineKeyboardMarkup(utils.build_menu(button_list, n_cols=1))
        payload = self.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(message, use_aliases=True), parse_mode='html',reply_markup=reply_markup)

        messageId = payload.message_id
        print("posted mess", messageId)
        sql.set_africa_messageId(messageId=messageId, queId=queId)
        sql.create_correct(messageId=messageId)

        # sleep for 49 seconds then post answer
        local_datetime = datetime.datetime.now()
        strppp = local_datetime.astimezone(pytz.UTC)
        new_time = strppp + datetime.timedelta(seconds=int(10))
        answer_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
        scheduler.add_job(utils.Notify().post_africa_answer, 'date', run_date=answer_time, args=[messageId],
                          id=str(messageId))
        print("post answer", answer_time)
        utils.mr_logger(f"Posting the answer at :{answer_time}")

    """Africa"""

    def post_africa_answer(self, messageId):

        try:
            utils.mr_logger(f"answer was posted")
            answer = sql.get_africa_answer_by_msgId(msgId=messageId)
            total = sql.check_correct(messageId=messageId)
            # self.bot.delete_message()
            stringg = utils.remove_html_tags(utils.BotMessages(id=3).get_message()).split('.')
            head = stringg[0]
            body = "\n".join(stringg[1:3])
            message = f"<b>{head}</b>\n{body}"

            payload = self.bot.edit_message_text(chat_id=configs.GROUPID,message_id=messageId,
                                            text=emoji.emojize(message, use_aliases=True).format(answer, total),
                                            parse_mode='html')
            sleep(5)
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=messageId)

            sql.delete_correct(messageId=messageId)
            sql.delete_chance(messageId=messageId)

            sql.delete_africa(messageId)
            utils.mr_logger(f"message was deleted")
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=payload.message_id)
        except:
            pass

