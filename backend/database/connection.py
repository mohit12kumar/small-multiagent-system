import pymysql
from urllib.parse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.config import settings

def create_db_engine():
    db_url = settings.DATABASE_URL
    
    if "mysql" in db_url:
        try:
            # Parse connection URL
            clean_url = db_url.replace("mysql+pymysql://", "http://")
            parsed = urlparse(clean_url)
            user = parsed.username or "root"
            password = parsed.password or ""
            host = parsed.hostname or "localhost"
            port = parsed.port or 3306
            dbname = parsed.path.lstrip("/")
            
            if dbname:
                conn = pymysql.connect(
                    host=host,
                    user=user,
                    password=password,
                    port=port,
                    autocommit=True
                )
                with conn.cursor() as cursor:
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                conn.close()
                print(f"[Database Setup]: Verified/Created MySQL database '{dbname}' automatically.")
                
            engine_kwargs = {
                "pool_pre_ping": True,
                "pool_size": 10,
                "max_overflow": 20,
                "pool_recycle": 3600,
            }
            eng = create_engine(db_url, **engine_kwargs)
            # Test connection
            with eng.connect() as test_conn:
                pass
            print(f"[Database Setup]: Successfully connected to MySQL database engine.")
            return eng
        except Exception as e:
            print(f"[Database Setup Warning]: Could not connect to MySQL database ({e}). Falling back to SQLite database.")
            
    # Fallback to SQLite
    sqlite_url = "sqlite:///./interview_assistant.db"
    return create_engine(sqlite_url, connect_args={"check_same_thread": False}, pool_pre_ping=True)

engine = create_db_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
