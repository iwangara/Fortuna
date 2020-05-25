import emoji
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup,ParseMode
import botify
import configs
import utils
sql =utils.DBHelper()
sched = utils.SCHED
def javis(update,context):
    query = update.callback_query
    text = str(query.data)
    user = query.from_user
    chat_type = query.message.chat.type
    userId = user.id
    chat_id = query.message.chat.id
    print(text)
    if chat_type != 'private':
        if text.startswith('like'):
            user_id = text.split('+')[1]
            rank = text.split('+')[2]
            username = text.split('+')[3]
            level =text.split('+')[4]
            check_like=sql.check_likes(userid=int(user_id),liker=userId,rank=rank)
            print(check_like)
            if check_like:
                context.bot.answer_callback_query(update.callback_query.id,
                                                  text="You already liked this achievement")
            else:
                sql.create_like(userid=user_id,liker=userId,rank=rank)
                count_likes = sql.count_likes(userid=user_id,rank=rank)
                print(count_likes)
                key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {count_likes}', use_aliases=True),
                                                  callback_data=f'like+{user_id}+{rank}+{username}+{level}')]]
                main_markup = InlineKeyboardMarkup(key_main)
                bot_text = utils.remove_html_tags(utils.BotMessages(id=21).get_message())
                context.bot.edit_message_text(text=emoji.emojize(bot_text.format(username,level,rank), use_aliases=True),
                                              chat_id=update.callback_query.message.chat_id,
                                              message_id=update.callback_query.message.message_id,
                                              reply_markup=main_markup)

        elif text.startswith('odin'):
            queId = text.split('+')[1]
            word =sql.get_odin_question_by_queId(queId=int(queId))

            print(word)
            admin = utils.Admin(userid=user.id, language=configs.LANGUAGE).get_data()
            username = utils.get_username(update, context)
            bot_type ='Odin'
            if admin==False:
                """register/confirm the db under the question and language"""
                res = utils.CreateStudent(userid=user.id, language=configs.LANGUAGE, exercise='Odin',
                                          name=username).get_data()
                botify.logger.warning(f'creating student api called : {res}')
                """Check how many chances a user has got remaining,1 chance per user per question"""
                tries = sql.check_try(userId=user.id, messageId=update.callback_query.message.message_id, bot=bot_type)
                if tries != True:
                    """mark the user as tried the question"""
                    sql.create_chance(userId=user.id, messageId=update.callback_query.message.message_id, bot=bot_type)

                    context.bot.answer_callback_query(update.callback_query.id,text=emoji.emojize(f":fire:{word}:fire:",use_aliases=True))
                else:
                    print(tries)
                    context.bot.answer_callback_query(update.callback_query.id,
                                                      text=emoji.emojize(f":see_no_evil:You only peep once :see_no_evil:", use_aliases=True))

        elif text.startswith('africa'):

            admin = utils.Admin(userid=user.id, language=configs.LANGUAGE).get_data()
            username = utils.get_username(update, context)
            bot_type = 'Africa'
            if admin == False:
                """register/confirm the db under the question and language"""
                res = utils.CreateStudent(userid=user.id, language=configs.LANGUAGE, exercise='Africa',
                                          name=username).get_data()
                botify.logger.warning(f'creating student api called : {res}')
                """Check how many chances a user has got remaining,1 chance per user per question"""
                tries = sql.check_try(userId=user.id, messageId=update.callback_query.message.message_id, bot=bot_type)
                if tries != True:
                    message_id = update.callback_query.message.message_id
                    """mark the user as tried the question"""
                    sql.create_chance(userId=user.id, messageId=update.callback_query.message.message_id, bot=bot_type)
                    """Check user level"""
                    student = utils.GetStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()

                    student_level = student['level']

                    qlevel = sql.get_africa_level_by_msgId(msgId=message_id)
                    que_level = utils.levelq(qlevel)
                    botify.logger.warning(f'question level : {que_level}')
                    if int(que_level) >= int(student_level):
                        """Check user answer"""
                        answer = sql.get_africa_answer_by_msgId(msgId=message_id)
                        user_answer = text.split('+')[1]
                        if answer == user_answer:
                            """add user's fortuna in this language and exercise"""
                            utils.AddFortunas(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
                            """increase count of users who tried this question"""
                            sql.update_correct(messageId=message_id)
                            context.bot.answer_callback_query(update.callback_query.id,
                                                              text=emoji.emojize(f":fire:You answered {user_answer}. Now wait for feedback. :fire:",
                                                                                 use_aliases=True))
                        else:
                            context.bot.answer_callback_query(update.callback_query.id,
                                                              text=emoji.emojize(f":fire:You answered {user_answer} .Now wait for feedback. :fire:",
                                                                               use_aliases=True))
                else:
                    context.bot.answer_callback_query(update.callback_query.id,
                                                      text=emoji.emojize(f":fire: YOLO :fire:",
                                                                         use_aliases=True))



    else:
        if text.startswith('stop'):
            context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                     text=emoji.emojize('Come back when you change your mind :wink:',use_aliases=True),message_id=update.callback_query.message.message_id,)
        elif text.startswith('start'):
            admin_keyboard = [['MY RA', 'TOP'],
                              [emoji.emojize(':game_die:', use_aliases=True), 'PROGRESS'],
                              ['HELP', 'PROFILE']]

            join_markup = ReplyKeyboardMarkup(admin_keyboard, True, False)
            utils.CUMessages(userid=user.id, language=configs.LANGUAGE).get_data()
            botify.create_student(userid=user.id, name=utils.get_username(update, context))
            bot_text = utils.remove_html_tags(utils.BotMessages(id=18).get_message())
            context.bot.delete_message(chat_id=update.callback_query.message.chat_id,message_id=update.callback_query.message.message_id)
            context.bot.send_message(chat_id=user.id,
                                          text=emoji.emojize(bot_text,use_aliases=True),reply_markup=join_markup )
            key_main = [[InlineKeyboardButton(emoji.emojize("↪️ Go back to the group", use_aliases=True), url=f"{configs.GROUPLINK}")]]
            main_markup = InlineKeyboardMarkup(key_main)
            context.bot.send_message(chat_id=user.id,
                                     text="Go back to class", reply_markup=main_markup)
        elif text.startswith('session'):
            session_id = text.split("+")[1]
            apollos =sql.get_apollo_by_session_id(session_id=session_id)
            seshats =sql.get_seshat_by_session_id(session_id=session_id)
            tyches = sql.get_tyche_by_session_id(session_id=session_id)
            leizis = sql.get_leizi_by_session_id(session_id=session_id)
            odins = sql.get_odin_by_session_id(session_id=session_id)
            zamos = sql.get_zamo_by_session_id(session_id=session_id)
            africas = sql.get_africa_by_session_id(session_id=session_id)
            if len(apollos)>0:
                for question in apollos:
                    try:
                        sql.delete_apollo_by_qid(question[0])
                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
            elif len(seshats)>0:
                for question in seshats:

                    try:
                        sql.delete_seshat_by_qid(question[0])
                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
            elif len(leizis)>0:
                for question in leizis:

                    try:
                        sql.delete_leizi_by_qid(question[0])
                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)

            elif len(tyches)>0:
                for question in seshats:

                    try:
                        sql.delete_tyche_by_qid(question[0])
                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
            elif len(odins)>0:
                for question in odins:

                    try:
                        sql.delete_odin_by_qid(question[0])
                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)

            elif len(zamos)>0:
                for question in zamos:

                    try:
                        sql.delete_zamo_by_qid(question[0])
                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
            elif len(africas)>0:
                for question in africas:

                    try:
                        sql.delete_africa_by_qid(question[0])
                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
