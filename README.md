# Telegram-Movie-Bot

# Description:

The Movie Bot is a Telegram bot that provides information about movies based on genres. Users can interact with the bot to explore different movie genres and get details about movies within a selected genre. The bot uses the Telegram API for communication and The Movie Database (TMDb) API to fetch movie information.

# Features:

Explore and select movie genres.
Get details about movies in the selected genre, including title, overview, release date, and poster.
Prerequisites:

Python 3.x
Required Python packages: telegram, requests, python-dotenv

# Setup:

1. Clone the repository:
   git clone <repository_url>
   cd <repository_directory>
   
2. Install the required packages:
   pip install -r requirements.txt
   
3. Create an .env file in the repository directory with the following content:
   TELEGRAM_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
   AUTHORIZATION=YOUR_TMDB_API_KEY
# Usage:
1. Start the bot by running:
   python main.py
   
2. Open your Telegram app and search for your bot. Send the command /start to begin.

3. Use the /show_genres command to see available movie genres.

4. Use the /select command to choose a movie genre. Enter the genre name when prompted.

5. The bot will display movie information including title, overview, release date, and poster for each movie in the selected genre.

# Important Notes:

The bot requires a valid Telegram bot token (TELEGRAM_TOKEN) and The Movie Database (TMDb) API key (AUTHORIZATION) for authentication.
  



