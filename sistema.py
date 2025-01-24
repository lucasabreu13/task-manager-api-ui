from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List
import sqlite3
import jwt
import datetime

# App Initialization
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "your_secret_key"

def create_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL,
        due_date TEXT
    )
    """)
    conn.commit()
    conn.close()

create_db()

# Models
class Task(BaseModel):
    title: str
    description: str
    status: str
    due_date: str

class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    status: str = None
    due_date: str = None

class User(BaseModel):
    username: str
    password: str

# Utility Functions
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def authenticate_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)

# Routes
@app.post("/token")
def login(user: User):
    if user.username == "admin" and user.password == "admin":
        payload = {
            "sub": user.username,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/tasks", response_model=dict, dependencies=[Depends(authenticate_user)])
def create_task(task: Task):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, status, due_date) VALUES (?, ?, ?, ?)",
        (task.title, task.description, task.status, task.due_date)
    )
    conn.commit()
    conn.close()
    return {"message": "Task created successfully!"}

@app.get("/tasks", response_model=List[Task], dependencies=[Depends(authenticate_user)])
def read_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, description, status, due_date FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return [
        {"title": t[0], "description": t[1], "status": t[2], "due_date": t[3]} for t in tasks
    ]

@app.put("/tasks/{task_id}", response_model=dict, dependencies=[Depends(authenticate_user)])
def update_task(task_id: int, task: TaskUpdate):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    query = "UPDATE tasks SET "
    updates = []
    params = []

    if task.title:
        updates.append("title = ?")
        params.append(task.title)
    if task.description:
        updates.append("description = ?")
        params.append(task.description)
    if task.status:
        updates.append("status = ?")
        params.append(task.status)
    if task.due_date:
        updates.append("due_date = ?")
        params.append(task.due_date)

    query += ", ".join(updates) + " WHERE id = ?"
    params.append(task_id)

    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return {"message": "Task updated successfully!"}

@app.delete("/tasks/{task_id}", response_model=dict, dependencies=[Depends(authenticate_user)])
def delete_task(task_id: int):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return {"message": "Task deleted successfully!"}
