from telegram import ParseMode, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import Unauthorized
import utils
import configs
import botify
import emoji

sql=utils.DBHelper()
#check if the user started the bot
def check_progress(update,context):
    group_title = update.message.chat.title
    chat_type = update.message.chat.type
    username=utils.get_username(update, context)
    user = update.message.from_user
    botify.create_student(userid=user.id, name=username)
    utils.CUMessages(userid=user.id, language=configs.LANGUAGE)
    if chat_type != "private":

        student=utils.Student(userid=user.id,language=configs.LANGUAGE).get_data()
        position = utils.StudentPosition(userId=user.id).get_position()
        messages = utils.GetMessages(userid=user.id, language=configs.LANGUAGE).get_data()
        level = student[0]['level']
        rank =student[0]['user_rank']
        point = utils.GetFortuna(user.id, configs.LANGUAGE).get_data()
        data = []
        for x in student:
            res = f"<b>{x['exercise']}</b> - {x['fortunas']}"
            data.append(res)
        fortunas = "\n".join(data)
        msg = f"Hi {username},\nBelow are your standings in the <b>{group_title} Group</b>\n" \
              f"<b>Current position:</b> {position}\n<b>Fortunas</b>\n{fortunas}\n<b>Total Points:</b> {point}\n<b>Messages Sent:</b> {messages}\n" \
              f"<b>Language Level:</b> {level}\n<b>Rank:</b> {rank}"
        bot =Bot(token=configs.TOKEN)
        try:
            bot.send_message(chat_id=user.id, text=msg, parse_mode=ParseMode.HTML)
        except Unauthorized:
            update.message.reply_text(f"Please start @{context.bot.username} to use this command")
        else:
            update.message.reply_text("Psss! check your pm")
    else:
        update.message.reply_text(f"Hi {username}, please send this command inside an LC group")

# save only messages from non admins
def message_counter(update,context):
    user = update.message.from_user
    username=utils.get_username(update,context)
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

    totalpts =utils.GetFortuna(userid=user.id,language=configs.LANGUAGE).get_data()
    if admin == False and chat_type != 'private':
        student =utils.Student(userid=user.id,language=configs.LANGUAGE).get_data()
        if len(student)>0:
            # save or create use in the message table
            utils.CUMessages(userid=user.id, language=configs.LANGUAGE).get_data()
            # now get the messages
            user_messages = utils.GetMessages(userid=user.id, language=configs.LANGUAGE).get_data()

            if (studentmsg <= user_messages < apprenticemsg) and (studentpts <= totalpts < apprenticepts):
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
            elif (apprenticemsg <= user_messages < followermsg) and (apprenticepts <= totalpts < followerpts):
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
            elif (followermsg <= user_messages < instructormsg) and (followerpts <= totalpts < instructorpts):
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
            elif (instructormsg <= user_messages < mentormsg) and (instructorpts <= totalpts < mentorpts):
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
            elif (mentormsg <= user_messages < teachermsg) and (mentorpts <= totalpts < teacherpts):
                rank = 'Mentor'
                if sql.check_notice(userid=user.id, rank=rank) == False:
                    # # change user level
                    utils.UpdateLevel(userid=user.id,language=configs.LANGUAGE)
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
            elif (teachermsg <= user_messages < scholarmsg) and (teacherpts <= totalpts < scholarpts):
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
            elif (scholarmsg <= user_messages < mastermsg) and (scholarpts <= totalpts < masterpts):
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
            elif (mastermsg <= user_messages < eminencemsg) and (masterpts <= totalpts < eminencepts):
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
            elif (eminencemsg <= user_messages < gurumsg) and (eminencepts <= totalpts < gurupts):
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
            elif (gurumsg <= user_messages < titanmsg) and (gurupts >= totalpts < titanpts):
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
            elif (user_messages >= titanmsg) and (totalpts >= titanpts):
                print('titan')
                rank = 'Titan'
                if sql.check_notice(userid=user.id, rank=rank) == False:
                    # # change user level
                    utils.UpdateLevel(userid=user.id,language=configs.LANGUAGE)
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
            bot_text = utils.remove_html_tags(utils.BotMessages(id=22).get_message())
            bot_username =f"@{context.bot.username}"
            update.message.reply_text(emoji.emojize(bot_text.format(bot_username),use_aliases=True))









def start(update,context):
    user = update.message.from_user
    admin = utils.Admin(userid=user.id, language=configs.LANGUAGE).get_data()
    chat_type = update.message.chat.type
    if chat_type=='private':
        if admin==False:
            utils.CUMessages(userid=user.id, language=configs.LANGUAGE).get_data()
            botify.create_student(userid=user.id,name=utils.get_username(update,context))
            bot_text=utils.remove_html_tags(utils.BotMessages(id=18).get_message())
            context.bot.send_message(chat_id=user.id,text=emoji.emojize(bot_text,use_aliases=True))
        else:
            update.message.reply_text("Hi Admin, you need to use the portal nowadays.")
