from telegram import ParseMode, Bot, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.error import Unauthorized
import utils
import configs
import botify
import emoji

sql = utils.DBHelper()


# save only messages from non admins
def message_counter(update, context):
    user = update.message.from_user
    username = utils.get_username(update, context)
    admin = utils.Admin(userid=user.id, language=configs.LANGUAGE).get_data()
    chat_type = update.message.chat.type

    """RANKS DATA"""
    ranks = utils.Ranks().get_data()
    studentmsg = ranks[0]['messages']
    studentpts = ranks[0]['points']
    apprenticemsg = ranks[1]['messages']
    apprenticepts = ranks[1]['points']
    followermsg = ranks[2]['messages']
    followerpts = ranks[2]['points']
    instructormsg = ranks[3]['messages']
    instructorpts = ranks[3]['points']
    mentormsg = ranks[4]['messages']
    mentorpts = ranks[4]['points']
    teachermsg = ranks[5]['messages']
    teacherpts = ranks[5]['points']
    scholarmsg = ranks[6]['messages']
    scholarpts = ranks[6]['points']
    mastermsg = ranks[7]['messages']
    masterpts = ranks[7]['points']
    eminencemsg = ranks[8]['messages']
    eminencepts = ranks[8]['points']
    gurumsg = ranks[9]['messages']
    gurupts = ranks[9]['points']
    titanmsg = ranks[10]['messages']
    titanpts = ranks[10]['points']

    totalpts = utils.GetFortuna(userid=user.id, language=configs.LANGUAGE).get_data()
    if admin == False and chat_type != 'private':
        student = utils.Student(userid=user.id, language=configs.LANGUAGE).get_data()
        if len(student) > 0:
            # save or create use in the message table
            utils.CUMessages(userid=user.id, language=configs.LANGUAGE).get_data()
            # now get the messages
            user_messages = utils.GetMessages(userid=user.id, language=configs.LANGUAGE).get_data()
            print("check notice",sql.check_notice(userid=user.id, rank='Student'))
            if (studentpts <= totalpts < apprenticepts) and (user_messages>=studentmsg ):
                rank = 'Student'
                # check if the user congrats message was posted
                if sql.check_notice(userid=user.id, rank=rank) == False:
                    # # change user level
                    # utils.UpdateLevel(userid=user.id,language=configs.LANGUAGE)
                    # change user rank
                    utils.UpdateRank(userid=user.id, language=configs.LANGUAGE, rank=rank)
                    bot_text = utils.remove_html_tags(utils.BotMessages(id=21).get_message())
                    # congratulate the user and start likes counts
                    likes = sql.count_likes(userid=user.id, rank=rank)
                    level = 'Elementary'
                    key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                      callback_data=f'like+{user.id}+{rank}+{username}+{level}')]]

                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=configs.GROUPID,
                                             text=emoji.emojize(bot_text.format(username, level, rank),
                                                                use_aliases=True), reply_markup=main_markup)
                    # mark as notified
                    sql.create_notice(userid=user.id, rank=rank)
            elif (apprenticepts <= totalpts < followerpts) and (apprenticemsg <= user_messages):
                rank = 'Apprentice'
                if sql.check_notice(userid=user.id, rank=rank) == False:
                    # # change user level
                    # utils.UpdateLevel(userid=user.id,language=configs.LANGUAGE)
                    # change user rank
                    utils.UpdateRank(userid=user.id, language=configs.LANGUAGE, rank=rank)
                    bot_text = utils.remove_html_tags(utils.BotMessages(id=21).get_message())
                    # congratulate the user and start likes counts
                    likes = sql.count_likes(userid=user.id, rank=rank)
                    level = 'Elementary'
                    key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                      callback_data=f'like+{user.id}+{rank}+{username}+{level}')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=configs.GROUPID,
                                             text=emoji.emojize(bot_text.format(username, level, rank),
                                                                use_aliases=True), reply_markup=main_markup)
                    # mark as notified
                    sql.create_notice(userid=user.id, rank=rank)
            elif (followerpts <= totalpts < instructorpts) and (followermsg <= user_messages):
                rank = 'Follower'
                if sql.check_notice(userid=user.id, rank=rank) == False:
                    # # change user level
                    # utils.UpdateLevel(userid=user.id,language=configs.LANGUAGE)
                    # change user rank
                    utils.UpdateRank(userid=user.id, language=configs.LANGUAGE, rank=rank)
                    bot_text = utils.remove_html_tags(utils.BotMessages(id=21).get_message())
                    # congratulate the user and start likes counts
                    likes = sql.count_likes(userid=user.id, rank=rank)
                    level = 'Elementary'
                    key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                      callback_data=f'like+{user.id}+{rank}+{username}+{level}')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=configs.GROUPID,
                                             text=emoji.emojize(bot_text.format(username, level, rank),
                                                                use_aliases=True), reply_markup=main_markup)
                    # mark as notified
                    sql.create_notice(userid=user.id, rank=rank)
            elif (instructorpts <= totalpts < mentorpts) and (instructormsg <= user_messages):
                rank = 'Instructor'
                if sql.check_notice(userid=user.id, rank=rank) == False:
                    # # change user level
                    # utils.UpdateLevel(userid=user.id,language=configs.LANGUAGE)
                    # change user rank
                    utils.UpdateRank(userid=user.id, language=configs.LANGUAGE, rank=rank)
                    bot_text = utils.remove_html_tags(utils.BotMessages(id=21).get_message())
                    # congratulate the user and start likes counts
                    likes = sql.count_likes(userid=user.id, rank=rank)
                    level = 'Elementary'
                    key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                      callback_data=f'like+{user.id}+{rank}+{username}+{level}')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=configs.GROUPID,
                                             text=emoji.emojize(bot_text.format(username, level, rank),
                                                                use_aliases=True), reply_markup=main_markup)
                    # mark as notified
                    sql.create_notice(userid=user.id, rank=rank)
            elif (mentorpts <= totalpts < teacherpts) and (mentormsg <= user_messages):
                rank = 'Mentor'
                if sql.check_notice(userid=user.id, rank=rank) == False:
                    # # change user level
                    utils.UpdateLevel(userid=user.id, language=configs.LANGUAGE)
                    # change user rank
                    utils.UpdateRank(userid=user.id, language=configs.LANGUAGE, rank=rank)
                    bot_text = utils.remove_html_tags(utils.BotMessages(id=21).get_message())
                    # congratulate the user and start likes counts
                    likes = sql.count_likes(userid=user.id, rank=rank)
                    level = 'Intermediate'
                    key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                      callback_data=f'like+{user.id}+{rank}+{username}+{level}')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=configs.GROUPID,
                                             text=emoji.emojize(bot_text.format(username, level, rank),
                                                                use_aliases=True), reply_markup=main_markup)
                    # mark as notified
                    sql.create_notice(userid=user.id, rank=rank)
            elif (teacherpts <= totalpts < scholarpts) and (teachermsg <= user_messages):
                print("teacher")
                rank = 'Teacher'
                if sql.check_notice(userid=user.id, rank=rank) == False:
                    # # change user level
                    # utils.UpdateLevel(userid=user.id,language=configs.LANGUAGE)
                    # change user rank
                    utils.UpdateRank(userid=user.id, language=configs.LANGUAGE, rank=rank)
                    bot_text = utils.remove_html_tags(utils.BotMessages(id=21).get_message())
                    # congratulate the user and start likes counts
                    likes = sql.count_likes(userid=user.id, rank=rank)
                    level = 'Intermediate'
                    key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                      callback_data=f'like+{user.id}+{rank}+{username}+{level}')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=configs.GROUPID,
                                             text=emoji.emojize(bot_text.format(username, level, rank),
                                                                use_aliases=True), reply_markup=main_markup)
                    # mark as notified
                    sql.create_notice(userid=user.id, rank=rank)
            elif (scholarpts <= totalpts < masterpts) and (scholarmsg <= user_messages):
                print('scholar')
                rank = 'Scholar'
                if sql.check_notice(userid=user.id, rank=rank) == False:
                    # # change user level
                    # utils.UpdateLevel(userid=user.id,language=configs.LANGUAGE)
                    # change user rank
                    utils.UpdateRank(userid=user.id, language=configs.LANGUAGE, rank=rank)
                    bot_text = utils.remove_html_tags(utils.BotMessages(id=21).get_message())
                    # congratulate the user and start likes counts
                    likes = sql.count_likes(userid=user.id, rank=rank)
                    level = 'Intermediate'
                    key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                      callback_data=f'like+{user.id}+{rank}+{username}+{level}')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=configs.GROUPID,
                                             text=emoji.emojize(bot_text.format(username, level, rank),
                                                                use_aliases=True), reply_markup=main_markup)
                    # mark as notified
                    sql.create_notice(userid=user.id, rank=rank)
            elif (masterpts <= totalpts < eminencepts) and (mastermsg <= user_messages):
                print("master")
                rank = 'Master'
                if sql.check_notice(userid=user.id, rank=rank) == False:
                    # # change user level
                    # utils.UpdateLevel(userid=user.id,language=configs.LANGUAGE)
                    # change user rank
                    utils.UpdateRank(userid=user.id, language=configs.LANGUAGE, rank=rank)
                    bot_text = utils.remove_html_tags(utils.BotMessages(id=21).get_message())
                    # congratulate the user and start likes counts
                    likes = sql.count_likes(userid=user.id, rank=rank)
                    level = 'Intermediate'
                    key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                      callback_data=f'like+{user.id}+{rank}+{username}+{level}')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=configs.GROUPID,
                                             text=emoji.emojize(bot_text.format(username, level, rank),
                                                                use_aliases=True), reply_markup=main_markup)
                    # mark as notified
                    sql.create_notice(userid=user.id, rank=rank)
            elif (eminencepts <= totalpts < gurupts) and (eminencemsg <= user_messages):
                print("eminence")
                rank = 'Eminence'
                if sql.check_notice(userid=user.id, rank=rank) == False:
                    # # change user level
                    # utils.UpdateLevel(userid=user.id,language=configs.LANGUAGE)
                    # change user rank
                    utils.UpdateRank(userid=user.id, language=configs.LANGUAGE, rank=rank)
                    bot_text = utils.remove_html_tags(utils.BotMessages(id=21).get_message())
                    # congratulate the user and start likes counts
                    likes = sql.count_likes(userid=user.id, rank=rank)
                    level = 'Intermediate'
                    key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                      callback_data=f'like+{user.id}+{rank}+{username}+{level}')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=configs.GROUPID,
                                             text=emoji.emojize(bot_text.format(username, level, rank),
                                                                use_aliases=True), reply_markup=main_markup)
                    # mark as notified
                    sql.create_notice(userid=user.id, rank=rank)
            elif (gurupts >= totalpts < titanpts) and (gurumsg <= user_messages):
                print("guru")
                rank = 'Guru'
                if sql.check_notice(userid=user.id, rank=rank) == False:
                    # # change user level
                    # utils.UpdateLevel(userid=user.id,language=configs.LANGUAGE)
                    # change user rank
                    utils.UpdateRank(userid=user.id, language=configs.LANGUAGE, rank=rank)
                    bot_text = utils.remove_html_tags(utils.BotMessages(id=21).get_message())
                    # congratulate the user and start likes counts
                    likes = sql.count_likes(userid=user.id, rank=rank)
                    level = 'Intermediate'
                    key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                      callback_data=f'like+{user.id}+{rank}+{username}+{level}')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=configs.GROUPID,
                                             text=emoji.emojize(bot_text.format(username, level, rank),
                                                                use_aliases=True), reply_markup=main_markup)
                    # mark as notified
                    sql.create_notice(userid=user.id, rank=rank)
            elif (totalpts >= titanpts) and (user_messages >= titanmsg):
                print('titan')
                rank = 'Titan'
                if sql.check_notice(userid=user.id, rank=rank) == False:
                    # # change user level
                    utils.UpdateLevel(userid=user.id, language=configs.LANGUAGE)
                    # change user rank
                    utils.UpdateRank(userid=user.id, language=configs.LANGUAGE, rank=rank)
                    bot_text = utils.remove_html_tags(utils.BotMessages(id=21).get_message())
                    # congratulate the user and start likes counts
                    likes = sql.count_likes(userid=user.id, rank=rank)
                    level = 'Advanced'
                    key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                      callback_data=f'like+{user.id}+{rank}+{username}+{level}')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=configs.GROUPID,
                                             text=emoji.emojize(bot_text.format(username, level, rank),
                                                                use_aliases=True), reply_markup=main_markup)
                    # mark as notified
                    sql.create_notice(userid=user.id, rank=rank)


        else:
            key_main = [[InlineKeyboardButton(emoji.emojize("Join", use_aliases=True),
                                              url=f"https://t.me/{context.bot.username}?start={user.id}")]]
            main_markup = InlineKeyboardMarkup(key_main)
            bot_text = utils.remove_html_tags(utils.BotMessages(id=22).get_message())
            bot_username = f"@{context.bot.username}"
            update.message.reply_text(emoji.emojize(bot_text.format(bot_username), use_aliases=True),reply_markup=main_markup)


