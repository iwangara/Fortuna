import requests

import utils
from functools import wraps
import logging

logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')
c_handler.setLevel(logging.ERROR)
f_handler.setLevel(logging.WARNING)
# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)
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
        seshat = sql.get_seshat_bot(message_id)
        tyche = sql.get_tyche_bot(message_id)
        leizi = sql.get_leizi_bot(message_id)
        odin = sql.get_odin_bot(message_id)
        zamo = sql.get_zamo_bot(message_id)
    except:
        pass
    if apollo != False:
        qstn_type = apollo
        return qstn_type
    elif seshat != False:
        qstn_type = seshat
        return qstn_type
    elif tyche != False:
        qstn_type = tyche
        return qstn_type
    elif leizi != False:
        qstn_type = leizi
        return qstn_type
    elif odin != False:
        qstn_type = odin
        return qstn_type
    elif zamo != False:
        qstn_type = zamo
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
            return f"@{user.username}"
    except AttributeError:
        query = update.callback_query
        usern = query.from_user
        if usern.username == None:
            return usern.first_name
        else:
            return f"@{usern.username}"


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def mr_logger(message):
    return logger.warning(message)


def zamol_download(url):
    filename = 'question.mp3'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
        return filename

    else:
        print("Unable to download image")


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu
