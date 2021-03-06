# -*- coding: utf-8 -*-
from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler, PicklePersistence, \
    PollAnswerHandler, PollHandler
from telegram.utils.request import Request
from telegram.error import  BadRequest
from telegram.ext import messagequeue as mq
import telegram.bot
import logging
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
# utils.fetchSessions()
# sched.add_job(utils.fetchSessions, 'interval', minutes=5)


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
        except Exception as e:
            print(e)
            logger.warning(e)
            return e



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
    """Instanciate a Defaults object"""

    # Create the EventHandler and pass it your bot's token.
    q = mq.MessageQueue(all_burst_limit=29, all_time_limit_ms=1017, group_burst_limit=15, group_time_limit_ms=55000,
                        autostart=True)
    # set connection pool size for bot
    request = Request(con_pool_size=12)
    testbot = MQBot(configs.TOKEN, request=request, mqueue=q)
    pp = PicklePersistence(filename='rabot',store_bot_data=True)
    updater = telegram.ext.updater.Updater(bot=testbot,persistence=pp, use_context=True)

    # Get the dispatcher to register handlers CallbackQueryHandler(language)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.regex('^TOP$'), botify.top))
    dp.add_handler(MessageHandler(Filters.regex('^PROGRESS$'), botify.check_progress))
    dp.add_handler(MessageHandler(Filters.regex('^HELP$'), botify.help))
    dp.add_handler(MessageHandler(Filters.regex('^MY RA$'), botify.myra))
    dp.add_handler(MessageHandler(Filters.regex('^PROFILE$'), botify.profile))
    dp.add_handler(CommandHandler(command='start', callback=botify.start))
    dp.add_handler(CommandHandler(command='help', callback=botify.help))
    dp.add_handler(CommandHandler(command='top', callback=botify.top))
    dp.add_handler(CommandHandler(command='gid',callback=botify.gid))
    dp.add_handler(CommandHandler(command='solo', callback=botify.solo_learn))
    dp.add_handler(CommandHandler(command='progress', callback=botify.check_progress))
    dp.add_handler(CommandHandler(command='studyrooms', callback=botify.studyrooms))
    dp.add_handler(CommandHandler(command='teachers', callback=botify.teachers))
    dp.add_handler(CommandHandler(command='classrooms', callback=botify.classrooms))
    dp.add_handler(CommandHandler(command='rector', callback=botify.rector))
    dp.add_handler(CommandHandler(command='settopic', callback=botify.settopic))
    dp.add_handler(CommandHandler(command='support', callback=botify.ask_donation))
    dp.add_handler(CommandHandler(command='topic', callback=botify.topic))
    dp.add_handler(CommandHandler(command='stop', callback=botify.session_manager))
    dp.add_handler(MessageHandler(Filters.command & Filters.reply & Filters.group,botify.bonus))
    dp.add_handler(MessageHandler(Filters.reply & (Filters.text | Filters.voice), botify.reply_check))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,botify.unauth_group))
    dp.add_handler(MessageHandler(Filters.text,botify.message_counter))
    dp.add_handler(MessageHandler(Filters.dice, botify.solo_learn))
    dp.add_handler(CallbackQueryHandler(botify.javis))
    dp.add_handler(PollHandler(botify.poll_private))
    dp.add_handler(PollAnswerHandler(botify.poll_listener))
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
