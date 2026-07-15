from app.database.connection import engine
from app.database.models import Base

def init_database():
    Base.metadata.create_all(
        engine
    )

if __name__ == "__main__":

    init_database()