def start(update, context):
    user = update.message.from_user
    admin = utils.Admin(userid=user.id, language=configs.LANGUAGE).get_data()
    chat_type = update.message.chat.type
    student = utils.Student(userid=user.id, language=configs.LANGUAGE).get_data()
    if chat_type == 'private':
        if admin == False:
            if len(student) < 1:
                key_main = [
                    [InlineKeyboardButton(emoji.emojize("Agree :thumbsup:", use_aliases=True), callback_data=f"start")],
                    [InlineKeyboardButton(emoji.emojize("Disagree :x:", use_aliases=True),
                                          callback_data=f"stop")]]
                main_markup = InlineKeyboardMarkup(key_main)

                bot_text = utils.remove_html_tags(utils.BotMessages(id=24).get_message())
                context.bot.send_message(chat_id=user.id, text=emoji.emojize(bot_text, use_aliases=True),
                                         reply_markup=main_markup,parse_mode='markdown')
            else:
                admin_keyboard = [['MY RA', 'TOP'],
                                  [emoji.emojize(':game_die:',use_aliases=True), 'PROGRESS'],
                                  ['HELP', 'PROFILE']]

                join_markup = ReplyKeyboardMarkup(admin_keyboard, True, False)
                bot_text = utils.remove_html_tags(utils.BotMessages(id=18).get_message())
                context.bot.send_message(chat_id=user.id,
                                         text=emoji.emojize(bot_text, use_aliases=True), reply_markup=join_markup)

        else:
            update.message.reply_text("Hi Admin, you need to use the portal nowadays.")


