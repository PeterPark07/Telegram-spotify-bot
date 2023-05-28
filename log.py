import time

def send_log(message, log_chat_id):

    name = message.from_user.username or message.from_user.first_name
    chat_id = message.chat.id
    message_text = message.text

    log_message = f"Bot: @{bot.get_me().username}\n" \
                  f"Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n" \
                  f"User: {name}\n" \
                  f"Chat ID: {chat_id}\n" \
                  f"Message: {message_text}"

    bot.send_message(log_chat_id, log_message)
