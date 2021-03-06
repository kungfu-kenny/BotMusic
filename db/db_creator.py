import os
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine,
                        Table,
                        Column,
                        Integer,
                        String,
                        ForeignKey,
                        PrimaryKeyConstraint)
from sqlalchemy.orm.session import Session
from config import (table_user,
                    table_song,
                    table_label,
                    table_album,
                    table_genre,
                    table_artist,
                    table_song_year,
                    table_song_genre,
                    table_song_label,
                    table_album_song,
                    table_album_year,
                    table_album_label,
                    table_album_genre,
                    table_artist_song,
                    table_genre_label,
                    table_artist_genre,
                    table_artist_label,
                    table_artist_album,
                    table_song_youtube,
                    table_user_history_song,
                    table_user_history_album,
                    table_user_favourite_song,
                    table_user_favourite_album,
                    FolderProject,
                    DataBaseCredentials)


Base = declarative_base()


association_table_song_genre = Table(table_song_genre, Base.metadata,
    Column('id_song', ForeignKey(f'{table_song}.id')),
    Column('id_genre', ForeignKey(f'{table_genre}.id')),
    PrimaryKeyConstraint('id_song', 'id_genre'),    
)

association_table_song_label = Table(table_song_label, Base.metadata,
    Column('id_song', ForeignKey(f'{table_song}.id')),
    Column('id_label', ForeignKey(f'{table_label}.id')),
    PrimaryKeyConstraint('id_song', 'id_label')
)

association_table_album_song = Table(table_album_song, Base.metadata,
    Column('id_song', ForeignKey(f'{table_song}.id')),
    Column('id_album', ForeignKey(f'{table_album}.id')),
    PrimaryKeyConstraint('id_song', 'id_album')
)

association_table_album_label = Table(table_album_label, Base.metadata,
    Column('id_album', ForeignKey(f'{table_album}.id')),
    Column('id_label', ForeignKey(f'{table_label}.id')),
    PrimaryKeyConstraint('id_album', 'id_label')
)

association_table_album_genre = Table(table_album_genre, Base.metadata,
    Column('id_album', ForeignKey(f'{table_album}.id')),
    Column('id_genre', ForeignKey(f'{table_genre}.id')),
    PrimaryKeyConstraint('id_album', 'id_genre')
)

association_table_artist_song = Table(table_artist_song, Base.metadata,
    Column('id_song', ForeignKey(f'{table_song}.id')),
    Column('id_artist', ForeignKey(f'{table_artist}.id')),
    PrimaryKeyConstraint('id_song', 'id_artist')
)

association_table_genre_label = Table(table_genre_label, Base.metadata,
    Column('id_genre', ForeignKey(f'{table_genre}.id')),
    Column('id_label', ForeignKey(f'{table_label}.id')),
    PrimaryKeyConstraint('id_genre', 'id_label')
)

association_table_artist_genre = Table(table_artist_genre, Base.metadata,
    Column('id_artist', ForeignKey(f'{table_artist}.id')),
    Column('id_genre', ForeignKey(f'{table_genre}.id')),
    PrimaryKeyConstraint('id_artist', 'id_genre')
)

association_table_artist_label = Table(table_artist_label, Base.metadata,
    Column('id_artist', ForeignKey(f'{table_artist}.id')),
    Column('id_label', ForeignKey(f'{table_label}.id')),
    PrimaryKeyConstraint('id_artist', 'id_label')
)

association_table_artist_album = Table(table_artist_album, Base.metadata,
    Column('id_artist', ForeignKey(f'{table_artist}.id')),
    Column('id_album', ForeignKey(f'{table_album}.id')),
    PrimaryKeyConstraint('id_artist', 'id_album')
)

association_table_user_history_song = Table(table_user_history_song, Base.metadata,
    Column('id_song', ForeignKey(f'{table_song}.id')),
    Column('id_user', ForeignKey(f'{table_user}.id')),
    PrimaryKeyConstraint('id_song', 'id_user')
)