def help(update, context):
    user = update.message.from_user
    admins = utils.Admin(userid=user.id, language=configs.LANGUAGE).get_data()
    student = utils.Student(userid=user.id, language=configs.LANGUAGE).get_data()
    if len(student) > 0:
        commands = utils.Commands().get_data()
        student = []
        teacher = []
        for data in commands:
            command = data['command']
            desc = data['description']
            admin = data['availability']
            if admin == 2:
                admin = "Admins only"
                bot_commands = f"{command}  - {desc}"
                teacher.append(bot_commands)
            else:
                admin = "students"
                bot_commands = f"{command}  - {desc}"
                student.append(bot_commands)
        if admins == False:
            text = "\n".join(student)
            context.bot.send_message(chat_id=user.id,
                                     text=emoji.emojize(
                                         f":fire: <b>Those who seek help will always find it!</b> :fire:\n{text}"),
                                     parse_mode='HTML')
        else:
            text = "\n".join(teacher)
            context.bot.send_message(chat_id=user.id,
                                     text=emoji.emojize(
                                         f":fire: <b>Those who seek help will always find it!</b> :fire:\n{text}"),
                                     parse_mode='HTML')
    else:
        key_main = [[InlineKeyboardButton(emoji.emojize("Join", use_aliases=True),
                                          url=f"https://t.me/{context.bot.username}?start={user.id}")]]
        main_markup = InlineKeyboardMarkup(key_main)
        bot_text = utils.remove_html_tags(utils.BotMessages(id=22).get_message())
        bot_username = f"@{context.bot.username}"
        update.message.reply_text(emoji.emojize(bot_text.format(bot_username), use_aliases=True),
                                  reply_markup=main_markup)


