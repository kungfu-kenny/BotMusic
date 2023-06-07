import sqlite3
from contextlib import contextmanager


@contextmanager
def get_connection():
    try:
        con = sqlite3.connect("tutorial.db")
    finally:
        con.close()

def develop_database_basic():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS db_music;")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXIST users(
                id INT PRIMARY KEY,
                username VARCHAR(100),
                name_first VARCHAR(100),
                name_last VARCHAR(100),
                use_albums BOOLEAN DEFAULT True
            );        
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS albums(
                id INT PRIMARY KEY,
                name TEXT,    
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS songs(
                id INT PRIMARY KEY,
                name TEXT,
                duration INT,
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS artists(
                id INT PRIMARY KEY,
                name TEXT,
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS albums_artists(
                id_album INT FOREIGN KEY REFERENCES albums(id),
                id_artist INT FOREIGN KEY REFERENCES artists(id),
                PRIMARY KEY (id_album, id_artist) 
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS albums_songs(
                id_album INT FOREIGN KEY REFERENCES albums(id),
                id_song INT FOREIGN KEY REFERENCES songs(id),
                PRIMARY KEY (id_album, id_song)
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS artists_songs(
                id_artist INT FOREIGN KEY REFERENCES artists(id),
                id_song INT FOREIGN KEY REFERENCES songs(id),
                PRIMARY KEY (id_artist, id_song)
            );
            """
        )
        #TODO think about that
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS albums_users(
                id_album INT FOREIGN KEY REFERENCES albums(id),
                id_user INT FOREIGN KEY REFERENCES users(id),
                PRIMARY KEY (id_album, id_user)
            );
            """
        )
        conn.commit()

def select_songs() -> None:
    pass

def insert_songs() -> None:
    pass

