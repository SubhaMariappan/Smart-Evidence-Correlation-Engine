from sqlalchemy import inspect, text
from app.db.session import engine, Base
import app.models  # Ensures all ORM models are registered with Base.metadata

def init_prototype_schema():
    """
    TEMPORARY PROTOTYPE INITIALIZATION MECHANISM.
    Uses Base.metadata.create_all() to create missing prototype tables in sece_db.
    Safely adds missing columns if prototype tables were created in earlier steps.
    """
    print("[*] Initializing prototype tables in target database...")
    Base.metadata.create_all(bind=engine)
    
    # Ensure status column is present on entity_matches
    try:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE entity_matches ADD COLUMN IF NOT EXISTS status VARCHAR(30) NOT NULL DEFAULT 'PENDING_REVIEW';"))
    except Exception as e:
        print(f"[!] Column check notice: {e}")

    # Inspect created tables
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"[+] Active tables in database: {tables}")
    return tables
