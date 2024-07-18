# Environment variables
import os
from dotenv import load_dotenv

load_dotenv()
HOST     = os.getenv("HOST")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")


# SQLAlchemy and database session configuration
from database.models import Base
from sqlalchemy.orm  import Session
from sqlalchemy      import create_engine

DATABASE_URI = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"
engine = create_engine(DATABASE_URI, future=True)

def get_session() -> Session:
    try:
        return Session(engine)
    except Exception as e:
        raise ConnectionError(f'Error en la conexión a la base de datos {e}')
    