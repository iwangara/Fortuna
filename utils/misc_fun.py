import os

import requests

import utils
from functools import wraps
import logging
import speech_recognition as sr
import subprocess
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
    string =string.rstrip(".")
    string = string.lower()
    return string


def bot_type(message_id):
    try:
        apollo = sql.get_apollo_bot(message_id)
        seshat = sql.get_seshat_bot(message_id)
        tyche = sql.get_tyche_bot(message_id)
        leizi = sql.get_leizi_bot(message_id)
        odin = sql.get_odin_bot(message_id)
        zamo = sql.get_zamo_bot(message_id)
        nuwa = sql.get_nuwa_bot(message_id)
        gaia = sql.get_gaia_bot(message_id)
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
    elif nuwa != False:
        qstn_type = nuwa
        return qstn_type
    elif gaia != False:
        qstn_type = gaia
        return qstn_type


def bot_poll_type(poll_id):
    try:
        wala = sql.get_wala_bot(poll_id)
        africa = sql.get_africa_bot(poll_id)
        kadlu =sql.get_kadlu_bot(poll_id)
    except:
        pass
    if wala != False:
        qstn_type = wala
        return qstn_type
    elif africa != False:
        qstn_type = africa
        return qstn_type
    elif kadlu != False:
        qstn_type = kadlu
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




def convert_ogg_to_wav(ogg_file, wav_file):
    """
    :return: convert ogg file to wav file
    """
    src_filename = ogg_file
    dest_filename = wav_file
    exists = os.path.isfile(wav_file)
    if exists:
        os.remove(wav_file)

    process = subprocess.run(['ffmpeg', '-i', src_filename, dest_filename])
    print(process)
    if process.returncode != 0:
        raise Exception("Something went wrong")
    return dest_filename

def clear_gaia(user_id):
    try:
        os.remove("gaia_{}.wav".format(user_id))
        os.remove("gaia_{}.ogg".format(user_id))
    except:
        pass
    return True


def clear_nuwa(user_id):
    try:
        os.remove("nuwa_{}.wav".format(user_id))
        os.remove("nuwa_{}.ogg".format(user_id))
    except:
        pass
    return True

def language_select(language):
    if language == "English":
        return "en-GB"
    elif language == "French":
        return "fr-FR"
    elif language == "Spanish":
        return "es-ES"
    elif language == "Arabic":
        return "ar-AE"
    elif language == "German":
        return "de-DE"
    elif language == "Italian":
        return "it-IT"
    elif language == "Portuguese":
        return "pt-PT"
    elif language == "Polish":
        return "pl-PL"
    elif language == "Romanian":
        return "ro-RO"
    elif language == "Bahasa":
        return "id-ID"
    elif language == "Russian":
        return "ru-RU"
    elif language == "Turkish":
        return "tr-TR"
    elif language == "Korean":
        return "ko-KR"
    elif language == "Hebrew":
        return "he-IL"
    elif language == "Azerbaijani":
        return "az-AZ"
    elif language == "Swahili":
        return "sw-KE"
    elif language == "Swedish":
        return "sv-SE"
    elif language == "Amharic":
        return "am-ET"
    elif language == "Chinese":
        return "zh-HK"
    elif language == "Hindi":
        return "hi-IN"
    elif language == "Ukrainian":
        return "uk-UA"
    elif language == "Malay":
        return "ms-MY"
    elif language == "Persian":
        return "fa-IR"
    elif language == "Greek":
        return "el-GR"



class Speech():

    def __init__(self, file = ""):
        self.r = sr.Recognizer()
        self._file = file

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        self._file = value


    def to_text(self,lang):
        try:
            harvard = sr.AudioFile(self._file)
            # print(self.file + "******" * 100)
            with harvard as source:
                audio = self.r.record(source)
                # print(audio)
            return self.r.recognize_google(audio, language=lang)
        except sr.WaitTimeoutError:
            return 500
        except sr.UnknownValueError:
            return 401