# check if the user started the bot
def check_progress(update, context):
    botname = context.bot.username
    chat_type = update.message.chat.type
    username = utils.get_username(update, context)
    user = update.message.from_user
    student = utils.Student(userid=user.id, language=configs.LANGUAGE).get_data()
    if len(student) > 0:
        botify.create_student(userid=user.id, name=username)
        utils.CUMessages(userid=user.id, language=configs.LANGUAGE)
        if chat_type != "private":
            student = utils.Student(userid=user.id, language=configs.LANGUAGE).get_data()
            position = utils.StudentPosition(userId=user.id).get_position()
            messages = utils.GetMessages(userid=user.id, language=configs.LANGUAGE).get_data()
            level = student[0]['level']
            rank = student[0]['user_rank']
            point = utils.GetFortuna(user.id, configs.LANGUAGE).get_data()
            data = []
            for x in student:
                res = f"<b>{x['exercise']}</b> - {x['fortunas']}"
                data.append(res)
            fortunas = "\n".join(data)
            act_level =utils.qlevel(level)
            msg = f"Hi {username},\nBelow are your standings on  <b>{botname} </b>\n" \
                  f"<b>Current position:</b> {position}\n<b>Fortunas</b>\n{fortunas}\n<b>Total Points:</b> {point}\n<b>Messages Sent:</b> {messages}\n" \
                  f"<b>Language Level:</b> {act_level}\n<b>Rank:</b> {rank}"
            bot = Bot(token=configs.TOKEN)
            try:
                bot.send_message(chat_id=user.id, text=msg, parse_mode=ParseMode.HTML)
            except Unauthorized:
                update.message.reply_text(f"Please start @{context.bot.username} to use this command")
            else:
                update.message.reply_text("Psss! check your pm")
        else:
            student = utils.Student(userid=user.id, language=configs.LANGUAGE).get_data()
            position = utils.StudentPosition(userId=user.id).get_position()
            messages = utils.GetMessages(userid=user.id, language=configs.LANGUAGE).get_data()
            level = student[0]['level']
            rank = student[0]['user_rank']
            point = utils.GetFortuna(user.id, configs.LANGUAGE).get_data()
            data = []
            for x in student:
                res = f"<b>{x['exercise']}</b> - {x['fortunas']}"
                data.append(res)
            fortunas = "\n".join(data)
            act_level = utils.qlevel(level)
            msg = f"Hi {username},\nBelow are your standings on  <b>{botname} </b>\n" \
                  f"<b>Current position:</b> {position}\n<b>Fortunas</b>\n{fortunas}\n<b>Total Points:</b> {point}\n<b>Messages Sent:</b> {messages}\n" \
                  f"<b>Language Level:</b> {act_level}\n<b>Rank:</b> {rank}"
            bot = Bot(token=configs.TOKEN)
            try:
                bot.send_message(chat_id=user.id, text=msg, parse_mode=ParseMode.HTML)
            except Unauthorized:
                update.message.reply_text(f"Please start @{context.bot.username} to use this command")

    else:
        key_main = [[InlineKeyboardButton(emoji.emojize("Join", use_aliases=True),
                                          url=f"https://t.me/{context.bot.username}?start={user.id}")]]
        main_markup = InlineKeyboardMarkup(key_main)
        bot_text = utils.remove_html_tags(utils.BotMessages(id=22).get_message())
        bot_username = f"@{context.bot.username}"
        update.message.reply_text(emoji.emojize(bot_text.format(bot_username), use_aliases=True),
                                  reply_markup=main_markup)


