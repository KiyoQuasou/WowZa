from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
import os

# Database setup
# Render provides the database URL in the environment variable 'DATABASE_URL'
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# Handle Render's postgres:// vs postgresql:// quirk if necessary
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class UserStreak(Base):
    __tablename__ = "user_streaks"
    nickname = Column(String, primary_key=True, index=True)
    streak_count = Column(Integer, default=0)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change this to your actual frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schema for incoming requests
class UserStart(BaseModel):
    nickname: str

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/start-quiz")
def start_quiz(user: UserStart, db: Session = Depends(get_db)):
    # Find user or create new one
    db_user = db.query(UserStreak).filter(UserStreak.nickname == user.nickname).first()
    
    if db_user:
        db_user.streak_count += 1
    else:
        db_user = UserStreak(nickname=user.nickname, streak_count=1)
        db.add(db_user)
    
    db.commit()
    db.refresh(db_user)
    
    return {"nickname": db_user.nickname, "streak_count": db_user.streak_count}
