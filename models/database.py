import sqlite3
from contextlib import contextmanager

#TODO fix connection absence
CHUNKS_N = 250

@contextmanager
def get_connection():
    try:
        con = sqlite3.connect("tutorial.db")
    finally:
        con.close()

def make_list_chunk(value_list:list, n:int=CHUNKS_N) -> list:
    def divide_chunks(l, n):    
        for i in range(0, len(l), n): 
            yield l[i:i + n]
    return list(divide_chunks(value_list, n))

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

def select_song(song_dict:dict, conn=None) -> list:
    with get_connection() as conn:
        cur = conn.cursor()
        usage = cur.execute(
            f"SELECT * FROM songs WHERE id={song_dict['song_id']};"
        ).fetchone()
    return usage if usage else []

def select_songs(song_list:list, conn=None) -> list:
    if len(song_list) > CHUNKS_N:
            song_list = make_list_chunk(song_list)
    else:
        song_list = [song_list]
    with get_connection() as conn:
        cur = conn.cursor()
        usage = []
        for song_chunk in song_list:
            if (
                new:=cur.execute(
                    f"""
                    SELECT * FROM songs WHERE id IN(
                        {','.join(i['song_id'] for i in song_chunk)}
                    );
                    """
                ).fetchall()
            ):
                usage.append(new)
    return usage

def insert_song_album(song_list:list, conn=None) -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        for song_dict in song_list:
            cur.execute(
                f"""
                INSERT INTO albums_songs(id_album, id_song)
                VALUES ({song_dict['album_id']}, {song_dict['song_id']})
                WHERE NOT EXIST (
                    SELECT * FROM albums_songs
                    WHERE id_album = {song_dict['album_id']} AND id_song = {song_dict['song_id']}
                );
                """
            )
        conn.commit()

def insert_album(album_list:dict, conn=None) -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        for album_dict in album_list:
            cur.execute(
                f"""
                INSERT INTO albums(id, name)
                """
            )
        conn.commit()
def insert_song(song_list:list, conn=None) -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        # cur.execute(
        #     f"""
        #     INSERT INTO songs 
        #     """
        # )
        # conn.commit()

def insert_songs(song_dict:dict, conn=None) -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        # cur.execute(
        #     f"""
            
        #     """
        # )
        # conn.commit()
