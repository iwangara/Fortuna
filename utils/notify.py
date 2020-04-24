from telegram import Bot
import configs
import utils
import re
import datetime
import emoji
from time import sleep
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

    def session_start(self,bot, questions, total_time):
        try:
            stringg = utils.BotMessages(id=4).get_message()
            message = stringg.replace('strong', 'b').replace('<p>', '').replace('</p>', '').replace('<li>',
                                                                                                    '▪️').replace(
                '<ul>', '\n').replace('</ul>', '').replace('</li>', '\n')
            print(message)
            timeinmins =int(total_time)/60
            payload = self.bot.send_message(chat_id=configs.GROUPID,
                                            text=message.format(bot,questions,timeinmins),parse_mode='html')
            self.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=payload.message_id)
        except:
            pass

    def apollo_post(self,queId,question):
        string=utils.BotMessages(id=6).get_message()
        string =string.replace("<p>","<b>").replace("</p>","</b>")
        message=f"{emoji.emojize(string,use_aliases=True)}\n\n<i>{question}</i>\n\n<b>Time remaining: 50 seconds.</b>"
        payload = self.bot.send_message(chat_id=configs.GROUPID,
                                        text=message, parse_mode='html')
        messageId =payload.message_id
        print("posted mess",messageId)
        sql.set_apollo_messageId(messageId=messageId,queId=queId)
        sql.create_correct(messageId=messageId)

        #sleep for 49 seconds then post answer
        post_time = datetime.datetime.now()
        print("post time",post_time)
        new_time = post_time + datetime.timedelta(seconds=int(49))
        answer_time= new_time.strftime("%Y-%m-%d %H:%M:%S")
        print("post answer",answer_time)
        scheduler.add_job(self.post_apollo_answer,'date',run_date=answer_time,args=[messageId])

    def post_apollo_answer(self,messageId):
        try:
            answer = sql.get_apollo_answer_by_msgId(msgId=messageId)
            # self.bot.delete_message()
            string = utils.BotMessages(id=3).get_message()
            total = sql.check_correct(messageId=messageId)
            message = string.replace('strong', 'b').replace('<p>', '').replace('</p>', '').replace('<li>',
                                                                                                   '▪️').replace(
                '<ul>', '\n').replace('</ul>', '').replace('</li>', '\n')

            payload = self.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(message,use_aliases=True).format(answer, total),
                                            parse_mode='html')
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=messageId)

            sql.delete_correct(messageId=messageId)
            sql.delete_chance(messageId=messageId)
            sleep(10)
            sql.delete_apollo(messageId)
            self.bot.delete_message(chat_id=configs.GROUPID, message_id=payload.message_id)
        except:
            pass

