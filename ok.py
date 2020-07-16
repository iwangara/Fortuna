import datetime

import pytz

import utils

# sql= utils.DBHelper().setup()
stringg = utils.remove_html_tags(utils.BotMessages(id=28).get_message()).split('.')
print(".\n".join(stringg))


