def generated_user_email(username, chat_id):
    if username is None:
        username = "user"
    return username + "_" + str(chat_id) + "@templinkshare.bot"
