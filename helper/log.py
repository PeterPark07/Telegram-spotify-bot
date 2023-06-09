import os
from telegraph import Telegraph

telegraph = Telegraph(os.getenv('telegraph_token'))
path = os.getenv('telegraph_path')
admin_user = int(os.getenv('admin'))
users = [int(user_id) for user_id in os.getenv('users').split(',')]

def logg(new_content):
    page = telegraph.get_page(path=path,return_content=True,return_html=True)
    title, content = page['title'], page['content']
    content = new_content + content
    telegraph.edit_page(path=path,title=title,html_content=content,author_name='bots')
    return


def log(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_text = message.text
    name = message.from_user.username or message.from_user.first_name

    # Determine the information to display based on user and chat IDs
    if user_id == admin_user:
        log_info = "⭐️ ADMIN ⭐️  "
    elif user_id in users:
        log_info = f"🔹 User: {name} (USER)  User ID: {user_id}  "
    elif user_id == chat_id:
        log_info = f"🔸 User: {name}   Chat ID: {chat_id}  "
    else:
        log_info = f"🔸 User: {name}   User ID: {user_id}  Chat ID: {chat_id}  "

    # Construct the log message with relevant details
    log_message = f"🤖 Bot: @AnotherSpotify_bot  {log_info}Message: {message_text}"
    log_message = f"<p>{log_message}</p>"
    logg(log_message)