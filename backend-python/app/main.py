from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import init_db, get_db, User
from passlib.context import CryptContext

# Initialize FastAPI app
app = FastAPI()

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize the database
@app.on_event("startup")
async def startup():
    init_db()

# Pydantic model for user registration request
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

# User registration endpoint
@app.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password
    hashed_password = pwd_context.hash(user.password)
    
    # Create a new user and save to the database
    db_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "User successfully registered", "user": {"id": db_user.id, "name": db_user.name, "email": db_user.email}}