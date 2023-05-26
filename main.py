import os
from flask import Flask, request
import telebot

app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT'), threaded=False)
bot.set_webhook(url=os.getenv('url'))
state = False


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
    bot.reply_to(message, 'Welcome to the SpotDL Song Downloader Bot!')

# Handler for the '/start' command
@bot.message_handler(commands=['delete'])
def deleteit(message):
    bot.remove_webhook()
    bot.reply_to(message  , "Bot is Free now")
    
# Handler for receiving messages
@bot.message_handler(func=lambda message: True)
def download_song(message):
    # Extract the input from the message
    input_text = message.text.strip()

    # Create the "./spotify" directory if it doesn't exist
    if not os.path.exists('./spotify'):
        os.makedirs('./spotify')

    # Change to the "./spotify" directory
    os.chdir('./spotify')

    # Check if the input is a Spotify link or a song name
    if input_text.startswith('http') and 'spotify.com' in input_text:
        # Input is a Spotify link
        spotify_link = input_text
    else:
        # Input is a song name
        spotify_link = f'\'{input_text}\''

    # Run SpotDL command in the shell to download the song
    command = f'spotdl {spotify_link}'
    
    bot.reply_to(message , "Downloading...")
    result = os.system(command)
    
    if result != 0:
      bot.reply_to(message , "This query yielded no results")

    # Get the list of downloaded song files
    song_files = [f for f in os.listdir('.') if os.path.isfile(f) and os.path.getsize(f) > 10000]

    # Send each song file back to the user
    for song_file in song_files:
        # Send the song file as an audio to the user
        bot.send_audio(message.chat.id, audio=open(song_file, 'rb'))

    # Change back to the previous directory
    os.chdir('..')

    # Delete the entire "./spotify" directory
    os.system('rm -rf ./spotify')

if __name__ == '__main__':
    app.run()
