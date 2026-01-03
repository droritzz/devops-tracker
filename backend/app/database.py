from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import logging
from sqlalchemy.exc import OperationalError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/devops_tracker"

# Create engine with connection pooling
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=300,    # Recycle connections every 5 minutes
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def wait_for_db(max_retries=30, delay=1):
    """Wait for database to be available with retry logic"""
    for attempt in range(max_retries):
        try:
            # Test the connection
            connection = engine.connect()
            connection.close()
            logger.info("Successfully connected to database")
            return True
        except OperationalError as e:
            if attempt == max_retries - 1:
                logger.error(f"Could not connect to database after {max_retries} attempts: {e}")
                raise
            logger.warning(f"Database connection attempt {attempt + 1}/{max_retries} failed, retrying in {delay} seconds...")
            time.sleep(delay)
    return False

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
