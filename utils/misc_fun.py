import utils
from functools import wraps

sql = utils.DBHelper()


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context, *args, **kwargs)

        return command_func

    return decorator


# delete spaces on texts
def stripper(text):
    string = text.replace("  ", " ").strip()
    return string


def bot_type(message_id):
    try:
        apollo = sql.get_apollo_bot(message_id)
    except:
        pass
    if apollo != False:
        qstn_type = apollo
        return qstn_type


def qlevel(text):
    if text == 1:
        level = 'Elementary'
        return level
    elif text == 2:
        level = 'intermediate'
        return level
    elif text == 3:
        level = 'advanced'
        return level


def levelq(text):
    textx = text.lower()
    if textx == 'elementary':
        level = 1
        return level
    elif textx == 'intermediate':
        level = 2
        return level
    elif textx == 'advanced':
        level = 3
        return level

def get_username(update, context):
    try:
        user = update.message.from_user
        if user.username == None:
            return user.first_name
        else:
            return user.username
    except AttributeError:
        query = update.callback_query
        usern = query.from_user
        if usern.username == None:
            return usern.first_name
        else:
            return usern.username
