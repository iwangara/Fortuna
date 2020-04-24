import utils
import configs

# save only messages from non admins
def save_messages(update,context):
    user = update.message.from_user
    admin =utils.Admin(userid=user.id,language=configs.LANGUAGE).get_data()
    if admin==False:
        utils.CUMessages(userid=user.id, language=configs.LANGUAGE).get_data()



def check_progress(update,context):
    pass
