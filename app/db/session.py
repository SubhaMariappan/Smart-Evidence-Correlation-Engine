from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Create SQLAlchemy engine with pool verification
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

# Transactional session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for ORM models
Base = declarative_base()

def get_db():
    """
    FastAPI dependency yielding transactional database session per HTTP request.
    Closes the session cleanly when request execution completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
