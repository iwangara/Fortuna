import random

import emoji
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ParseMode, Poll
import botify
import configs
import utils
from os import remove
from time import sleep
sql =utils.DBHelper()
dbs =utils.DBManager()
sched = utils.SCHED
def javis (update,context):
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
            walas = sql.get_wala_by_session_id(session_id=session_id)
            kadlus = sql.get_kadlu_by_session_id(session_id=session_id)
            nuwas = sql.get_nuwa_by_session_id(session_id=session_id)
            gaias = sql.get_gaia_by_session_id(session_id=session_id)
            if len(apollos)>0:
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent = context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id, text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
                for question in apollos:
                    sql.delete_apollo_by_qid(question[0])
                    try:

                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass

            elif len(seshats)>0:
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent = context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id, text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
                for question in seshats:
                    sql.delete_seshat_by_qid(question[0])
                    try:
                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
            elif len(leizis)>0:
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent = context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id, text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
                for question in leizis:
                    print(question)
                    sql.delete_leizi_by_qid(question[0])
                    try:

                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)

            elif len(tyches)>0:
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent = context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id, text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
                for question in tyches:
                    sql.delete_tyche_by_qid(question[0])

                    try:

                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
            elif len(odins)>0:
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent = context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id, text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
                for question in odins:
                    sql.delete_odin_by_qid(question[0])
                    try:

                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)

            elif len(zamos)>0:
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent = context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id, text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
                for question in zamos:
                    sql.delete_zamo_by_qid(question[0])

                    try:

                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
            elif len(africas)>0:
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent = context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id, text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
                for question in africas:
                    sql.delete_africa_by_qid(question[0])

                    try:

                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID,message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)


            elif len(walas)>0:
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent = context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id, text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
                for question in walas:
                    sql.delete_wala_by_qid(question[0])

                    try:

                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID,message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
            elif len(kadlus)>0:
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent = context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id, text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
                for question in kadlus:
                    sql.delete_kadlu_by_qid(question[0])

                    try:

                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID,message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)
            elif len(nuwas)>0:
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent = context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id, text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)

                for question in nuwas:
                    sql.delete_nuwa_by_qid(question[0])

                    try:

                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID,message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)

            elif len(gaias)>0:
                for question in gaias:
                    sql.delete_gaia_by_qid(question[0])

                    try:
                        sched.remove_job(job_id=str(question[0]))
                    except:
                        pass
                sql.update_session(sessId=session_id)
                msg = ":fire:The LIVE session is over. Thank you for learning with us. The next session starts soon. ❤:heart:Enjoy creative learning!❤:heart:"
                sent =context.bot.send_message(chat_id=configs.GROUPID, text=emoji.emojize(msg, use_aliases=True))
                context.bot.pin_chat_message(chat_id=configs.GROUPID,message_id=sent.message_id)
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,text="Session Stopped ✔️",
                                              message_id=update.callback_query.message.message_id)

        elif text.startswith('solo_africa'):
            session_try = dbs.get_tries(userid=user.id)
            #new user
            if session_try==False:
                print(dbs.get_tries(userid=user.id))
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                              text=emoji.emojize(
                                                  ':hourglass_flowing_sand: Please wait, generating 10 questions for you.:hourglass_flowing_sand:',
                                                  use_aliases=True),
                                              message_id=update.callback_query.message.message_id)
                sleep(2)
                context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                           message_id=update.callback_query.message.message_id)

                afri_ques = dbs.get_africa_question()
                if afri_ques != False:
                    question, answer, answer1, answer2, answer3, answer4 = afri_ques
                    pick = [answer1, answer2, answer3, answer4]
                    answer = pick[0]

                    random.shuffle(pick)
                    correct = pick.index(answer)
                    payload = context.bot.send_poll(chat_id=user.id, question=question, options=pick,
                                                    is_anonymous=True, type=Poll.QUIZ, correct_option_id=correct,
                                                    explanation=emoji.emojize(f":fire:Answer: {answer}",
                                                                              use_aliases=True))

                    message_id = payload.message_id
                    poll_id = payload.poll.id
                    correct_id = payload.poll.correct_option_id
                    dbs.update_user_question(userid=user.id, answer=correct_id, session='Africa', message_id=message_id,
                                             poll_id=poll_id, tries=10)


                else:
                    context.bot.send_message(chat_id=user.id,
                                             text="Sorry, there is no validated questions under this exercise at the moment, please select another exercise.")
                    dbs.update_tries(user_id=user.id, tries=0)
            else:
                session,tries =session_try
                if session !="Africa" and tries>0:
                    key_main = [[InlineKeyboardButton('Africa', callback_data='solo_africa'),
                                 InlineKeyboardButton('Apollo', callback_data='solo_apollo')],
                                [InlineKeyboardButton('Gaia', callback_data='solo_gaia'),
                                 InlineKeyboardButton('Kadlu', callback_data='solo_kadlu')],
                                [InlineKeyboardButton('Leizi', callback_data='solo_leizi'),
                                 InlineKeyboardButton('Nuwa', callback_data='solo_nuwa')],
                                [InlineKeyboardButton('Odin', callback_data='solo_odin'),
                                 InlineKeyboardButton('Seshat', callback_data='solo_seshat')],
                                [InlineKeyboardButton('Tyche', callback_data='solo_tyche'),
                                 InlineKeyboardButton('Wala', callback_data='solo_wala')],
                                [InlineKeyboardButton('Zamo', callback_data='solo_zamo'),
                                 InlineKeyboardButton('Instructions', url='https://telegra.ph/Ra-v3-tutorials-05-08')],
                                [InlineKeyboardButton('Donate',
                                                      url='https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WJYMNYLP9TQHL&source=url')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=user.id,
                                             text=f"Sorry, you can not start a new exercise until you finish the previous one, you have {tries} questions remaining under {session}.",reply_markup=main_markup)
                else:
                    if tries>0:
                        context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                                      text=emoji.emojize(
                                                          f':hourglass_flowing_sand: Please wait, generating {tries}questions for you.:hourglass_flowing_sand:',
                                                          use_aliases=True),
                                                      message_id=update.callback_query.message.message_id)
                        sleep(2)
                        context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                                   message_id=update.callback_query.message.message_id)

                        afri_ques = dbs.get_africa_question()
                        if afri_ques != False:
                            question, answer, answer1, answer2, answer3, answer4 = afri_ques
                            pick = [answer1, answer2, answer3, answer4]
                            answer = pick[0]

                            random.shuffle(pick)
                            correct = pick.index(answer)
                            payload = context.bot.send_poll(chat_id=user.id, question=question, options=pick,
                                                            is_anonymous=True, type=Poll.QUIZ,
                                                            correct_option_id=correct,
                                                            explanation=emoji.emojize(f":fire:Answer: {answer}",
                                                                                      use_aliases=True))

                            message_id = payload.message_id
                            poll_id = payload.poll.id
                            correct_id = payload.poll.correct_option_id
                            dbs.update_user_question(userid=user.id, answer=correct_id, session='Africa',
                                                     message_id=message_id,
                                                     poll_id=poll_id, tries=tries)
                    else:
                        context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                                      text=emoji.emojize(
                                                          f':hourglass_flowing_sand: Please wait, generating 10 questions for you.:hourglass_flowing_sand:',
                                                          use_aliases=True),
                                                      message_id=update.callback_query.message.message_id)
                        sleep(2)
                        context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                                   message_id=update.callback_query.message.message_id)

                        afri_ques = dbs.get_africa_question()
                        if afri_ques != False:
                            question, answer, answer1, answer2, answer3, answer4 = afri_ques
                            pick = [answer1, answer2, answer3, answer4]
                            answer = pick[0]

                            random.shuffle(pick)
                            correct = pick.index(answer)
                            payload = context.bot.send_poll(chat_id=user.id, question=question, options=pick,
                                                            is_anonymous=True, type=Poll.QUIZ,
                                                            correct_option_id=correct,
                                                            explanation=emoji.emojize(f":fire:Answer: {answer}",
                                                                                      use_aliases=True))

                            message_id = payload.message_id
                            poll_id = payload.poll.id
                            correct_id = payload.poll.correct_option_id
                            dbs.update_user_question(userid=user.id, answer=correct_id, session='Africa',
                                                     message_id=message_id,
                                                     poll_id=poll_id, tries=10)



        elif text.startswith('solo_apollo'):
            session_try = dbs.get_tries(userid=user.id)
            #new user
            if session_try == False:
                print(dbs.get_tries(userid=user.id))
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                              text=emoji.emojize(
                                                  ':hourglass_flowing_sand: Please wait, generating 10 questions for you.:hourglass_flowing_sand:',
                                                  use_aliases=True),
                                              message_id=update.callback_query.message.message_id)
                sleep(2)
                context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                           message_id=update.callback_query.message.message_id)
                apollo_ques = dbs.get_apollo_question()
                if apollo_ques != False:
                    question, answer = apollo_ques
                    string = utils.remove_html_tags(utils.BotMessages(id=6).get_message())
                    message = f"<b>{string}</b>\n\n:orange_book:<i>{question}</i>"

                    payload = context.bot.send_message(chat_id=user.id,
                                                    text=emoji.emojize(message, use_aliases=True), parse_mode='html')
                    messageId = payload.result().message_id
                    dbs.update_user_question(userid=user.id, answer=answer, session='Apollo', message_id=messageId,tries=10,correct=0)
                    # dbs.update_correct(user_id=user.id, correct=0)
                else:
                    context.bot.send_message(chat_id=user.id,
                                             text="Sorry, there is no validated questions under this exercise at the moment, please select another exercise.")
                    dbs.update_tries(user_id=user.id, tries=0)
            else:
                session, tries = session_try
                if session !="Apollo" and tries>0:
                    key_main = [[InlineKeyboardButton('Africa', callback_data='solo_africa'),
                                 InlineKeyboardButton('Apollo', callback_data='solo_apollo')],
                                [InlineKeyboardButton('Gaia', callback_data='solo_gaia'),
                                 InlineKeyboardButton('Kadlu', callback_data='solo_kadlu')],
                                [InlineKeyboardButton('Leizi', callback_data='solo_leizi'),
                                 InlineKeyboardButton('Nuwa', callback_data='solo_nuwa')],
                                [InlineKeyboardButton('Odin', callback_data='solo_odin'),
                                 InlineKeyboardButton('Seshat', callback_data='solo_seshat')],
                                [InlineKeyboardButton('Tyche', callback_data='solo_tyche'),
                                 InlineKeyboardButton('Wala', callback_data='solo_wala')],
                                [InlineKeyboardButton('Zamo', callback_data='solo_zamo'),
                                 InlineKeyboardButton('Instructions', url='https://telegra.ph/Ra-v3-tutorials-05-08')],
                                [InlineKeyboardButton('Donate',
                                                      url='https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WJYMNYLP9TQHL&source=url')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=user.id,
                                             text=f"Sorry, you can not start a new exercise until you finish the previous one, you have {tries} questions remaining under {session}.",reply_markup=main_markup)
                else:
                    if tries > 0:
                        context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                                      text=emoji.emojize(
                                                          f':hourglass_flowing_sand: Please wait, generating {tries}questions for you.:hourglass_flowing_sand:',
                                                          use_aliases=True),
                                                      message_id=update.callback_query.message.message_id)
                        sleep(2)
                        context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                                   message_id=update.callback_query.message.message_id)
                        apollo_ques = dbs.get_apollo_question()
                        if apollo_ques != False:
                            question, answer = apollo_ques
                            string = utils.remove_html_tags(utils.BotMessages(id=6).get_message())
                            message = f"<b>{string}</b>\n\n:orange_book:<i>{question}</i>"

                            payload = context.bot.send_message(chat_id=user.id,
                                                               text=emoji.emojize(message, use_aliases=True),
                                                               parse_mode='html')
                            messageId = payload.result().message_id
                            correct=dbs.get_correct(userid=user.id)
                            dbs.update_user_question(userid=user.id, answer=answer, session='Apollo',
                                                     message_id=messageId,
                                                     tries=tries,correct=correct)
                    else:
                        context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                                      text=emoji.emojize(
                                                          f':hourglass_flowing_sand: Please wait, generating 10 questions for you.:hourglass_flowing_sand:',
                                                          use_aliases=True),
                                                      message_id=update.callback_query.message.message_id)
                        sleep(2)
                        context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                                   message_id=update.callback_query.message.message_id)
                        apollo_ques = dbs.get_apollo_question()
                        if apollo_ques != False:
                            question, answer = apollo_ques
                            string = utils.remove_html_tags(utils.BotMessages(id=6).get_message())
                            message = f"<b>{string}</b>\n\n:orange_book:<i>{question}</i>"

                            payload = context.bot.send_message(chat_id=user.id,
                                                               text=emoji.emojize(message, use_aliases=True),
                                                               parse_mode='html')
                            messageId = payload.result().message_id
                            dbs.update_user_question(userid=user.id, answer=answer, session='Apollo',
                                                     message_id=messageId,
                                                     tries=10,correct=0)




        elif text.startswith('solo_gaia'):
            session_try = dbs.get_tries(userid=user.id)
            # new user
            if session_try == False:
                print(dbs.get_tries(userid=user.id))
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                              text=emoji.emojize(
                                                  ':hourglass_flowing_sand: Please wait, generating 10 questions for you.:hourglass_flowing_sand:',
                                                  use_aliases=True),
                                              message_id=update.callback_query.message.message_id)
                sleep(2)
                context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                           message_id=update.callback_query.message.message_id)
                gaia_ques = dbs.get_gaia_question()
                if gaia_ques!=False:
                    question, answer = gaia_ques
                    string = utils.remove_html_tags(utils.BotMessages(id=7).get_message())
                    message = f"<b>{string}</b>"
                    voice = utils.zamol_download(url=question)
                    payload = context.bot.send_audio(chat_id=user.id, audio=open(voice, 'rb'),
                                                  caption=emoji.emojize(message, use_aliases=True), parse_mode='html')
                    # sleep(2)
                    # remove(voice)
                    messageId = payload.result().message_id
                    dbs.update_user_question(userid=user.id, answer=answer, session='Gaia', message_id=messageId,
                                             tries=10,correct=0)
                    # dbs.update_correct(user_id=user.id, correct=0)
                else:
                    context.bot.send_message(chat_id=user.id,
                                             text="Sorry, there is no validated questions under this exercise at the moment, please select another exercise.")
                    dbs.update_tries(user_id=user.id, tries=0)
            else:
                session, tries = session_try
                if session != "Gaia" and tries > 0:
                    key_main = [[InlineKeyboardButton('Africa', callback_data='solo_africa'),
                                 InlineKeyboardButton('Apollo', callback_data='solo_apollo')],
                                [InlineKeyboardButton('Gaia', callback_data='solo_gaia'),
                                 InlineKeyboardButton('Kadlu', callback_data='solo_kadlu')],
                                [InlineKeyboardButton('Leizi', callback_data='solo_leizi'),
                                 InlineKeyboardButton('Nuwa', callback_data='solo_nuwa')],
                                [InlineKeyboardButton('Odin', callback_data='solo_odin'),
                                 InlineKeyboardButton('Seshat', callback_data='solo_seshat')],
                                [InlineKeyboardButton('Tyche', callback_data='solo_tyche'),
                                 InlineKeyboardButton('Wala', callback_data='solo_wala')],
                                [InlineKeyboardButton('Zamo', callback_data='solo_zamo'),
                                 InlineKeyboardButton('Instructions', url='https://telegra.ph/Ra-v3-tutorials-05-08')],
                                [InlineKeyboardButton('Donate',
                                                      url='https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WJYMNYLP9TQHL&source=url')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=user.id,
                                             text=f"Sorry, you can not start a new exercise until you finish the previous one, you have {tries} questions remaining under {session}.",
                                             reply_markup=main_markup)
                else:
                    if tries > 0:
                        context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                                      text=emoji.emojize(
                                                          f':hourglass_flowing_sand: Please wait, generating {tries}questions for you.:hourglass_flowing_sand:',
                                                          use_aliases=True),
                                                      message_id=update.callback_query.message.message_id)
                        sleep(2)
                        context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                                   message_id=update.callback_query.message.message_id)
                        gaia_ques = dbs.get_gaia_question()
                        if gaia_ques != False:
                            question, answer = gaia_ques
                            string = utils.remove_html_tags(utils.BotMessages(id=7).get_message())
                            message = f"<b>{string}</b>"
                            voice = utils.zamol_download(url=question)
                            payload = context.bot.send_audio(chat_id=user.id, audio=open(voice, 'rb'),
                                                             caption=emoji.emojize(message, use_aliases=True),
                                                             parse_mode='html')
                            # sleep(2)
                            # remove(voice)
                            messageId = payload.result().message_id
                            correct = dbs.get_correct(userid=user.id)
                            dbs.update_user_question(userid=user.id, answer=answer, session='Gaia',
                                                     message_id=messageId,
                                                     tries=tries,correct=correct)
                    else:
                        context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                                      text=emoji.emojize(
                                                          f':hourglass_flowing_sand: Please wait, generating 10 questions for you.:hourglass_flowing_sand:',
                                                          use_aliases=True),
                                                      message_id=update.callback_query.message.message_id)
                        sleep(2)
                        context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                                   message_id=update.callback_query.message.message_id)

                        gaia_ques = dbs.get_gaia_question()
                        if gaia_ques != False:
                            question, answer = gaia_ques
                            string = utils.remove_html_tags(utils.BotMessages(id=7).get_message())
                            message = f"<b>{string}</b>"
                            voice = utils.zamol_download(url=question)
                            payload = context.bot.send_audio(chat_id=user.id, audio=open(voice, 'rb'),
                                                             caption=emoji.emojize(message, use_aliases=True),
                                                             parse_mode='html')
                            # sleep(2)
                            # remove(voice)
                            messageId = payload.result().message_id
                            dbs.update_user_question(userid=user.id, answer=answer, session='Gaia',
                                                     message_id=messageId,
                                                     tries=10,correct=0)
                            # dbs.update_correct(user_id=user.id, correct=0)



        elif text.startswith('solo_kadlu'):
            session_try = dbs.get_tries(userid=user.id)
            # new user
            if session_try == False:
                print(dbs.get_tries(userid=user.id))
                context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                              text=emoji.emojize(
                                                  ':hourglass_flowing_sand: Please wait, generating Kadlu Main question for you.:hourglass_flowing_sand:',
                                                  use_aliases=True),
                                              message_id=update.callback_query.message.message_id)
                sleep(6)
                context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                           message_id=update.callback_query.message.message_id)
                kadlu_ques = dbs.get_kadlu_main()
                if kadlu_ques != False:
                    main_id, main_question =kadlu_ques
                    kadlu_count=dbs.get_kadlu_count_main_id(main_id)
                    string = utils.remove_html_tags(utils.BotMessages(id=13).get_message()).split('.')
                    fmt = ".\n".join(string)
                    message = f"<b>{fmt}</b>"
                    voice = utils.zamol_download(url=main_question)
                    payload = context.bot.send_audio(chat_id=user.id, audio=open(voice, 'rb'),
                                                  caption=emoji.emojize(message, use_aliases=True),
                                                  parse_mode='html')
                    messageId = payload.result().message_id
                    dbs.update_user_question(userid=user.id, answer=main_question, session='Kadlu',
                                             message_id=messageId,poll_id=main_id,
                                             tries=kadlu_count, correct=0)
                    sleep(2)
                    context.bot.delete_message(chat_id=user.id,
                                               message_id=messageId)
                    kadlu_min_id =dbs.get_kadlu_min_qstn_id(main_id)
                    next_id=dbs.get_kadlu_next_id(kadlu_min_id)
                    dbs.update_user_msg_id(user_id=user.id,msgid=next_id)
                    kadlu_first =dbs.get_kadlu_qstn_by_id(kadlu_min_id)
                    kadlu_count = dbs.get_kadlu_count_main_id(main_id)
                    if kadlu_first!=False:
                        question,answer1, answer2, answer3, answer4 =kadlu_first
                        pick = [answer1, answer2, answer3, answer4]
                        answer = pick[0]

                        random.shuffle(pick)
                        correct = pick.index(answer)
                        payload = context.bot.send_poll(chat_id=user.id, question=question, options=pick,
                                                        is_anonymous=True, type=Poll.QUIZ, correct_option_id=correct,
                                                        explanation=emoji.emojize(f":fire:Answer: {answer}",
                                                                                  use_aliases=True))

                        message_id = payload.message_id
                        poll_id = payload.poll.id
                        correct_id = payload.poll.correct_option_id
                        dbs.update_user_question(userid=user.id, answer=correct_id, session='Kadlu',
                                                 message_id=message_id,
                                                 poll_id=poll_id, tries=kadlu_count,correct=next_id)

                else:
                    context.bot.send_message(chat_id=user.id,
                                             text="Sorry, there is no validated questions under this exercise at the moment, please select another exercise.")
                    dbs.update_tries(user_id=user.id, tries=0)
            else:
                session,tries =session_try
                if session !="Kadlu" and tries>0:
                    key_main = [[InlineKeyboardButton('Africa', callback_data='solo_africa'),
                                 InlineKeyboardButton('Apollo', callback_data='solo_apollo')],
                                [InlineKeyboardButton('Gaia', callback_data='solo_gaia'),
                                 InlineKeyboardButton('Kadlu', callback_data='solo_kadlu')],
                                [InlineKeyboardButton('Leizi', callback_data='solo_leizi'),
                                 InlineKeyboardButton('Nuwa', callback_data='solo_nuwa')],
                                [InlineKeyboardButton('Odin', callback_data='solo_odin'),
                                 InlineKeyboardButton('Seshat', callback_data='solo_seshat')],
                                [InlineKeyboardButton('Tyche', callback_data='solo_tyche'),
                                 InlineKeyboardButton('Wala', callback_data='solo_wala')],
                                [InlineKeyboardButton('Zamo', callback_data='solo_zamo'),
                                 InlineKeyboardButton('Instructions', url='https://telegra.ph/Ra-v3-tutorials-05-08')],
                                [InlineKeyboardButton('Donate',
                                                      url='https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WJYMNYLP9TQHL&source=url')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=user.id,
                                             text=f"Sorry, you can not start a new exercise until you finish the previous one, you have {tries} questions remaining under {session}.",reply_markup=main_markup)
                else:
                    if tries > 0:
                        context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                                      text=emoji.emojize(
                                                          f':hourglass_flowing_sand: Please wait, generating {tries} questions from your previous session.:hourglass_flowing_sand:',
                                                          use_aliases=True),
                                                      message_id=update.callback_query.message.message_id)
                        sleep(6)
                        context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                                   message_id=update.callback_query.message.message_id)
                        kadlu_ques = dbs.get_kadlu_main()
                        if kadlu_ques != False:
                            main_id, main_question = kadlu_ques
                            kadlu_count = dbs.get_kadlu_count_main_id(main_id)
                            string = utils.remove_html_tags(utils.BotMessages(id=13).get_message()).split('.')
                            fmt = ".\n".join(string)
                            message = f"<b>{fmt}</b>"
                            voice = utils.zamol_download(url=main_question)
                            payload = context.bot.send_audio(chat_id=user.id, audio=open(voice, 'rb'),
                                                             caption=emoji.emojize(message, use_aliases=True),
                                                             parse_mode='html')
                            messageId = payload.result().message_id
                            dbs.update_user_question(userid=user.id, answer=main_question, session='Kadlu',
                                                     message_id=messageId, poll_id=main_id,
                                                     tries=kadlu_count, correct=0)
                            sleep(2)
                            context.bot.delete_message(chat_id=user.id,
                                                       message_id=messageId)
                            kadlu_min_id = dbs.get_kadlu_min_qstn_id(main_id)
                            next_id = dbs.get_kadlu_next_id(kadlu_min_id)
                            dbs.update_user_msg_id(user_id=user.id, msgid=next_id)
                            kadlu_first = dbs.get_kadlu_qstn_by_id(kadlu_min_id)
                            if kadlu_first != False:
                                question, answer1, answer2, answer3, answer4 = kadlu_first
                                pick = [answer1, answer2, answer3, answer4]
                                answer = pick[0]

                                random.shuffle(pick)
                                correct = pick.index(answer)
                                payload = context.bot.send_poll(chat_id=user.id, question=question, options=pick,
                                                                is_anonymous=True, type=Poll.QUIZ,
                                                                correct_option_id=correct,
                                                                explanation=emoji.emojize(f":fire:Answer: {answer}",
                                                                                          use_aliases=True))

                                message_id = payload.message_id
                                poll_id = payload.poll.id
                                correct_id = payload.poll.correct_option_id
                                dbs.update_user_question(userid=user.id, answer=correct_id, session='Kadlu',
                                                         message_id=message_id,
                                                         poll_id=poll_id, tries=kadlu_count,correct=next_id)

                        else:
                            context.bot.send_message(chat_id=user.id,
                                                     text="Sorry, there is no validated questions under this exercise at the moment, please select another exercise.")
                            dbs.update_tries(user_id=user.id,tries=0)
                    else:
                        kadlu_ques = dbs.get_kadlu_main()
                        if kadlu_ques != False:
                            main_id, main_question = kadlu_ques
                            kadlu_count = dbs.get_kadlu_count_main_id(main_id)
                            context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                                          text=emoji.emojize(
                                                              f':hourglass_flowing_sand: Please wait, generating {kadlu_count} questions for you.:hourglass_flowing_sand:',
                                                              use_aliases=True),
                                                          message_id=update.callback_query.message.message_id)
                            sleep(2)
                            context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                                       message_id=update.callback_query.message.message_id)
                            string = utils.remove_html_tags(utils.BotMessages(id=13).get_message()).split('.')
                            fmt = ".\n".join(string)
                            message = f"<b>{fmt}</b>"
                            voice = utils.zamol_download(url=main_question)
                            payload = context.bot.send_audio(chat_id=user.id, audio=open(voice, 'rb'),
                                                             caption=emoji.emojize(message, use_aliases=True),
                                                             parse_mode='html')
                            messageId = payload.result().message_id
                            dbs.update_user_question(userid=user.id, answer=main_question, session='Kadlu',
                                                     message_id=messageId, poll_id=main_id,
                                                     tries=kadlu_count, correct=0)
                            sleep(2)
                            context.bot.delete_message(chat_id=user.id,
                                                       message_id=messageId)
                            kadlu_min_id = dbs.get_kadlu_min_qstn_id(main_id)
                            next_id = dbs.get_kadlu_next_id(kadlu_min_id)
                            dbs.update_user_msg_id(user_id=user.id, msgid=next_id)
                            kadlu_first = dbs.get_kadlu_qstn_by_id(kadlu_min_id)
                            if kadlu_first != False:
                                question, answer1, answer2, answer3, answer4 = kadlu_first
                                pick = [answer1, answer2, answer3, answer4]
                                answer = pick[0]

                                random.shuffle(pick)
                                correct = pick.index(answer)
                                payload = context.bot.send_poll(chat_id=user.id, question=question, options=pick,
                                                                is_anonymous=True, type=Poll.QUIZ,
                                                                correct_option_id=correct,
                                                                explanation=emoji.emojize(f":fire:Answer: {answer}",
                                                                                          use_aliases=True))

                                message_id = payload.message_id
                                poll_id = payload.poll.id
                                correct_id = payload.poll.correct_option_id
                                dbs.update_user_question(userid=user.id, answer=correct_id, session='Kadlu',
                                                         message_id=message_id,
                                                         poll_id=poll_id, tries=kadlu_count,correct=next_id)

                        else:
                            context.bot.send_message(chat_id=user.id,
                                                     text="Sorry, there is no validated questions under this exercise at the moment, please select another exercise.")
                            dbs.update_tries(user_id=user.id, tries=0)
        elif text.startswith('solo_leizi'):
            context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                          text=emoji.emojize(':hourglass_flowing_sand: Please wait, generating 10 questions for you.:hourglass_flowing_sand:',
                                                             use_aliases=True),
                                          message_id=update.callback_query.message.message_id, )
        elif text.startswith('solo_nuwa'):
            context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                          text=emoji.emojize(':hourglass_flowing_sand: Please wait, generating 10 questions for you.:hourglass_flowing_sand:',
                                                             use_aliases=True),
                                          message_id=update.callback_query.message.message_id, )
        elif text.startswith('solo_odin'):
            context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                          text=emoji.emojize(':hourglass_flowing_sand: Please wait, generating 10 questions for you.:hourglass_flowing_sand:',
                                                             use_aliases=True),
                                          message_id=update.callback_query.message.message_id, )
        elif text.startswith('solo_seshat'):
            context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                          text=emoji.emojize(':hourglass_flowing_sand: Please wait, generating 10 questions for you.:hourglass_flowing_sand:',
                                                             use_aliases=True),
                                          message_id=update.callback_query.message.message_id, )
        elif text.startswith('solo_tyche'):
            context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                          text=emoji.emojize(
                                              ':hourglass_flowing_sand: Please wait, generating 10 questions for you.:hourglass_flowing_sand:',
                                              use_aliases=True),
                                          message_id=update.callback_query.message.message_id, )

        elif text.startswith('solo_wala'):
            context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                          text=emoji.emojize(
                                              ':hourglass_flowing_sand: Please wait, generating 10 questions for you.:hourglass_flowing_sand:',
                                              use_aliases=True),
                                          message_id=update.callback_query.message.message_id, )

        elif text.startswith('solo_zamo'):
            context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                          text=emoji.emojize(
                                              ':hourglass_flowing_sand: Please wait, generating 10 questions for you.:hourglass_flowing_sand:',
                                              use_aliases=True),
                                          message_id=update.callback_query.message.message_id, )
