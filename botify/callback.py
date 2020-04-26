import emoji
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import utils
sql =utils.DBHelper()
def javis(update,context):
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