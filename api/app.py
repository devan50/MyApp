
import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_PATH = os.getenv("DB_PATH", "/data/tasks.db")


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0
            )
        """)


@app.route("/")
def home():
    return jsonify({
        "message": "Task Manager API is running!",
        "endpoints": [
            "/health",
            "/api/tasks"
        ]
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


# Get all tasks
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    with get_db() as conn:
        tasks = conn.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()

    return jsonify([dict(task) for task in tasks])


# Create a new task
@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Task title is required"}), 400

    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (title.strip(),)
        )
        task_id = cursor.lastrowid

    return jsonify({
        "id": task_id,
        "title": title.strip(),
        "completed": False
    }), 201


# Update task completion status
@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}

    if not isinstance(data.get("completed"), bool):
        return jsonify({"error": "completed must be true or false"}), 400

    with get_db() as conn:
        cursor = conn.execute(
            "UPDATE tasks SET completed = ? WHERE id = ?",
            (data["completed"], task_id)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task updated successfully"})


# Delete a task
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with get_db() as conn:
        cursor = conn.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted successfully"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

