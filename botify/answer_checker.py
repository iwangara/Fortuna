from telegram import ChatAction
import configs
import utils
import botify
sql =utils.DBHelper()

send_typing_action = utils.send_action(ChatAction.TYPING)

@send_typing_action
def reply_check(update,context):
    bot_username = update.message.reply_to_message.from_user.username

    user = update.message.from_user
    username =utils.get_username(update,context)
    user_answer = update.message.text
    group_id = update.message.chat.id
    chat_type = update.message.chat.type
    #check if the user is replying in the group and to the bot's message
    if chat_type != "private" and bot_username == configs.BOTUSERNAME:
        # chat message id
        message_id = update.message.reply_to_message.message_id
        #question type(apollo,gaia,etc)
        bot_type = utils.bot_type(message_id=message_id)
        botify.logger.warning(f'bot type: {bot_type}')
        if bot_type=='Apollo':
            """register/confirm the db under the question and language"""
            res =utils.CreateStudent(userid=user.id, language=configs.LANGUAGE, exercise=bot_type,name=username).get_data()
            botify.logger.warning(f'creating student api called : {res}')
            """Check how many chances a user has got remaining,1 chance per user per question"""
            tries =sql.check_try(userId=user.id,messageId=message_id,bot=bot_type)
            if tries!=True:
                """mark the user as tried the question"""
                sql.create_chance(userId=user.id,messageId=message_id,bot=bot_type)
                """Check user level"""
                student =utils.GetStudent(userid=user.id,language=configs.LANGUAGE,exercise=bot_type).get_data()
                student_level=student['level']
                qlevel=sql.get_apollo_level_by_msgId(msgId=message_id)
                que_level =utils.levelq(qlevel)
                botify.logger.warning(f'question level : {que_level}')

                if int(que_level)>=int(student_level):
                    """Check user answer"""
                    answer = sql.get_apollo_answer_by_msgId(msgId=message_id)
                    if utils.stripper(text=user_answer)==utils.stripper(text=answer):
                        """add user's fortuna in this language and exercise"""
                        utils.AddFortunas(userid=user.id, language=configs.LANGUAGE, exercise=bot_type).get_data()
                        """increase count of users who tried this question"""
                        sql.update_correct(messageId=message_id)





@send_typing_action
def gid(update,context):
    user = update.message.from_user
    chat_type = update.message.chat.type

    if chat_type == "private":
        update.message.reply_text(
            "First Name: {}\nUsername: {}\nUser ID:{}".format(user.first_name, user.username, user.id))
    else:
        update.message.reply_text("Group ID is : {}".format(update.message.chat.id))



