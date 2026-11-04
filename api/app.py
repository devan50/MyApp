
import os
import psycopg2
from flask import Flask, request, jsonify
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# PostgreSQL configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("POSTGRES_DB", "taskmanager"),
    "user": os.getenv("POSTGRES_USER", "admin"),
    "password": os.getenv("POSTGRES_PASSWORD", "mypassword")
}


# Database connection
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


# Create tasks table
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            status VARCHAR(30) DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


# API home
@app.route("/")
def home():
    return jsonify({
        "application": "Professional Task Manager",
        "version": "1.0",
        "status": "running"
    })


# Health check
@app.route("/health")
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as error:
        return jsonify({"status": "unhealthy", "error": str(error)}), 500


# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM tasks ORDER BY id DESC")
    tasks = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(tasks)


# Add a task
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "Task title is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        INSERT INTO tasks (title, description)
        VALUES (%s, %s)
        RETURNING *
    """, (data["title"], data.get("description", "")))

    task = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return jsonify(task), 201


# Update task status
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()

    if not data or not data.get("status"):
        return jsonify({"error": "Status is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        UPDATE tasks
        SET status = %s
        WHERE id = %s
        RETURNING *
    """, (data["status"], task_id))

    task = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task)


# Delete task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    deleted = cur.rowcount

    conn.commit()
    cur.close()
    conn.close()

    if deleted == 0:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted successfully"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.getenv("APP_PORT", 5000)))