def topic(update, context):
    user = update.message.from_user
    student = utils.Student(userid=user.id, language=configs.LANGUAGE).get_data()
    if len(student) > 0:
        try:
            group_topic = context.bot_data['topic']
            context.bot.send_message(chat_id=user.id,
                                     text=group_topic,
                                     parse_mode='HTML')
        except KeyError:
            update.message.reply_text(emoji.emojize(f":fire:No topic set at the moment"))
    else:
        key_main = [[InlineKeyboardButton(emoji.emojize("Join", use_aliases=True),
                                          url=f"https://t.me/{context.bot.username}?start={user.id}")]]
        main_markup = InlineKeyboardMarkup(key_main)
        bot_text = utils.remove_html_tags(utils.BotMessages(id=22).get_message())
        bot_username = f"@{context.bot.username}"
        update.message.reply_text(emoji.emojize(bot_text.format(bot_username), use_aliases=True),
                                  reply_markup=main_markup)


def top(update, context):
    user = update.message.from_user

    admins = utils.Admin(userid=user.id, language=configs.LANGUAGE).get_data()
    student = utils.Student(userid=user.id, language=configs.LANGUAGE).get_data()
    if len(student) > 0:
        score1 = utils.topten()[0]
        score2 = utils.topten()[1]
        score3 = utils.topten()[2]
        elem = "\n".join(score1)
        inter = "\n".join(score2)
        advance = "\n".join(score3)

        top10 = f":crown: <b>TOP 10 ELEMENTARY SCOREBOARD</b>:trophy:\n\n{elem}\n\n" \
                f":crown: <b>TOP 10 INTERMEDIATE SCOREBOARD</b> :trophy:\n\n{inter}\n\n" \
                f":crown: <b>TOP 10 ADVANCED SCOREBOARD</b> :trophy:\n\n{advance}\n"
        if admins:
            update.message.reply_text(text=emoji.emojize(top10), parse_mode='HTML')
            # context.bot.send_message(chat_id=user.id, text=emoji.emojize(top10), parse_mode='HTML')
        # else:
        #     update.message.reply_text(text=emoji.emojize(top10), parse_mode='HTML')
    else:
        key_main = [[InlineKeyboardButton(emoji.emojize("Join", use_aliases=True),
                                          url=f"https://t.me/{context.bot.username}?start={user.id}")]]
        main_markup = InlineKeyboardMarkup(key_main)
        bot_text = utils.remove_html_tags(utils.BotMessages(id=22).get_message())
        bot_username = f"@{context.bot.username}"
        update.message.reply_text(emoji.emojize(bot_text.format(bot_username), use_aliases=True),
                                  reply_markup=main_markup)