association_table_user_history_album = Table(table_user_history_album, Base.metadata,
    Column('id_album', ForeignKey(f'{table_album}.id')),
    Column('id_user', ForeignKey(f'{table_user}.id')),
    PrimaryKeyConstraint('id_album', 'id_user')
)

association_table_user_favourite_song = Table(table_user_favourite_song, Base.metadata,
    Column('id_song', ForeignKey(f'{table_song}.id')),
    Column('id_user', ForeignKey(f'{table_user}.id')),
    PrimaryKeyConstraint('id_song', 'id_user')
)

association_table_user_favourite_album = Table(table_user_favourite_album, Base.metadata,
    Column('id_album', ForeignKey(f'{table_album}.id')),
    Column('id_user', ForeignKey(f'{table_user}.id')),
    PrimaryKeyConstraint('id_album', 'id_user')
)


class SongYoutube(Base):
    __tablename__ = table_song_youtube
    id_song = Column(Integer, ForeignKey(f'{table_song}.id'), primary_key=True)
    link = Column(String(200))
    song_youtube = relationship("Song", back_populates="song_youtube")


class SongYear(Base):
    __tablename__ = table_song_year
    id_song = Column(Integer, ForeignKey(f'{table_song}.id'), primary_key=True)
    year = Column(Integer)
    song_year = relationship("Song", back_populates="song_year")


class AlbumYear(Base):
    __tablename__ = table_album_year
    id_album = Column(Integer, ForeignKey(f'{table_album}.id'), primary_key=True)
    year = Column(Integer)
    album_year = relationship("Album", back_populates="album_year")


class User(Base):
    __tablename__ = table_user
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    name_first = Column(String(50))
    name_last = Column(String(50))
    user_history_song = relationship("Song",
        secondary=association_table_user_history_song,
        back_populates="user_history_song")
    user_history_album = relationship("Album",
        secondary=association_table_user_history_album,
        back_populates="user_history_album")
    user_favourite_song = relationship("Song",
        secondary=association_table_user_favourite_song,
        back_populates="user_favourite_song")
    user_favourite_album = relationship("Album",
        secondary=association_table_user_favourite_album,
        back_populates="user_favourite_album")


class Song(Base):
    __tablename__ = table_song
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    length = Column(Integer)
    length_str = Column(String(15))
    song_year = relationship("SongYear", back_populates="song_year")
    song_youtube = relationship("SongYoutube", back_populates="song_youtube")
    song_genre = relationship("Genre",
        secondary=association_table_song_genre,
        back_populates="song_genre")
    song_label = relationship("Label",
        secondary=association_table_song_label,
        back_populates="song_label")
    album_song = relationship("Album",
        secondary=association_table_album_song,
        back_populates="album_song")
    artist_song = relationship("Artist",
        secondary=association_table_artist_song,
        back_populates="artist_song")
    user_history_song = relationship("User",
        secondary=association_table_user_history_song,
        back_populates="user_history_song")
    user_favourite_song = relationship("User",
        secondary=association_table_user_favourite_song,
        back_populates="user_favourite_song")



class Album(Base):
    __tablename__ = table_album
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    album_year = relationship("AlbumYear", back_populates="album_year")
    album_song = relationship("Song",
        secondary=association_table_album_song,
        back_populates="album_song")
    album_label = relationship("Label",
        secondary=association_table_album_label,
        back_populates="album_label")
    album_genre = relationship("Genre",
        secondary=association_table_album_genre,
        back_populates="album_genre")
    artist_album = relationship("Artist",
        secondary=association_table_artist_album,
        back_populates="artist_label")
    user_history_album = relationship("User",
        secondary=association_table_user_history_album,
        back_populates="user_history_album")
    user_favourite_album = relationship("User",
        secondary=association_table_user_favourite_album,
        back_populates="user_favourite_album")


