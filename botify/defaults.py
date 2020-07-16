import logging


import configs
import utils
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

f_handler = logging.FileHandler('file.log')
f_handler.setLevel(logging.WARNING)
logger.addHandler(f_handler)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def create_student(userid,name):
    language= configs.LANGUAGE
    exercises=configs.EXERCISES
    for exercise in exercises:
        utils.CreateStudent(userid,language,exercise,name)

def unauth_group(update, context):
    print(update)
    user = update.message.from_user
    chat_type = update.message.chat.type
    if (chat_type == "group" or chat_type == "supergroup"):

        group_id = update.message.chat.id
        user_id = user.id

        group_title = update.message.chat.title
        for i in update.message.new_chat_members:
            if i.username == configs.BOTUSERNAME:
                if user_id not in configs.ADMINS:
                    try:
                        context.bot.send_message(chat_id=group_id,
                                                 text="Join @learningcreators now!!!. Don’t you see it is boring here? I am leaving already.")
                    except:
                        pass

                    context.bot.leave_chat(chat_id=group_id)
                    try:
                        for admin in configs.ADMINS:
                            context.bot.send_message(chat_id=admin,
                                             text=f"@{utils.get_username(update, context)} tried to add me to {group_title} but I left ASAP.")
                    except:
                        pass





