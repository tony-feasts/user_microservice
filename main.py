from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
from passlib.context import CryptContext
import os

DB_PASSWORD = os.getenv('DB_PASSWORD')

# Database connection configuration
db_config = {
    'user': 'admin',  # Replace with your actual database username
    'password': DB_PASSWORD,
    'host': 'cloudproject.crimg8c22499.us-east-2.rds.amazonaws.com',  # Replace with your RDS endpoint
    'database': 'user',  # Replace with your actual database name
}

# Initialize FastAPI app
app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for your frontend's domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# Password hashing context using Argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Function to get a database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Pydantic model for user credentials
class UserCredentials(BaseModel):
    username: str
    password: str

# API endpoint to add a new user (Sign Up)
@app.post("/signup")
def sign_up(credentials: UserCredentials):
    username = credentials.username
    password = credentials.password
    hashed_password = pwd_context.hash(password)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "You are now signed up"}
    except mysql.connector.IntegrityError:
        # Handle duplicate username error
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail="An internal error occurred.")

# API endpoint for user login
@app.post("/login")
def login(credentials: UserCredentials):
    username = credentials.username
    password = credentials.password
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result and pwd_context.verify(password, result[0]):
            return {"message": "You are logged in"}
        else:
            # Invalid credentials
            raise HTTPException(status_code=400, detail="Invalid username or password")
    except HTTPException as e:
        # Re-raise HTTPExceptions to allow FastAPI to handle them
        raise e
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail="An internal error occurred.")