def next_live(update, context):
    pass


def bonus(update, context):
    user = update.message.from_user
    admins = utils.Admin(userid=user.id, language=configs.LANGUAGE).get_data()
    student = utils.Student(userid=user.id, language=configs.LANGUAGE).get_data()
    if admins:
        command = update.message.text
        if command == '/bonus':
            award_to = update.message.reply_to_message.from_user.id
            award_to_name = update.message.reply_to_message.from_user.username
            answer = emoji.emojize(f":fire:Congratulations @{award_to_name}! Reward comes to those who work hard!",
                                   use_aliases=True)
            utils.AddFortunas(userid=award_to, exercise='Apollo').get_data()
            update.message.reply_text(answer)


def classrooms(update, context):
    user = update.message.from_user
    student = utils.Student(userid=user.id, language=configs.LANGUAGE).get_data()
    if len(student) > 0:
        data = []
        classes = utils.Classrooms().get_data()
        for clas in classes:
            room = f"<b>Classroom</b>: {clas['classroom']}\n<b>Group Link</b>: {clas['groupLink']}"
            data.append(room)
        msg = emoji.emojize(":fire:Here are all classrooms where the Master is present:", use_aliases=True)
        all_rooms = "\n\n".join(data)
        text = f"{msg}\n\n{all_rooms}"
        context.bot.send_message(chat_id=user.id, text=emoji.emojize(text), disable_web_page_preview=True,
                                 parse_mode='HTML')
    else:
        key_main = [[InlineKeyboardButton(emoji.emojize("Join", use_aliases=True),
                                          url=f"https://t.me/{context.bot.username}?start={user.id}")]]
        main_markup = InlineKeyboardMarkup(key_main)
        bot_text = utils.remove_html_tags(utils.BotMessages(id=22).get_message())
        bot_username = f"@{context.bot.username}"
        update.message.reply_text(emoji.emojize(bot_text.format(bot_username), use_aliases=True),
                                  reply_markup=main_markup)


