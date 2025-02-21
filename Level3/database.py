from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DB_CONFIG  # Import the config

from sqlalchemy import create_engine
from urllib.parse import quote_plus  # Add this
from config import DB_CONFIG

Base = declarative_base()


#starting


# URL-encode the password
encoded_password = quote_plus(DB_CONFIG["password"])

# Create connection URL
connection_url = (
    f"postgresql://{DB_CONFIG['user']}:{encoded_password}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/"
    f"{DB_CONFIG['dbname']}"
)

engine = create_engine(connection_url)

#ending

























Session = sessionmaker(bind=engine)

class Dialogue(Base):
    __tablename__ = "dialogues"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    character_name = Column(String(100))
    dialogue = Column(Text)

# Create tables if not exists
Base.metadata.create_all(engine)