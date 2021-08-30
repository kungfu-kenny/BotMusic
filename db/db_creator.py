import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine,
                        Table,
                        Column,
                        Integer,
                        String,
                        ForeignKey)
from sqlalchemy.orm.session import Session
from config import (db_file,
                    db_host,
                    db_name,
                    db_pass,
                    db_base,                    
                    table_user,# = 'user'
                    table_song,# = 'song'
                    table_label,# = 'label'
                    table_album,# = 'album'
                    table_genre,# = 'genre'
                    table_artist,# = 'artist'
                    table_song_year,# = 'song_year'
                    table_song_genre,# = 'song_genre'
                    table_song_label,# = 'song_label'
                    table_album_song,# = 'album_song'
                    table_album_year,# = 'album_year'
                    table_album_label,# = 'album_label'
                    table_album_genre,# = 'album_genre'
                    table_artist_song,# = 'artist_song'
                    table_genre_label,# = 'genre_label'
                    table_artist_genre,# = 'artist_genre'
                    table_artist_label,# = 'artist_label'
                    table_artist_album,# = 'artist_album'
                    table_song_youtube,# = 'song_youtube'
                    table_user_history_song,# = 'user_history_song'
                    table_user_history_album,# = 'user_history_album'
                    table_user_favourite_song,# = 'user_favourite_song'
                    table_user_favourite_album,# = 'user_favourite_album'
                    folder_storage,
                    folder_current)


Base = declarative_base()


association_table_song_year = Table(table_song_year, Base.metadata,
    Column('id_song', ForeignKey(f'{table_song}.id')),
    Column('year', String(10))
)

association_table_song_genre = Table(table_song_genre, Base.metadata,
    Column('id_song', ForeignKey(f'{table_song}.id')),
    Column('id_genre', ForeignKey(f'{table_genre}.id'))
)

association_table_song_label = Table(table_song_label, Base.metadata,
    Column('id_song', ForeignKey(f'{table_song}.id')),
    Column('id_label', ForeignKey(f'{table_label}.id'))
)

association_table_album_song = Table(table_album_song, Base.metadata,
    Column('id_song', ForeignKey(f'{table_song}.id')),
    Column('id_album', ForeignKey(f'{table_album}.id'))
)

association_table_album_year = Table(table_album_year, Base.metadata,
    Column('id_album', ForeignKey(f'{table_album}.id')), 
    Column('year', String(10))
)

association_table_album_label = Table(table_album_label, Base.metadata,
    Column('id_album', ForeignKey(f'{table_album}.id')),
    Column('id_label', ForeignKey(f'{table_label}.id'))
)

association_table_album_genre = Table(table_album_genre, Base.metadata,
    Column('id_album', ForeignKey(f'{table_album}.id')),
    Column('id_genre', ForeignKey(f'{table_genre}.id'))
)

association_table_artist_song = Table(table_artist_song, Base.metadata,
    Column('id_song', ForeignKey(f'{table_song}.id')),
    Column('id_artist', ForeignKey(f'{table_artist}.id'))
)

association_table_genre_label = Table(table_genre_label, Base.metadata,
    Column('id_genre', ForeignKey(f'{table_genre}.id')),
    Column('id_label', ForeignKey(f'{table_label}.id'))
)

association_table_artist_genre = Table(table_artist_genre, Base.metadata,
    Column('id_artist', ForeignKey(f'{table_artist}.id')),
    Column('id_genre', ForeignKey(f'{table_genre}.id'))
)

association_table_artist_label = Table(table_artist_label, Base.metadata,
    Column('id_artist', ForeignKey(f'{table_artist}.id')),
    Column('id_label', ForeignKey(f'{table_label}.id'))
)

association_table_artist_album = Table(table_artist_album, Base.metadata,
    Column('id_artist', ForeignKey(f'{table_artist}.id')),
    Column('id_album', ForeignKey(f'{table_album}.id'))
)

association_table_song_youtube = Table(table_song_youtube, Base.metadata,
    Column('id_song', ForeignKey(f'{table_song}.id')),
    Column('link', String(200))
)

association_table_user_history_song = Table(table_user_history_song, Base.metadata,
    Column('id_song', ForeignKey(f'{table_song}.id')),
    Column('id_user', ForeignKey(f'{table_user}.id'))
)

association_table_user_history_album = Table(table_user_history_album, Base.metadata,
    Column('id_album', ForeignKey(f'{table_album}.id')),
    Column('id_user', ForeignKey(f'{table_user}.id'))
)

association_table_user_favourite_song = Table(table_user_favourite_song, Base.metadata,
    Column('id_song', ForeignKey(f'{table_song}.id')),
    Column('id_user', ForeignKey(f'{table_user}.id'))
)

association_table_user_favourite_album = Table(table_user_favourite_album, Base.metadata,
    Column('id_album', ForeignKey(f'{table_album}.id')),
    Column('id_user', ForeignKey(f'{table_user}.id'))
)

class User(Base):
    __tablename__ = table_user
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    name_first = Column(String(50))
    name_last = Column(String(50))


class Song(Base):
    __tablename__ = table_song
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    length = Column(Integer)
    length_str = Column(String(15))


class Album(Base):
    __tablename__ = table_album
    id = Column(Integer, primary_key=True)
    name = Column(String(60))


class Artist(Base):
    __tablename__ = table_artist
    id = Column(Integer, primary_key=True)
    nickname = String(60)
    name_first = Column(String(50))
    name_last = Column(String(50))


class Label(Base):
    __tablename__ = table_label
    id = Column(Integer, primary_key=True)
    name = Column(String(150))


class Genre(Base):
    __tablename__ = table_genre
    id = Column(Integer, primary_key=True)
    name = Column(String(60))


class SessionCreator:
    """
    class which is dedicated to operate with our database
    """
    def __init__(self) -> None:
        self.db_host = db_host
        self.db_name = db_name
        self.db_pass = db_pass
        self.db_base = db_base
        self.get_folder = lambda x: os.path.exists(x) or os.mkdir(x)
        self.folder_storage = os.path.join(folder_current, folder_storage)
        self.engine = self.produce_engine()
        print(self.engine)

    def produce_engine(self) -> object:
        """
        Method which is dedicated to connect to the values of the 
        Input:  All values for the PostgeSQL
        Output: object of the session
        """
        try:
            # return create_engine(f'postgresql://{self.db_base}:{self.db_pass}@{self.db_host}/{self.db_name}')
            self.get_folder(self.folder_storage)
            self.sql_file = os.path.join(self.folder_storage, db_file)
            return create_engine(f"sqlite:///{self.sql_file}")
        except Exception as e:
            self.get_folder(self.folder_storage)
            self.sql_file = os.path.join(self.folder_storage, db_file)
            return create_engine(f"sqlite:///{self.sql_file}")
        
    def return_session(self) -> object:
        """
        Method which is dedicated to develop session
        Input:  None
        Output: We created session of the values
        """
        try:
            return Session(bind=self.engine)
        except Exception as e:
            print(e)
            print('=================================================')
            return None
