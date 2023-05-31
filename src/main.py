import os
import time
from flask import Flask, request
import telebot
from helper.log import send_log

app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('spotify_bot'), threaded=False)
admin_user = int(os.getenv('admin'))  
users = [int(id) for id in (os.getenv('users').split(','))]
state = False
last_message_id = None

@app.route('/', methods=['POST'])
def telegram():
    # Process incoming updates from Telegram
    if request.headers.get('content-type') == 'application/json':
        bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
        return 'OK', 200
    
@bot.message_handler(commands=['start', 'on', 'off', 'help'])
def handle_commands(message):
    # Handle /start, /on, and /off commands
    send_log(bot, message)
    global state
    if message.text == '/start':
        bot.reply_to(message, 'Welcome to the Spotify Downloader Bot!\n\nSend me a song name or a Spotify link to download.')
    elif message.text == '/help' :
        bot.reply_to(message, "This bot can download songs from Spotify. Here's how to use it:\n\n1. Send a song name: Just send the name of the song, e.g., 'Luxury'.\n2. Send a Spotify link: Send a link to a specific song, album, or playlist on Spotify.\n\nPlease note that downloading albums and playlists may take longer.")
    elif message.text == '/on':
        state = True
        bot.reply_to(message, "BOT ON")
    elif message.text == '/off':
        state = False
        bot.reply_to(message, "BOT OFF")

@bot.message_handler(func=lambda message: True)
def download_song(message):
    # Handle song download requests
    send_log(bot, message)
    if not state and message.chat.id != admin_user and message.chat.id not in users :
        return
    global last_message_id  
  
    # Check if this is the same message as the previous one  
    if last_message_id == message.message_id:  
         return  
  
    # Store the current message ID as the most recent one  
    last_message_id = message.message_id 
 
    input_text = message.text.strip()

    os.makedirs('./spotify', exist_ok=True)
    os.chdir('./spotify')
    
    spotify_link = input_text if input_text.startswith('http') and 'spotify.com' in input_text else f"'{input_text}'"
    response = 'Downloading Album ...' if 'album' in input_text else 'Downloading Playlist ...' if 'playlist' in input_text else 'Downloading Track ...'
    command = f'spotdl --threads 6 {spotify_link}'

    start_time = time.time()
    wait = bot.reply_to(message, response)
    result = os.system(command)
    end_time = time.time()
    download_time = end_time - start_time
    bot.delete_message(message.chat.id, wait.message_id)

    if result != 0:
        bot.reply_to(message, "There was some error in the Download.")

    song_files = [f for f in os.listdir('.') if os.path.isfile(f) and os.path.getsize(f) > 10000]
    for song_file in song_files:
        bot.send_audio(message.chat.id, audio=open(song_file, 'rb'))

    bot.send_message(message.chat.id, f"Download time: {(int(download_time)) // 60} minutes {(int(download_time)) % 60} seconds")

    os.chdir('..')
    os.system('rm -rf ./spotify')
