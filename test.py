# -*- coding: utf-8 -*-
from telegram import MessageEntity, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Bot
from telegram.ext import Updater, MessageHandler, Filters,CommandHandler,CallbackQueryHandler
from telegram.ext.dispatcher import run_async
from telegram.utils.request import Request
from telegram.error import  BadRequest
from telegram.ext import messagequeue as mq
import telegram.bot
import logging
import emoji
import utils
import configs
import botify

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
bot =Bot(token=configs.TOKEN)
logger = logging.getLogger(__name__)
sql =  utils.DBHelper()
sched = utils.SCHED
# """when new session is found"""
# #save the session
# # create 3 jobs in apschedler
# #job one to notify group & get all the questions
# #job two to start posting the question in the group
#job 3 to post answers when the time ends and delete the question




"""fetch new questions every 10 mins"""
utils.fetchSessions()
sched.add_job(utils.fetchSessions,'interval',minutes=10)

sched.print_jobs()
sched.start()






class MQBot(telegram.bot.Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()


    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
        super(MQBot, self).__del__()



    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        logger.info("native send message method called")
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot, self).send_message(*args, **kwargs)
        except:
            pass

    @mq.queuedmessage
    def edit_message_text(self, *args, **kwargs):
        logger.info("native edit message method called")
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))

        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        try:
            return super(MQBot, self).edit_message_text(*args, **kwargs)
        except:
            pass

    @mq.queuedmessage
    def pin_chat_message(self, *args,**kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
                OPTIONAL arguments'''
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot,self).pin_chat_message(*args, **kwargs)
        except BadRequest:
            pass

    @mq.queuedmessage
    def answer_callback_query(self,*args,**kwargs):
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot, self).answer_callback_query(*args, **kwargs)
        except:
            pass

    @mq.queuedmessage
    def unpin_chat_message(self, *args, **kwargs):
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot, self).unpin_chat_message(*args, **kwargs)
        except BadRequest:
            pass

    @mq.queuedmessage
    def send_audio(self, *args, **kwargs):
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot,self).send_audio(*args, **kwargs)
        except:
            pass

    @mq.queuedmessage
    def send_document(self, *args, **kwargs):
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot, self).send_document(*args, **kwargs)
        except:
            pass

    @mq.queuedmessage
    def send_video(self, *args, **kwargs):
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot, self).send_video(*args, **kwargs)
        except:
            pass

    @mq.queuedmessage
    def send_photo(self, *args, **kwargs):
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot, self).send_photo(*args, **kwargs)
        except:
            pass

    @mq.queuedmessage
    def send_voice(self, *args, **kwargs):
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot, self).send_voice(*args, **kwargs)
        except:
            pass



def main():
    # Create the EventHandler and pass it your bot's token.

    q = mq.MessageQueue(all_burst_limit=29, all_time_limit_ms=1017, group_burst_limit=15, group_time_limit_ms=55000,
                        autostart=True)
    # set connection pool size for bot
    request = Request(con_pool_size=12)
    testbot = MQBot(configs.TOKEN, request=request, mqueue=q)
    updater = telegram.ext.updater.Updater(bot=testbot, use_context=True)

    # Get the dispatcher to register handlers CallbackQueryHandler(language)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.reply & (Filters.text | Filters.voice), botify.reply_check))
    dp.add_handler(CommandHandler(command='gid',callback=botify.gid))
    dp.add_handler(MessageHandler(Filters.text,botify.save_messages))
# log all errors
#     dp.add_error_handler(botify.error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()


# while True:
#     sleep(100)
#     print("ok")