def studyrooms(update, context):
    user = update.message.from_user
    student = utils.Student(userid=user.id, language=configs.LANGUAGE).get_data()
    if len(student) > 0:
        data = []
        classes = utils.Studyrooms().get_data()
        for clas in classes:
            room = f"<b>Study room</b>: {clas['classroom']}\n<b>Group Link</b>: {clas['groupLink']}"
            data.append(room)
        msg = emoji.emojize(":fire:Here are all study rooms of Learning Creators:", use_aliases=True)
        all_rooms = "\n\n".join(data)
        text = f"{msg}\n\n{all_rooms}"
        context.bot.send_message(chat_id=user.id, text=emoji.emojize(text), disable_web_page_preview=True,
                                 parse_mode='HTML')
    else:
        key_main = [[InlineKeyboardButton(emoji.emojize("Join", use_aliases=True),
                                          url=f"https://t.me/{context.bot.username}?start={user.id}")]]
        main_markup = InlineKeyboardMarkup(key_main)
        bot_text = utils.remove_html_tags(utils.BotMessages(id=22).get_message())
        bot_username = f"@{context.bot.username}"
        update.message.reply_text(emoji.emojize(bot_text.format(bot_username), use_aliases=True),
                                  reply_markup=main_markup)


def teachers(update, context):
    data = []
    user = update.message.from_user
    student = utils.Student(userid=user.id, language=configs.LANGUAGE).get_data()
    if len(student) > 0:
        teachers = utils.Teachers().get_data()
        for teacher in teachers:
            username = f'<b>Master</b>: <a href="http://t./me/{teacher["username"]}">{teacher["username"]}</a>'
            data.append(username)
        msg = ":fire:Looking for the followers of Master Ra? Here they are:"
        all_teachers = "\n\n".join(data)
        text = f"{msg}\n\n{all_teachers}"
        context.bot.send_message(chat_id=user.id, text=emoji.emojize(text), disable_web_page_preview=True,
                                 parse_mode='HTML')
    else:
        key_main = [[InlineKeyboardButton(emoji.emojize("Join", use_aliases=True),
                                          url=f"https://t.me/{context.bot.username}?start={user.id}")]]
        main_markup = InlineKeyboardMarkup(key_main)
        bot_text = utils.remove_html_tags(utils.BotMessages(id=22).get_message())
        bot_username = f"@{context.bot.username}"
        update.message.reply_text(emoji.emojize(bot_text.format(bot_username), use_aliases=True),
                                  reply_markup=main_markup)


def rector(update, context):
    msg = emoji.emojize(":fire:Looking for him? His name is @unualibro and He lives in a cave in Romania.",
                        use_aliases=True)
    user = update.message.from_user
    student = utils.Student(userid=user.id, language=configs.LANGUAGE).get_data()
    if len(student) > 0:
        context.bot.send_message(chat_id=user.id, text=msg, disable_web_page_preview=True,
                                 parse_mode='HTML')
    else:
        key_main = [[InlineKeyboardButton(emoji.emojize("Join", use_aliases=True),
                                          url=f"https://t.me/{context.bot.username}?start={user.id}")]]
        main_markup = InlineKeyboardMarkup(key_main)
        bot_text = utils.remove_html_tags(utils.BotMessages(id=22).get_message())
        bot_username = f"@{context.bot.username}"
        update.message.reply_text(emoji.emojize(bot_text.format(bot_username), use_aliases=True),
                                  reply_markup=main_markup)