def poll_listener(update,context):
    print("sssssss",update)
    user = update.poll_answer.user
    poll_id = update.poll_answer.poll_id
    user_answer = update.poll_answer.option_ids[0]
    print(poll_id, user.id, user_answer)
    admin = utils.Admin(userid=user.id, language=configs.LANGUAGE).get_data()
    if user.username is None or user.username=="":
        username = user.first_name
    else:
        username = user.username


    bot_type = utils.bot_poll_type(poll_id)
    if admin == False:
        if bot_type=='africa':
            """register/confirm the db under the question and language"""
            res = utils.CreateStudent(userid=user.id, language=configs.LANGUAGE, exercise=f'{bot_type}',
                                      name=username).get_data()
            botify.logger.warning(f'creating student api called : {res}')
            """Check user level"""
            student = utils.GetStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()

            student_level = student['level']
            qlevel = sql.get_africa_level_by_pollId(pollId=poll_id)
            que_level = utils.levelq(qlevel)
            botify.logger.warning(f'question level : {que_level}')
            if int(que_level) >= int(student_level):
                answer = sql.get_africa_answer_by_pollId(pollId=poll_id)
                print('answert', user_answer, answer)
                if answer == user_answer:
                    """add user's fortuna in this language and exercise"""
                    utils.AddFortunas(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
        elif bot_type=='wala':
            """register/confirm the db under the question and language"""
            res = utils.CreateStudent(userid=user.id, language=configs.LANGUAGE, exercise=f'{bot_type}',
                                      name=username).get_data()
            botify.logger.warning(f'creating student api called : {res}')
            """Check user level"""
            student = utils.GetStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
            student_level = student['level']
            qlevel = sql.get_wala_level_by_pollId(pollId=poll_id)
            que_level = utils.levelq(qlevel)
            botify.logger.warning(f'question level : {que_level}')
            if int(que_level) >= int(student_level):
                answer = sql.get_wala_answer_by_pollId(pollId=poll_id)
                print('answert', user_answer, answer)
                if answer == user_answer:
                    """add user's fortuna in this language and exercise twice"""
                    utils.AddFortunas(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
                    utils.AddFortunas(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()

        elif bot_type=='kadlu':
            """register/confirm the db under the question and language"""
            res = utils.CreateStudent(userid=user.id, language=configs.LANGUAGE, exercise=f'{bot_type}',
                                      name=username).get_data()
            botify.logger.warning(f'creating student api called : {res}')
            """Check user level"""
            student = utils.GetStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
            student_level = student['level']
            qlevel = sql.get_kadlu_level_by_pollId(pollId=poll_id)
            que_level = utils.levelq(qlevel)
            botify.logger.warning(f'question level : {que_level}')
            if int(que_level) >= int(student_level):
                answer = sql.get_kadlu_answer_by_pollId(pollId=poll_id)
                print('answert', user_answer, answer)
                if answer == user_answer:
                    """add user's fortuna in this language and exercise twice"""
                    utils.AddFortunas(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
                    utils.AddFortunas(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()


def poll_private(update,context):
    print("wewe",update)
    poll_id = update.poll.id

    if update.poll.is_closed:
        return
    if update.poll.total_voter_count == 1:
        user_id,message_id,session =dbs.get_africa_message_id(poll_id)
        if session=='Africa':
            session, tries = dbs.get_tries(userid=user_id)
            tries -= 1
            dbs.update_tries(user_id, tries)
            session, tries = dbs.get_tries(userid=user_id)
            print(tries)
            # context.bot.stop_poll(user_id, message_id)
            sleep(4)
            context.bot.delete_message(chat_id=user_id, message_id=message_id)
            if tries > 0:
                afri_ques = dbs.get_africa_question()
                if afri_ques != False:
                    question, answer, answer1, answer2, answer3, answer4 = afri_ques
                    pick = [answer1, answer2, answer3, answer4]
                    answer = pick[0]

                    random.shuffle(pick)
                    correct = pick.index(answer)
                    payload = context.bot.send_poll(chat_id=user_id, question=question, options=pick,
                                                    is_anonymous=True, type=Poll.QUIZ, correct_option_id=correct,
                                                    explanation=emoji.emojize(f":fire:Answer: {answer}",
                                                                              use_aliases=True))

                    message_id = payload.message_id
                    poll_id = payload.poll.id
                    correct_id = payload.poll.correct_option_id
                    dbs.update_user_question(userid=user_id, answer=correct_id, session='Africa', message_id=message_id,
                                             poll_id=poll_id, tries=tries)
            else:
                key_main = [[InlineKeyboardButton('Africa', callback_data='solo_africa'),
                             InlineKeyboardButton('Apollo', callback_data='solo_apollo')],
                            [InlineKeyboardButton('Gaia', callback_data='solo_gaia'),
                             InlineKeyboardButton('Kadlu', callback_data='solo_kadlu')],
                            [InlineKeyboardButton('Leizi', callback_data='solo_leizi'),
                             InlineKeyboardButton('Nuwa', callback_data='solo_nuwa')],
                            [InlineKeyboardButton('Odin', callback_data='solo_odin'),
                             InlineKeyboardButton('Seshat', callback_data='solo_seshat')],
                            [InlineKeyboardButton('Tyche', callback_data='solo_tyche'),
                             InlineKeyboardButton('Wala', callback_data='solo_wala')],
                            [InlineKeyboardButton('Zamo', callback_data='solo_zamo'),
                             InlineKeyboardButton('Instructions', url='https://telegra.ph/Ra-v3-tutorials-05-08')],
                            [InlineKeyboardButton('Donate',
                                                  url='https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WJYMNYLP9TQHL&source=url')]]
                main_markup = InlineKeyboardMarkup(key_main)
                msg = ":fire: Congratulations you have finished your 10 question,Keep on practicing to be the G.O.A.T"
                context.bot.send_message(chat_id=user_id, text=emoji.emojize(msg, use_aliases=True),
                                         reply_markup=main_markup)
        elif session=='Kadlu':
            print('Kadlu')
            session, tries = dbs.get_tries(userid=user_id)
            tries -= 1
            dbs.update_tries(user_id, tries)
            session, tries = dbs.get_tries(userid=user_id)
            print(tries)
            # context.bot.stop_poll(user_id, message_id)
            sleep(4)
            context.bot.delete_message(chat_id=user_id, message_id=message_id)
            if tries > 0:
                kadlu_min_id = dbs.get_user_nextqstn_id(user_id)
                next_id = dbs.get_kadlu_next_id(kadlu_min_id)
                dbs.update_user_msg_id(user_id=user_id, msgid=next_id)
                kadlu_first = dbs.get_kadlu_qstn_by_id(kadlu_min_id)
                print("kadlufirst",kadlu_first)
                if kadlu_first != False:
                    question, answer1, answer2, answer3, answer4 = kadlu_first
                    pick = [answer1, answer2, answer3, answer4]
                    answer = pick[0]

                    random.shuffle(pick)
                    correct = pick.index(answer)
                    payload = context.bot.send_poll(chat_id=user_id, question=question, options=pick,
                                                    is_anonymous=True, type=Poll.QUIZ,
                                                    correct_option_id=correct,
                                                    explanation=emoji.emojize(f":fire:Answer: {answer}",
                                                                              use_aliases=True))

                    message_id = payload.message_id
                    poll_id = payload.poll.id
                    correct_id = payload.poll.correct_option_id
                    dbs.update_user_question(userid=user_id, answer=correct_id, session='Kadlu',
                                             message_id=message_id,
                                             poll_id=poll_id, tries=tries,correct=next_id)

            else:
                key_main = [[InlineKeyboardButton('Africa', callback_data='solo_africa'),
                             InlineKeyboardButton('Apollo', callback_data='solo_apollo')],
                            [InlineKeyboardButton('Gaia', callback_data='solo_gaia'),
                             InlineKeyboardButton('Kadlu', callback_data='solo_kadlu')],
                            [InlineKeyboardButton('Leizi', callback_data='solo_leizi'),
                             InlineKeyboardButton('Nuwa', callback_data='solo_nuwa')],
                            [InlineKeyboardButton('Odin', callback_data='solo_odin'),
                             InlineKeyboardButton('Seshat', callback_data='solo_seshat')],
                            [InlineKeyboardButton('Tyche', callback_data='solo_tyche'),
                             InlineKeyboardButton('Wala', callback_data='solo_wala')],
                            [InlineKeyboardButton('Zamo', callback_data='solo_zamo'),
                             InlineKeyboardButton('Instructions', url='https://telegra.ph/Ra-v3-tutorials-05-08')],
                            [InlineKeyboardButton('Donate',
                                                  url='https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WJYMNYLP9TQHL&source=url')]]
                main_markup = InlineKeyboardMarkup(key_main)
                msg = ":fire: Congratulations you have finished your questions,Keep on practicing to be the G.O.A.T"
                context.bot.send_message(chat_id=user_id, text=emoji.emojize(msg, use_aliases=True),
                                         reply_markup=main_markup)
