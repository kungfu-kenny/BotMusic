import os
from dotenv import load_dotenv

load_dotenv()
######################BLOCK TELEGRAM BASIC#################################

bot_key = os.getenv('BOT_KEY')
chat_id_default = os.getenv('CHAT_ID_DEFAULT')
#######################BLOCK TELEGRAM ROUTES###############################

telegram_start = 'start'
######################BLOCK FOLDERS########################################

folder_db = "db"
folder_storage = "storage"
folder_defaults = "defaults"
folder_telegram = "telegram"
folder_current = os.getcwd()
######################CRED DATABASE########################################

db_file = "local.db"
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_base = os.getenv("DB_BASE")
db_pass = os.getenv("DB_PASSWORD")
######################CSV PARAMS###########################################

csv_basic = "Basic.csv"
csv_year = "Year.csv"
csv_edges = "Edges.csv"
csv_genre = "Genre.csv"
csv_albums = "Albums.csv"
csv_artist = "Artist.csv"
csv_subgenre = "Subgenre.csv"
csv_basic_song = "Basic_Song.csv"
csv_basic_label = "Basic_Label.csv"
csv_basic_genre = "Basic_Genre.csv"
csv_basic_song_fail = "Basic_Song_Failed.csv"
csv_basic_song_apple = "Basic_Song_Apple.csv"
csv_basic_song_deezer = "Basic_Song_Deezer.csv"
csv_basic_song_genius = "Basic_Song_Genius.csv"
csv_basic_song_deezer_select = "Basic_Song_Deezer_Selection.csv"
######################NAME DATABASE########################################

table_user = 'user'
table_song = 'song'
table_label = 'label'
table_album = 'album'
table_genre = 'genre'
table_artist = 'artist'
table_song_year = 'song_year'
table_song_genre = 'song_genre'
table_song_label = 'song_label'
table_album_song = 'album_song'
table_album_year = 'album_year'
table_album_label = 'album_label'
table_album_genre = 'album_genre'
table_artist_song = 'artist_song'
table_genre_label = 'genre_label'
table_artist_genre = 'artist_genre'
table_artist_label = 'artist_label'
table_artist_album = 'artist_album'
table_song_youtube = 'song_youtube'
table_user_history_song = 'user_history_song'
table_user_history_album = 'user_history_album'
table_user_favourite_song = 'user_favourite_song'
table_user_favourite_album = 'user_favourite_album'
#######################PARSE GENIUS########################################

genius_semaphore_threads = 10
link_genius = "https://genius.com"
link_genius_albums = "albums"
link_genius_search_begin = "/search?q="
link_genius_search_end= "%20"
#######################PARSE APPLE MUSIC###################################

apple_music_semaphore_threads = 10
link_apple_music = 'https://music.apple.com'
link_apple_music_us = 'us'
link_apple_music_space = '%20'
link_apple_music_search = 'search?term='
#######################PARSE DEEZER########################################

deezer_semaphore_threads = 10
link_deezer = 'https://www.deezer.com'
link_deezer_us = 'us'
link_deezer_album = 'album'
link_deezer_search = 'search'
link_deezer_space = '%20'
link_deezer_dollar = '%24'