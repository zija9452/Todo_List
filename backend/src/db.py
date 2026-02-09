from sqlmodel import create_engine, Session
from sqlalchemy import event
from sqlalchemy.pool import QueuePool
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    # Connection pool configuration
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    echo=False           # Set to True for SQL query logging
)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for use with dependency injection in FastAPI routes.

    Yields:
        Session: A SQLModel session for database operations
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """
    Create the database tables based on the defined models.
    This should be called when starting the application.
    """
    from .models import Task  # Import here to avoid circular imports
    from sqlmodel import SQLModel

    # Create all tables defined in SQLModel classes
    SQLModel.metadata.create_all(engine)


# Optional: Add event listeners for connection monitoring
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Set SQLite pragmas for better performance and concurrency.
    This is only applied when using SQLite.
    """
    if "sqlite" in DATABASE_URL.lower():
        cursor = dbapi_connection.cursor()
        # Enabling WAL mode for better concurrency
        cursor.execute("PRAGMA journal_mode=WAL")
        # Increasing cache size
        cursor.execute("PRAGMA cache_size=10000")
        # Enabling foreign key constraints
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


if __name__ == "__main__":
    # This allows us to create tables by running this file directly
    create_db_and_tables()
    print("Database tables created successfully.")