def settopic(update, context):
    user = update.message.from_user
    chat_type = update.message.chat.type
    admins = utils.Admin(userid=user.id, language=configs.LANGUAGE).get_data()
    user_says = " ".join(context.args)
    text = emoji.emojize(f":fire: <b>Topic Set:</b> {user_says}")
    if admins:
        if chat_type != 'private':
            group_id = update.message.chat.id
            context.bot_data['topic'] = text
            payload = context.bot.send_message(chat_id=group_id, text=text, disable_web_page_preview=True,
                                               parse_mode='HTML')
            message_id = payload.result().message_id
            context.bot.pin_chat_message(chat_id=group_id, message_id=message_id)



def ask_donation(update, context):
    user = update.message.from_user
    print(user)
    chat_type = update.message.chat.type
    admins = utils.Admin(userid=user.id, language=configs.LANGUAGE).get_data()
    text = emoji.emojize(f":sos:To support our teachers, maintain Ra bot ON and keep Learning Creators free for all, we depend on your support. Any donation is highly appreciated. Thank you!",use_aliases=True)
    key_main = [[InlineKeyboardButton(emoji.emojize(":heart:Donate:heart:", use_aliases=True),
                                      url="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WJYMNYLP9TQHL&source=url")]]
    main_markup = InlineKeyboardMarkup(key_main)

    print(admins)
    if admins==True:
        payload = context.bot.send_message(chat_id=configs.GROUPID, text=text, disable_web_page_preview=True,
                                           parse_mode='HTML', reply_markup=main_markup)
        message_id = payload.result().message_id
        context.bot.pin_chat_message(chat_id=configs.GROUPID, message_id=message_id)


def myra(update, context):
    user = update.message.from_user
    student = utils.Student(userid=user.id, language=configs.LANGUAGE).get_data()
    if len(student) > 0:
        context.bot.send_message(chat_id=user.id,
                                 text=emoji.emojize(
                                     ':fire:Log in with this link! <a href="https://fortunaenglish.com">My Ra Profile</a> ',
                                     use_aliases=True), disable_web_page_preview=True, parse_mode='HTML')
    else:
        key_main = [[InlineKeyboardButton(emoji.emojize("Join", use_aliases=True),
                                          url=f"https://t.me/{context.bot.username}?start={user.id}")]]
        main_markup = InlineKeyboardMarkup(key_main)
        bot_text = utils.remove_html_tags(utils.BotMessages(id=22).get_message())
        bot_username = f"@{context.bot.username}"
        update.message.reply_text(emoji.emojize(bot_text.format(bot_username), use_aliases=True),
                                  reply_markup=main_markup)


def profile(update, context):
    user = update.message.from_user
    student = utils.Student(userid=user.id, language=configs.LANGUAGE).get_data()
    chat_type = update.message.chat.type
    if len(student) > 0:
        if chat_type == "private":
            update.message.reply_text(
                "First Name: {}\nUsername: {}\nUser ID: {}\nJoined On: {}".format(user.first_name, utils.get_username(update, context),
                                                                   user.id,student[0]['created_at']))

def dice(update, context):
    user = update.message.from_user

    chat_type = update.message.chat.type
    if chat_type == "private":
        value =update.message.dice['value']
        update.message.reply_text(f"You will get  {value} fortunas if answer the next question correctly!")


def session_manager(update, context):
    user = update.message.from_user
    chat_type = update.message.chat.type
    admin = utils.Admin(userid=user.id, language=configs.LANGUAGE).get_data()
    if chat_type=='private':
        if admin or admin ==False:
            sessions = sql.get_sessions()
            if len(sessions)>0:
                update.message.reply_text("Which Session would you like to stop?")
                for session in sessions:
                    sess_id, sess_name, bot_type = session
                    key_main = [[InlineKeyboardButton(f"❌ Stop", callback_data=f"session+{sess_id}")]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    update.message.reply_text(f"*Session Name:* {sess_name}\n*Exercise:* {bot_type}",
                                              reply_markup=main_markup, parse_mode='markdown')
            else:
                update.message.reply_text("No session available at the moment.")


def solo_learn(update, context):
    data = utils.remove_html_tags(utils.BotMessages(id=28).get_message()).split('.')
    msg =".\n".join(data)
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
    update.message.reply_text(emoji.emojize(msg, use_aliases=True),reply_markup=main_markup, parse_mode='html')