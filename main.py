import os
from flask import Flask, request
import time
import telebot
from helper.log import send_log

app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT'), threaded=False)
admin_user = int(os.getenv('admin'))
state = False
last_message_id = None

@app.route('/', methods=['POST'])
def telegram():
    # Process incoming updates
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200

# Handler for the '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    send_log(bot, message)
    bot.reply_to(message, 'Welcome to the Spotify Downloader Bot!\n\nSend me a song name or a Spotify link to download.')

@bot.message_handler(commands=['on'])
def handle_on(message):
    send_log(bot, message)
    global state
    state = True
    # Handle the /on command
    bot.reply_to(message, "BOT ON")

@bot.message_handler(commands=['off'])
def handle_off(message):
    global state
    state = False
    # Handle the /off command
    bot.reply_to(message, "BOT OFF")

# Handler for receiving messages
@bot.message_handler(func=lambda message: True)
def download_song(message):
    send_log(bot, message)
    if not state and message.chat.id != admin_user :
        return

    global last_message_id

    # Check if this is the same message as the previous one
    if last_message_id == message.message_id:
        return

    # Store the current message ID as the most recent one
    last_message_id = message.message_id

    # Extract the input from the message
    input_text = message.text.strip()

    # Create the "./spotify" directory if it doesn't exist
    if not os.path.exists('./spotify'):
        os.makedirs('./spotify')
    os.chdir('./spotify')

    # Check if the input is a Spotify link or a song name
    if input_text.startswith('http') and 'spotify.com' in input_text:
        # Input is a Spotify link
        spotify_link = input_text
        if 'album' in input_text:
            response = 'Downloading Album ...'
        elif 'playlist' in input_text:
            response = 'Downloading Playlist ...'
        else :
            response = 'Downloading Track ...'
            
    else:
        # Input is a song name
        spotify_link = f'\'{input_text}\''
        response = 'Downloading Track ...'

    # Run SpotDL command in the shell to download the song
    command = f'spotdl --threads 6 {spotify_link}'
    
    start_time = time.time()  # Record the start time
    
    
    
    wait = bot.reply_to(message, response)
    result = os.system(command)
    
    end_time = time.time()  # Record the end time
    download_time = end_time - start_time  # Calculate the download time
    bot.delete_message(message.chat.id, wait.message_id)

    if result != 0:
        bot.reply_to(message, "There was some error in the Download.")

    # Get the list of downloaded song files
    song_files = [f for f in os.listdir('.') if os.path.isfile(f) and os.path.getsize(f) > 10000]

    # Send each song file back to the user
    for song_file in song_files:
        # Send the song file as an audio to the user
        bot.send_audio(message.chat.id, audio=open(song_file, 'rb'))
        
    # Send the download time to the user
    bot.send_message(message.chat.id, f"Download time: {(int(download_time))//60} minutes {(int(download_time))%60} seconds")

    # Change back to the previous directory
    os.chdir('..')

    # Delete the entire "./spotify" directory
    os.system('rm -rf ./spotify')

if __name__ == '__main__':
    app.run()
