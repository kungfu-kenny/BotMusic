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
from config import (
    FolderProject,
    DataBaseCredentials,
    DataBaseCredentialsMongo,
)


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, default='')
    surname = Column(String, default='')
    username = Column(String, default='')

class SessionCreatorMongo:
    """
    class which is dedicated to operate the Mongo database
    """
    def __init__(self) -> None:
        self.db_host = DataBaseCredentialsMongo.host
        self.db_name = DataBaseCredentialsMongo.name
        self.db_pass = DataBaseCredentialsMongo.pawd
        self.db_base = DataBaseCredentialsMongo.base
        self.db_port = DataBaseCredentialsMongo.port
        
    "mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/myFirstDatabase"

class SessionCreatorPostgre:
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