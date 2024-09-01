# AsyncPress: Asynchronous Image Processing System

AsyncPress is a Django-based application designed to handle asynchronous image processing tasks using Celery, Redis, and SQLite. The system accepts CSV files with image URLs, processes the images by compressing them, and stores the results in a database. It provides APIs to upload files, check processing status, and to download output files.

## Technologies

- Python 3.11
- Framework - Django
- Worker & Task Queue- Celery
- Message Broker - Redis
- Database - SQLite
- Server - Nginx

## Running the Project Locally

Follow these steps to run the project locally using Docker:

### 1. Clone the Repository

Clone the repository from GitHub:

```bash
git clone https://github.com/ChetanNagane/asyncPress.git
cd asyncpress
```

### 2. Build Docker Containers

Build the Docker containers using the docker-compose command:
```bash
docker-compose build
```


### 3. Run Docker Containers

Start all the Docker containers with the following command:

```bash
docker-compose up
```

To Check Working Please view the [Docs](docs/Docs.md) 
.

## API Endpoints

### 1. Upload API

Uploads a CSV file and returns a unique request ID for tracking the processing status.

- **Endpoint**: `/api/upload/`
- **Method**: `POST`
- **Request**: 
  - `file`: A CSV file (form-data field named `file`)
- **Response**: 
  - JSON object containing a unique `request_id`.

#### Example using `curl`:

```bash
curl -X POST -F "file=@path/to/yourfile.csv" http://localhost:8000/api/upload/
```

### 2. Status API

Check the processing status using the request ID.

- **Endpoint:** `/api/status/<request_id>/`
- **Method:** `GET`
- **Response:** JSON object containing the status of the processing (`"in_progress"`, `"completed"`, or `"failed"`).

#### Example using `curl`

```bash
curl -X GET http://localhost:8000/api/status/your_request_id/
```

### 3. Output CSV API

- **URL**: `/api/download_csv/<request_id>/`
- **Method**: `GET`
- **Description**: Downloads the CSV file after processing is completed. Replace `<request_id>` with the actual ID of your request.

### Example Request

You can use `curl` to make a request to this endpoint. Here is an example:

```bash
curl -X GET http://localhost:8000/api/download_csv/your_request_id/ -o output.csv
```