import requests
from telegram import *
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
from dotenv import load_dotenv
from os import getenv

load_dotenv("envs")
TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
AUTHORIZATION= getenv("AUTHORIZATION")


headers = {
    "accept": "application/json",
    "Authorization": f"{AUTHORIZATION}"
}


def get_genres_names():
    genres = requests.get(url="https://api.themoviedb.org/3/genre/movie/list?language=en", headers=headers).json()["genres"]
    genres = [genre['name'] for genre in genres]

    return genres


def select_genre_name(choice):
    for name in get_genres_names():
        if choice == name:
            genres = requests.get(url="https://api.themoviedb.org/3/genre/movie/list?language=en", headers=headers).json()[
                "genres"]
            for genre in genres:
                if genre['name'] == choice:
                    return genre["id"]


def get_movies(movie_name):
    genre_id = movie_name
    movies = requests.get(url="https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc", headers=headers).json()['results']
    movie_info = []
    # movie_titles = [movie['title'] for movie in movies if genre_id in movie['genre_ids']]
    for movie in movies:
        if genre_id in movie['genre_ids']:
            movie_info.append({'title': movie['title'],
                          'overview': movie['overview'],
                          'release_date': movie['release_date'],
                          'poster_path': f"https://image.tmdb.org/t/p/w1280{movie['poster_path']}"
                          })
    return movie_info




#creating objects to perform a task
updater = Updater(TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher


# Conversation states
GENRE_SELECTION, SHOW_GENRES = range(2)


def start(update, context):
    update.message.reply_text("Hello! Welcome to the Movie Bot. Type /show_genres to see all genres,"
                              " /select to choose the genre.")
    return SHOW_GENRES


def handle_genre_selection(update, context):
    update.message.reply_text("Please enter the genre you want to explore:")
    return GENRE_SELECTION


def handle_genre_input(update, context):
    user_input = update.message.text
    movie_genre = select_genre_name(user_input)
    if movie_genre is None:
        update.message.reply_text("Invalid genre name. Please try again or type /show_genres to see all genres")
        return GENRE_SELECTION

    movies = get_movies(movie_genre)

    # Send movie information and poster for each movie
    #movie_list_message = "Available movies:\n\n"
    for movie in movies:
        movie_list_message = f"Title: {movie['title']}\n"
        movie_list_message += f"Overview: {movie['overview']}\n"
        movie_list_message += f"Release date: {movie['release_date']}\n\n"
        movie_list_message += f"Poster: {movie['poster_path']}\n\n\n"

        if movie_list_message:
            update.message.reply_text(movie_list_message, reply_markup=ReplyKeyboardRemove())
        else:
            update.message.reply_text("No movies found", reply_markup=ReplyKeyboardRemove())

    return SHOW_GENRES


def handle_showing_genres(update, context):
    genres = "\n".join(get_genres_names())
    update.message.reply_text(f"Available genres:\n\n{genres}", reply_markup=ReplyKeyboardRemove())

    return SHOW_GENRES


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Create a conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SHOW_GENRES: [
                CommandHandler('show_genres', handle_showing_genres),
                CommandHandler('select', handle_genre_selection),
            ],
            GENRE_SELECTION: [MessageHandler(Filters.text & ~Filters.command, handle_genre_input)]
        },
        fallbacks=[]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()