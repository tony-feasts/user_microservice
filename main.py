from fastapi import FastAPI, HTTPException, Form
import mysql.connector
from passlib.context import CryptContext

# Database connection configuration
db_config = {
    'user': 'root',
    'password': 'dbuserdbuser',
    'host': 'localhost',
    'database': 'user',
}

# Initialize FastAPI app
app = FastAPI()

# Password hashing context using Argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Function to get a database connection
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# API endpoint to add a new user (Sign Up)
@app.post("/signup")
def sign_up(username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Hash the password before storing it
    hashed_password = pwd_context.hash(password)
    try:
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))
        conn.commit()
    except mysql.connector.IntegrityError:
        conn.rollback()
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")
    cursor.close()
    conn.close()
    return {"message": "You are now signed up"}

# API endpoint for user login
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
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
        raise HTTPException(status_code=400, detail="Invalid username or password")
