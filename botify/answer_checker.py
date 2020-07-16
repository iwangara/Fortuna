from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
import configs
import utils
import botify
import emoji
from time import sleep
sql =utils.DBHelper()
solosql = utils.DBManager()
speech = utils.Speech()
send_typing_action = utils.send_action(ChatAction.TYPING)

@send_typing_action
def reply_check(update,context):
    bot_username = update.message.reply_to_message.from_user.username

    user = update.message.from_user
    username =utils.get_username(update,context)
    user_answer = update.message.text
    group_id = update.message.chat.id
    chat_type = update.message.chat.type
    admin = utils.Admin(userid=user.id, language=configs.LANGUAGE).get_data()
    #check if the user is replying in the group and to the bot's message
    if chat_type != "private" and bot_username == configs.BOTUSERNAME:
        # chat message id
        message_id = update.message.reply_to_message.message_id
        #question type(apollo,gaia,etc)
        bot_type = utils.bot_type(message_id=message_id)
        botify.logger.warning(f'bot type: {bot_type}')
        if bot_type=='Apollo':
            # if the user is not an admin
            if admin==False:
                """register/confirm the db under the question and language"""
                res = utils.CreateStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type,
                                          name=username).get_data()
                botify.logger.warning(f'creating student api called : {res}')
                """Check how many chances a user has got remaining,1 chance per user per question"""
                tries = sql.check_try(userId=user.id, messageId=message_id, bot=bot_type)
                if tries != True:
                    """mark the user as tried the question"""
                    sql.create_chance(userId=user.id, messageId=message_id, bot=bot_type)
                    """Check user level"""
                    student = utils.GetStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
                    student_level = student['level']
                    qlevel = sql.get_apollo_level_by_msgId(msgId=message_id)
                    que_level = utils.levelq(qlevel)
                    botify.logger.warning(f'question level : {que_level}')

                    if int(que_level) >= int(student_level):
                        """Check user answer"""
                        answer = sql.get_apollo_answer_by_msgId(msgId=message_id)
                        if utils.stripper(text=user_answer) == utils.stripper(text=answer):
                            """add user's fortuna in this language and exercise"""
                            utils.AddFortunas(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
                            """increase count of users who tried this question"""
                            sql.update_correct(messageId=message_id)
        elif bot_type=='Seshat':
            if admin==False:
                """register/confirm the db under the question and language"""
                res = utils.CreateStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type,
                                          name=username).get_data()
                botify.logger.warning(f'creating student api called : {res}')
                """Check how many chances a user has got remaining,1 chance per user per question"""
                tries = sql.check_try(userId=user.id, messageId=message_id, bot=bot_type)
                if tries != True:
                    """mark the user as tried the question"""
                    sql.create_chance(userId=user.id, messageId=message_id, bot=bot_type)
                    """Check user level"""
                    student = utils.GetStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
                    student_level = student['level']
                    qlevel = sql.get_seshat_level_by_msgId(msgId=message_id)
                    que_level = utils.levelq(qlevel)
                    botify.logger.warning(f'question level : {que_level}')
                    if int(que_level) >= int(student_level):
                        """Check user answer"""
                        answer = sql.get_seshat_answer_by_msgId(msgId=message_id)
                        correct_answer=utils.stripper(text=answer).lower()
                        answer_submitted=utils.stripper(text=user_answer).lower()
                        if answer_submitted == correct_answer:
                            """add user's fortuna in this language and exercise"""
                            utils.AddFortunas(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
                            """increase count of users who tried this question"""
                            sql.update_correct(messageId=message_id)

        elif bot_type == 'Tyche':

            if admin==False:
                """register/confirm the db under the question and language"""
                res = utils.CreateStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type,
                                          name=username).get_data()
                botify.logger.warning(f'creating student api called : {res}')
                """Check how many chances a user has got remaining,1 chance per user per question"""
                tries = sql.check_try(userId=user.id, messageId=message_id, bot=bot_type)
                if tries != True:
                    """mark the user as tried the question"""
                    sql.create_chance(userId=user.id, messageId=message_id, bot=bot_type)
                    """Check user level"""
                    student = utils.GetStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
                    student_level = student['level']
                    qlevel = sql.get_tyche_level_by_msgId(msgId=message_id)
                    que_level = utils.levelq(qlevel)
                    botify.logger.warning(f'question level : {que_level}')

                    if int(que_level) >= int(student_level):
                        """Check user answer"""
                        answer = sql.get_tyche_answer_by_msgId(msgId=message_id)
                        correct_answer = utils.stripper(text=answer).lower()
                        answer_submitted = utils.stripper(text=user_answer).lower()
                        if answer_submitted == correct_answer:
                            """add user's fortuna in this language and exercise"""
                            utils.AddFortunas(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
                            """increase count of users who tried this question"""
                            sql.update_correct(messageId=message_id)

        elif bot_type == 'Leizi':
            if admin==False:
                """register/confirm the db under the question and language"""
                res = utils.CreateStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type,
                                          name=username).get_data()
                botify.logger.warning(f'creating student api called : {res}')
                """Check how many chances a user has got remaining,1 chance per user per question"""
                tries = sql.check_try(userId=user.id, messageId=message_id, bot=bot_type)
                if tries != True:
                    """mark the user as tried the question"""
                    sql.create_chance(userId=user.id, messageId=message_id, bot=bot_type)
                    """Check user level"""
                    student = utils.GetStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
                    student_level = student['level']
                    qlevel = sql.get_leizi_level_by_msgId(msgId=message_id)
                    que_level = utils.levelq(qlevel)
                    botify.logger.warning(f'question level : {que_level}')

                    if int(que_level) >= int(student_level):
                        """Check user answer"""
                        answer = sql.get_leizi_answer_by_msgId(msgId=message_id)
                        try:
                            answer1, answer2 = answer
                            correct_answer1 = utils.stripper(text=answer1).lower()
                            correct_answer2 = utils.stripper(text=answer2).lower()
                            answer_submitted = utils.stripper(text=user_answer).lower()
                            if answer_submitted == correct_answer1 or answer_submitted == correct_answer2:
                                """add user's fortuna in this language and exercise"""
                                utils.AddFortunas(userid=user.id, language=configs.LANGUAGE,
                                                  exercise=bot_type).get_data()
                                """increase count of users who tried this question"""
                                sql.update_correct(messageId=message_id)
                        except :
                            pass

        elif bot_type == 'Odin':
            if admin==False:
                """register/confirm the db under the question and language"""
                res = utils.CreateStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type,
                                          name=username).get_data()
                botify.logger.warning(f'creating student api called : {res}')
                """Check how many chances a user has got remaining,1 chance per user per question"""
                tries = sql.count_chances(userId=user.id, messageId=message_id, bot=bot_type)

                if tries ==1:
                    """mark the user as tried the question"""
                    sql.create_chance(userId=user.id, messageId=message_id, bot=bot_type)
                    """Check user level"""
                    student = utils.GetStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
                    student_level = student['level']
                    qlevel = sql.get_odin_level_by_msgId(msgId=message_id)
                    que_level = utils.levelq(qlevel)
                    botify.logger.warning(f'question level : {que_level}')

                    if int(que_level) >= int(student_level):
                        """Check user answer"""
                        # answer = sql.get_odin_answer_by_msgId(msgId=message_id)
                        query = sql.get_odin_answer_by_msgId(msgId=message_id)
                        answer, meaning = query
                        try:

                            correct_answer = utils.stripper(text=answer).lower()

                            answer_submitted = utils.stripper(text=user_answer).lower()
                            if answer_submitted == correct_answer:
                                """add user's fortuna in this language and exercise"""
                                utils.AddFortunas(userid=user.id, language=configs.LANGUAGE,
                                                  exercise=bot_type).get_data()
                                """increase count of users who tried this question"""
                                sql.update_correct(messageId=message_id)
                        except :
                            pass

        elif bot_type == 'Zamo':
            if admin==False:
                """register/confirm the db under the question and language"""
                res = utils.CreateStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type,
                                          name=username).get_data()
                botify.logger.warning(f'creating student api called : {res}')
                """Check how many chances a user has got remaining,1 chance per user per question"""
                tries = sql.check_try(userId=user.id, messageId=message_id, bot=bot_type)
                if tries != True:
                    """mark the user as tried the question"""
                    sql.create_chance(userId=user.id, messageId=message_id, bot=bot_type)
                    """Check user level"""
                    student = utils.GetStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
                    student_level = student['level']
                    qlevel = sql.get_zamo_level_by_msgId(msgId=message_id)
                    que_level = utils.levelq(qlevel)
                    botify.logger.warning(f'question level : {que_level}')
                    if int(que_level) >= int(student_level):
                        """Check user answer"""
                        answer = sql.get_zamo_answer_by_msgId(msgId=message_id)
                        correct_answer=utils.stripper(text=answer).lower()
                        answer_submitted=utils.stripper(text=user_answer).lower()
                        if answer_submitted == correct_answer:
                            """add user's fortuna in this language and exercise"""
                            utils.AddFortunas(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
                            """increase count of users who tried this question"""
                            sql.update_correct(messageId=message_id)

        elif bot_type == 'nuwa':
            print(bot_type)
            if admin == False:
                """register/confirm the db under the question and language"""
                res = utils.CreateStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type,
                                          name=username).get_data()
                botify.logger.warning(f'creating student api called : {res}')
                """Check how many chances a user has got remaining,1 chance per user per question"""
                tries = sql.check_try(userId=user.id, messageId=message_id, bot=bot_type)
                if tries != True:
                    """mark the user as tried the question"""
                    sql.create_chance(userId=user.id, messageId=message_id, bot=bot_type)
                    """Check user level"""
                    student = utils.GetStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
                    student_level = student['level']
                    qlevel = sql.get_nuwa_level_by_msgId(msgId=message_id)
                    que_level = utils.levelq(qlevel)
                    botify.logger.warning(f'question level : {que_level}')
                    if int(que_level) >= int(student_level):
                        """voice to text"""
                        answer = sql.get_nuwa_answer_by_msgId(msgId=message_id)
                        correct_answer = utils.stripper(text=answer).lower()

                        file_id = update.message.voice.file_id
                        newFile = context.bot.get_file(file_id)
                        newFile.download(f'nuwa_{user.id}.ogg')
                        length = update.message.voice.duration
                        if length < 10:
                            new = utils.convert_ogg_to_wav(f"nuwa_{user.id}.ogg",
                                                          f"nuwa_{user.id}.wav")
                            speech.file = new

                            langue = utils.language_select(language=configs.LANGUAGE)
                            text = speech.to_text(lang=langue)
                            utils.mr_logger(f"totext: {text},answer {answer}")
                            if text == 401:
                                update.message.reply_text(
                                    f"Hi {user.first_name}, I did not understand this, please try again")
                            elif text == 500:
                                update.message.reply_text(
                                    f"Sorry {user.first_name}, I got a little light headed, please try again")
                            elif text.lower() == correct_answer:
                                """add user's fortuna in this language and exercise"""
                                utils.AddFortunas(userid=user.id, language=configs.LANGUAGE,
                                                  exercise=bot_type).get_data()
                                """increase count of users who tried this question"""
                                sql.update_correct(messageId=message_id)
                                return utils.clear_nuwa(user_id=user.id)

        elif bot_type == 'gaia':
            print("BOT NAME",bot_type)
            if admin == False:
                """register/confirm the db under the question and language"""
                res = utils.CreateStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type,
                                          name=username).get_data()
                botify.logger.warning(f'creating student api called : {res}')
                """Check how many chances a user has got remaining,1 chance per user per question"""
                tries = sql.check_try(userId=user.id, messageId=message_id, bot=bot_type)
                if tries != True:
                    """mark the user as tried the question"""
                    sql.create_chance(userId=user.id, messageId=message_id, bot=bot_type)
                    """Check user level"""
                    student = utils.GetStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
                    student_level = student['level']
                    qlevel = sql.get_gaia_level_by_msgId(msgId=message_id)
                    que_level = utils.levelq(qlevel)
                    botify.logger.warning(f'question level : {que_level}')
                    if int(que_level) >= int(student_level):
                        """voice to text"""
                        answer = sql.get_gaia_answer_by_msgId(msgId=message_id)
                        correct_answer = utils.stripper(text=answer)

                        file_id = update.message.voice.file_id
                        newFile = context.bot.get_file(file_id)
                        newFile.download('gaia_{}.ogg'.format(user.id))
                        length = update.message.voice.duration
                        if length < 10:
                            new = utils.convert_ogg_to_wav(f"gaia_{user.id}.ogg",
                                                          f"gaia_{user.id}.wav")
                            speech.file = new

                            langue = utils.language_select(language=configs.LANGUAGE)
                            text = speech.to_text(lang=langue)
                            utils.mr_logger(f"totext: {text},answer {answer}")
                            if text == 401:
                                update.message.reply_text(
                                    f"Hi {user.first_name}, I did not understand this, please try again")
                            elif text == 500:
                                update.message.reply_text(
                                    f"Sorry {user.first_name}, I got a little light headed, please try again")
                            elif text.lower() == correct_answer:
                                """add user's fortuna in this language and exercise"""
                                utils.AddFortunas(userid=user.id, language=configs.LANGUAGE,
                                                  exercise=bot_type).get_data()
                                """increase count of users who tried this question"""
                                sql.update_correct(messageId=message_id)
                                return utils.clear_gaia(user_id=user.id)
    elif chat_type=='private':
        message_id = update.message.reply_to_message.message_id
        session_type =solosql.get_session_type(userid=user.id,msgid=message_id)
        if session_type=='Apollo':
            canswer = solosql.get_answer_msgid(userid=user.id, msgid=message_id)
            if utils.stripper(text=user_answer) == utils.stripper(text=canswer):
                context.bot.delete_message(chat_id=user.id, message_id=message_id)
                pl = context.bot.send_message(chat_id=user.id, text=emoji.emojize(":fire:Your Answer is Correct:fire:",
                                                                                  use_aliases=True))
                correct = solosql.get_correct(user.id)
                print("correct", correct)
                correct += 1
                solosql.update_correct(user_id=user.id, correct=correct)
                print(pl.result().message_id)
                sleep(2)
                context.bot.delete_message(chat_id=user.id, message_id=pl.result().message_id)
                session, tries = solosql.get_tries(userid=user.id)
                tries -= 1
                solosql.update_tries(user.id, tries)
                session, tries = solosql.get_tries(userid=user.id)
                print(tries)
                if tries > 0:
                    apollo_ques = solosql.get_apollo_question()
                    if apollo_ques != False:
                        question, answer = apollo_ques
                        string = utils.remove_html_tags(utils.BotMessages(id=6).get_message())
                        message = f"<b>{string}</b>\n\n:orange_book:<i>{question}</i>"

                        payload = context.bot.send_message(chat_id=user.id,
                                                           text=emoji.emojize(message, use_aliases=True),
                                                           parse_mode='html')
                        messageId = payload.result().message_id
                        solosql.update_user_question(userid=user.id, answer=answer, session='Apollo',
                                                     message_id=messageId,
                                                     tries=tries, correct=correct)
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
                    correct = solosql.get_correct(user.id)
                    msg = f":fire: Congratulations you got {correct}/10,Keep on practicing to be the G.O.A.T"
                    context.bot.send_message(chat_id=user.id, text=emoji.emojize(msg, use_aliases=True),
                                             reply_markup=main_markup)
            else:
                context.bot.delete_message(chat_id=user.id, message_id=message_id)
                pl = context.bot.send_message(chat_id=user.id,
                                              text=emoji.emojize(
                                                  f":fire:Your Answer is Incorrect, the correct answer was: <b>{canswer}</b> :fire:",
                                                  use_aliases=True), parse_mode='html')

                print(pl.result().message_id)
                sleep(3)
                context.bot.delete_message(chat_id=user.id, message_id=pl.result().message_id)
                session, tries = solosql.get_tries(userid=user.id)
                tries -= 1
                solosql.update_tries(user.id, tries)
                session, tries = solosql.get_tries(userid=user.id)
                print(tries)
                if tries > 0:
                    apollo_ques = solosql.get_apollo_question()
                    if apollo_ques != False:
                        question, answer = apollo_ques
                        string = utils.remove_html_tags(utils.BotMessages(id=6).get_message())
                        message = f"<b>{string}</b>\n\n:orange_book:<i>{question}</i>"

                        payload = context.bot.send_message(chat_id=user.id,
                                                           text=emoji.emojize(message, use_aliases=True),
                                                           parse_mode='html')
                        messageId = payload.result().message_id
                        correct = solosql.get_correct(user.id)
                        solosql.update_user_question(userid=user.id, answer=answer, session='Apollo',
                                                     message_id=messageId,
                                                     tries=tries, correct=correct)
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
                    correct = solosql.get_correct(user.id)
                    msg = f":fire: Congratulations you got {correct}/10,Keep on practicing to be the G.O.A.T"
                    context.bot.send_message(chat_id=user.id, text=emoji.emojize(msg, use_aliases=True),
                                             reply_markup=main_markup)
        elif session_type=='Gaia':
            canswer = solosql.get_answer_msgid(userid=user.id, msgid=message_id)
            correct_answer = utils.stripper(text=canswer)
            try:
                file_id = update.message.voice.file_id
                newFile = context.bot.get_file(file_id)
                newFile.download('gaia_{}.ogg'.format(user.id))
                length = update.message.voice.duration
                if length < 10:
                    new = utils.convert_ogg_to_wav(f"gaia_{user.id}.ogg",
                                                   f"gaia_{user.id}.wav")
                    speech.file = new

                    langue = utils.language_select(language=configs.LANGUAGE)
                    text = speech.to_text(lang=langue)
                    utils.mr_logger(f"totext: {text},answer {canswer}")
                    if text == 401:
                        update.message.reply_text(
                            f"Hi {user.first_name}, I did not understand this, please try again")
                    elif text == 500:
                        update.message.reply_text(
                            f"Sorry {user.first_name}, I got a little light headed, please try again")
                    elif text.lower() == correct_answer:
                        context.bot.delete_message(chat_id=user.id, message_id=message_id)
                        pl = context.bot.send_message(chat_id=user.id,
                                                      text=emoji.emojize(":fire:Your Answer is Correct:fire:",
                                                                         use_aliases=True))
                        correct = solosql.get_correct(user.id)
                        print("correct", correct)
                        correct += 1
                        solosql.update_correct(user_id=user.id, correct=correct)
                        print(pl.result().message_id)
                        sleep(2)
                        context.bot.delete_message(chat_id=user.id, message_id=pl.result().message_id)
                        session, tries = solosql.get_tries(userid=user.id)
                        tries -= 1
                        solosql.update_tries(user.id, tries)
                        session, tries = solosql.get_tries(userid=user.id)
                        print(tries)
                        utils.clear_gaia(user_id=user.id)
                        if tries > 0:
                            gaia_ques = solosql.get_gaia_question()
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
                                solosql.update_user_question(userid=user.id, answer=answer, session='Gaia',
                                                             message_id=messageId,
                                                             tries=tries, correct=correct)
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
                                         InlineKeyboardButton('Instructions',
                                                              url='https://telegra.ph/Ra-v3-tutorials-05-08')],
                                        [InlineKeyboardButton('Donate',
                                                              url='https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WJYMNYLP9TQHL&source=url')]]
                            main_markup = InlineKeyboardMarkup(key_main)
                            correct = solosql.get_correct(user.id)
                            msg = f":fire: Congratulations you got {correct}/10,Keep on practicing to be the G.O.A.T"
                            context.bot.send_message(chat_id=user.id, text=emoji.emojize(msg, use_aliases=True),
                                                     reply_markup=main_markup)
                    elif text.lower() != correct_answer:
                        context.bot.delete_message(chat_id=user.id, message_id=message_id)
                        pl = context.bot.send_message(chat_id=user.id,
                                                      text=emoji.emojize(
                                                          f":fire:Your Answer is Incorrect, the correct answer was: <b>{canswer}</b> :fire:",
                                                          use_aliases=True), parse_mode='html')

                        print(pl.result().message_id)
                        sleep(3)
                        context.bot.delete_message(chat_id=user.id, message_id=pl.result().message_id)
                        session, tries = solosql.get_tries(userid=user.id)
                        tries -= 1
                        solosql.update_tries(user.id, tries)
                        session, tries = solosql.get_tries(userid=user.id)
                        print(tries)
                        if tries > 0:
                            gaia_ques = solosql.get_gaia_question()
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
                                correct = solosql.get_correct(user.id)
                                solosql.update_user_question(userid=user.id, answer=answer, session='Gaia',
                                                             message_id=messageId,
                                                             tries=tries, correct=correct)
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
                                         InlineKeyboardButton('Instructions',
                                                              url='https://telegra.ph/Ra-v3-tutorials-05-08')],
                                        [InlineKeyboardButton('Donate',
                                                              url='https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WJYMNYLP9TQHL&source=url')]]
                            main_markup = InlineKeyboardMarkup(key_main)
                            correct = solosql.get_correct(user.id)
                            msg = f":fire: Congratulations you got {correct}/10,Keep on practicing to be the G.O.A.T"
                            context.bot.send_message(chat_id=user.id, text=emoji.emojize(msg, use_aliases=True),
                                                     reply_markup=main_markup)
            except Exception as e:
                print(e)
                string = utils.remove_html_tags(utils.BotMessages(id=7).get_message())
                message = f"<b>{string}</b>"
                context.bot.send_message(chat_id=user.id, text=emoji.emojize(message, use_aliases=True),parse_mode="html")











@send_typing_action
def gid(update,context):
    user = update.message.from_user
    chat_type = update.message.chat.type

    if chat_type == "private":
        update.message.reply_text(
            "First Name: {}\nUsername: {}\nUser ID:{}".format(user.first_name, user.username, user.id))
    else:
        update.message.reply_text("Group ID is : {}".format(update.message.chat.id))



