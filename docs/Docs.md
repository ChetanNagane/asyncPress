
## Components

### 1. Backend (Django)
- Handles CSV uploads, validates data, stores it in the database, and adds image processing tasks to the task queue.

### 2. Redis
- Acts as a message broker, queuing tasks from the backend for asynchronous processing by Celery workers.

### 3. Asynchronous Workers (Celery)
- Fetch tasks from Redis, process images (e.g., compression), and store results back in the database.

### 4. Nginx
- Serves as a web server and reverse proxy, directing traffic to the Django backend and efficiently serving static files.

### 5. Database (SQLite)
- Stores CSV input data, output data, and results from image processing tasks, providing persistence and retrieval for the application's operations.

## System Design

<img src="images/system design.png" alt="system design" />

## DB Design

<img src="images/DB design.png" alt="DB design" />