class Artist(Base):
    __tablename__ = table_artist
    id = Column(Integer, primary_key=True)
    nickname = String(60)
    name_first = Column(String(50))
    name_last = Column(String(50))
    artist_song = relationship("Song",
        secondary=association_table_artist_song,
        back_populates="artist_song")
    artist_genre = relationship("Genre",
        secondary=association_table_artist_genre,
        back_populates="artist_genre")
    artist_label = relationship("Label",
        secondary=association_table_artist_label,
        back_populates="artist_label")
    artist_album = relationship("Album",
        secondary=association_table_artist_album,
        back_populates="artist_album")


class Label(Base):
    __tablename__ = table_label
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    album_label = relationship("Album",
        secondary=association_table_album_label,
        back_populates="album_label")
    song_label = relationship("Song",
        secondary=association_table_song_label,
        back_populates="song_label")
    genre_label = relationship("Genre",
        secondary=association_table_genre_label,
        back_populates="genre_label")
    artist_label = relationship("Artist",
        secondary=association_table_artist_label,
        back_populates="artist_label")


class Genre(Base):
    __tablename__ = table_genre
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    song_genre = relationship("Song",
        secondary=association_table_song_genre,
        back_populates="song_genre")
    album_genre = relationship("Album",
        secondary=association_table_album_genre,
        back_populates="album_genre")
    genre_label = relationship("Label",
        secondary=association_table_genre_label,
        back_populates="genre_label")
    artist_genre = relationship("Artist",
        secondary=association_table_artist_genre,
        back_populates="artist_genre")


class SessionCreator:
    """
    class which is dedicated to operate with our database
    """
    def __init__(self) -> None:
        self.db_host = DataBaseCredentials.db_host
        self.db_name = DataBaseCredentials.db_name
        self.db_pass = DataBaseCredentials.db_pass
        self.db_base = DataBaseCredentials.db_base
        self.get_folder = lambda x: os.path.exists(x) or os.mkdir(x)
        self.folder_storage = os.path.join(FolderProject.folder_current, 
                                            FolderProject.folder_storage)
        self.engine = self.return_engine()
        print(self.engine)
        self.session = self.return_session()
        print(self.session)
        print('.........................................')
        print(self.create_db())

    def return_engine(self, get_sub_engine=False) -> object:
        """
        Method which is dedicated to return engine in different cases
        Input:  get_sub_engine = boolean value which changes engine
        Output: engine for the developing database
        """
        if get_sub_engine:
            return self.produce_engine_file()
        return self.produce_engine()

    def produce_engine(self) -> object:
        """
        Method which is dedicated to create engine from the sql 
        Input:  All values for the PostgeSQL
        Output: object of the session
        """
        try:
            return create_engine(f'postgresql://{self.db_base}:{self.db_pass}@{self.db_host}/{self.db_name}')
        except Exception as e:
            print(f"We faced problems with values: {e}")
            return self.produce_engine_file()

    def produce_engine_file(self) -> object:
        """
        Method which is dedicated to create engine from the file
        Input:  None
        Output: we created engine files
        """
        self.get_folder(self.folder_storage)
        self.sql_file = os.path.join(self.folder_storage, DataBaseCredentials.db_file)
        return create_engine(f"sqlite:///{self.sql_file}")
        
    def return_session(self) -> object:
        """
        Method which is dedicated to develop session
        Input:  None
        Output: We created session of the values
        """
        try:
            Session = sessionmaker(bind=self.engine)
            return Session()
        except Exception as e:
            #TODO add here values of the logging
            try:
                self.engine = self.return_engine(True)
                Session = sessionmaker(bind=self.engine)
                return Session()
            except Exception as e:
                #TODO add here values of the logging
                pass
            return None

    def create_db(self):
        try:
            Base.metadata.create_all(self.engine)
        except Exception as e:
            print(f"We faced problems with Base: {e}")
            self.engine = self.return_engine(True)
            Base.metadata.create_all(self.engine)