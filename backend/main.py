import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker

# ==========================================
# 1. DATABASE SETUP (Safe SQLite Version)
# ==========================================
# This creates a local file named 'thaidrill.db' right inside your folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./thaidrill.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} # Required for SQLite + FastAPI
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==========================================
# 2. DATABASE MODELS
# ==========================================
class User(Base):
    __tablename__ = "users"
    # Notice the underscore in primary_key!
    nickname = Column(String, primary_key=True, index=True)

# This physically creates the database file and tables when the app starts
Base.metadata.create_all(bind=engine)

# ==========================================
# 3. FASTAPI APP INIT
# ==========================================
app = FastAPI()

# ==========================================
# 4. WEB ROUTES
# ==========================================
@app.get("/")
def read_root():
    # Find the exact directory this main.py file is living in
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Safely glue that directory path to the index.html file name
    html_path = os.path.join(base_dir, "index.html")
    
    # Safety Check: If the file is missing, tell us exactly where it looked!
    if not os.path.exists(html_path):
        return {"error": "File not found", "looked_in_path": html_path}
        
    return FileResponse(html_path)

# (Paste any of your other @app.get or @app.post routes down here!)
