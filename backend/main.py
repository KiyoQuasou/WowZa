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
    # 1. Find where main.py is (the 'backend' folder)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Go UP one level to the main project folder
    parent_dir = os.path.dirname(current_dir)
    
    # 3. Look for index.html in that main folder
    html_path = os.path.join(parent_dir, "index.html")
    
    # Safety Check!
    if not os.path.exists(html_path):
        return {"error": "File not found", "looked_in_path": html_path}
        
    return FileResponse(html_path)
# (Paste any of your other @app.get or @app.post routes down here!)
