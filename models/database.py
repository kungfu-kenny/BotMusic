import sqlite3
from contextlib import contextmanager

# TODO fix connection absence
CHUNKS_N = 250


@contextmanager
def get_connection():
    try:
        con = sqlite3.connect("tutorial.db")
        yield con
    finally:
        con.close()


def develop_database_basic():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id INT PRIMARY KEY,
                use_songs BOOLEAN DEFAULT True
            );        
            """
        )
        conn.commit()


def insert_user(
    user_id: int,
) -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            f"""
            SELECT id from users where id={user_id};
            """
        )
        ids = cur.fetchall()
        if not ids:
            cur.execute(
                f"""
                INSERT INTO users (id) VALUES ({user_id});
                """
            )
            conn.commit()


def select_album_search(user_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.cursor()
        value_bool = cur.execute(
            f"select use_songs from users where id={user_id}"
        ).fetchone()
        value_bool = value_bool[0] if value_bool else True
    return value_bool


def change_album_search(user_id: int, new_bool: bool) -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"update users set use_songs={new_bool} where id={user_id};")
        conn.commit()
