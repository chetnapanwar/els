import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Database Connection Details
DB_CONFIG = {
    "dbname": "els_db",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Data Model
class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    password: str

# Mount static files
from pathlib import Path
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/users", response_model=List[User])
def get_users():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users ORDER BY id;")
        users = cur.fetchall()
        cur.close()
        conn.close()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            return user
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users", response_model=User)
def create_user(user: User):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = """
        INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)
        RETURNING *;
        """
        cur.execute(query, (user.name, user.email, user.password))
        new_user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
