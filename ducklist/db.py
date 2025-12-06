from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./ducklist.db"  # local SQLite file
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    """Creates all tables in the database."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Provide a database session for FastAPI dependencies."""
    with Session(engine) as session:
        yield session
