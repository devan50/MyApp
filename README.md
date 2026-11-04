# Task Manager – Dockerized Web Application

A simple full-stack Task Manager application built using **Python Flask, PostgreSQL, HTML, CSS, JavaScript, Nginx, and Docker Compose**.

The application allows users to create, view, update, and delete tasks through a web dashboard. The entire application runs using Docker containers.

## Features

- Create new tasks with a title and description.
- View all available tasks.
- Update task status (Pending / Completed).
- Delete tasks.
- Search and filter tasks.
- Store task data in PostgreSQL.
- Serve the frontend using Nginx.
- Connect frontend and backend through an Nginx reverse proxy.
- Run all services using Docker Compose.
- Persist database data using Docker volumes.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | REST API |
| PostgreSQL 16 | Database |
| HTML, CSS, JavaScript | Frontend |
| Nginx | Web server and reverse proxy |
| Docker | Containerization |
| Docker Compose | Multi-container management |

## Project Structure

```text
MYAPP/
│
├── api/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── web/
│   ├── index.html
│   ├── Dockerfile
│   └── nginx.conf
│
├── .env
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Application Architecture

```text
             User Browser
                  |
                  | http://localhost:8080
                  |
             Nginx (Web)
                  |
                  | /api/
                  |
             Flask API
                  |
                  |
              PostgreSQL
                  |
             Docker Volume
```

### Services

- **Web:** Nginx serves the frontend dashboard on port `8080`.
- **API:** Flask handles task operations on container port `5000`, mapped to host port `8000`.
- **Database:** PostgreSQL stores task information on port `5432` internally.
- **Volume:** `db_data` preserves PostgreSQL data even if containers are recreated.

## Requirements

Install the following on your system:

- Docker Engine
- Docker Compose plugin
- Git

## Configuration

Create a `.env` file in the project root:

```env
APP_PORT=5000
DB_HOST=db
DB_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=taskmanager
```

**Important:** Change the example password before using this application beyond local development. Never commit your `.env` file to GitHub.

## Run the Application

Clone the repository:

```bash
git clone https://github.com/devan50/MyAPP.git
```

Enter the project directory:

```bash
cd MyAPP
```

Build and start all services:

```bash
sudo docker compose up -d --build
```

Check running containers:

```bash
sudo docker compose ps
```

View application logs:

```bash
sudo docker compose logs -f
```

## Access the Application

Open your browser:

**Frontend Dashboard:** http://localhost:8080

**Backend API:** http://localhost:8000

**API Health Check:** http://localhost:8000/health

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Check API and database health |
| GET | `/tasks` | Retrieve all tasks |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/<id>` | Update task status |
| DELETE | `/tasks/<id>` | Delete a task |

### Example: Create a Task

```bash
curl -X POST http://localhost:8000/tasks \
-H "Content-Type: application/json" \
-d '{"title":"Learn Docker","description":"Practice Docker Compose"}'
```

### Example: View Tasks

```bash
curl http://localhost:8000/tasks
```

## Docker Commands

Check containers:

```bash
sudo docker compose ps
```

View logs:

```bash
sudo docker compose logs -f api
```

Stop services:

```bash
sudo docker compose down
```

Restart services:

```bash
sudo docker compose up -d
```

Rebuild the application:

```bash
sudo docker compose up -d --build
```

**Note:** `docker compose down` does not remove the named database volume. Your PostgreSQL data remains stored in `db_data`.

## Learning Objectives

This project is also a hands-on learning exercise covering:

- Docker images and containers.
- Writing Dockerfiles.
- Docker Compose.
- Container networking.
- Service-to-service communication.
- Environment variables.
- Docker volumes and data persistence.
- Nginx reverse proxy configuration.
- Flask REST API development.
- PostgreSQL integration.
- Git and GitHub version control.

## Author

**Devan**

GitHub: [@devan50](https://github.com/devan50)
