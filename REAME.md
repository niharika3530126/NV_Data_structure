# Backend Home Assignment – Data Structure Management Service

## Overview

This project implements a **Data Structure Management Service** using **FastAPI** and **SQLite**.
It allows managing metadata about business datasets and their data elements.

The project demonstrates:

* Clean backend design
* REST API development with FastAPI
* Relational data modeling using SQLAlchemy
* Automated testing with pytest
* Containerization using Docker

---

## Tech Stack

* **Language:** Python 3
* **Framework:** FastAPI
* **Database:** SQLite
* **ORM:** SQLAlchemy
* **Testing:** pytest
* **Containerization:** Docker Desktop

---

## Project Structure

```
project

  ├── app/
  │   ├── __init__.py
  │   ├── main.py          # FastAPI app & routes
  │   ├── database.py      # DB engine & session
  │   ├── models.py        # SQLAlchemy models
  │   ├── schemas.py       # Pydantic schemas
  │   └── crud.py          # DB operations
  ├── tests/
  │   └── test_data.py     # Pytest test cases
  ├── conftest.py          # Pytest path configuration
  ├── Dockerfile
  ├── requirements.txt
  ├── .dockerignore
  └── README.md
```

---

## Data Model

### Dataset

Represents a business entity (e.g., Customer, Order).

Fields:

* `id`
* `name` (unique)
* `description`
* `created_at`
* `updated_at`

### DataElement

Represents a field belonging to a dataset.

Fields:

* `id`
* `dataset_id` (FK → Dataset)
* `name`
* `data_type`
* `is_required`
* `is_pii`
* `created_at`
* `updated_at`

### Constraints

* Dataset name must be **unique**
* Data element names must be **unique per dataset**
* Foreign key enforced with cascade delete

---

## API Endpoints

### Create Dataset

```
POST /datasets
```

```json
{
  "name": "Customer",
  "description": "Customer master data"
}
```

---

### List Datasets

```
GET /datasets
```

---

### Get Dataset (with data elements)

```
GET /datasets/{dataset_id}
```

---

### Add Data Element to Dataset

```
POST /datasets/{dataset_id}/elements
```

```json
{
  "name": "email",
  "data_type": "string",
  "is_required": true,
  "is_pii": true
}
```

---

## Running the Application Locally (Without Docker)

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Start the Server

```bash
uvicorn app.main:app --reload
```

Swagger UI:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Running Tests Locally

```bash
pytest
```

Expected output:

```
collected 3 items
tests/test_data.py ...                             [100%]
```

Tests use an **in-memory SQLite database** to ensure isolation and speed.

---

## Running with Docker

### 1️⃣ Build Docker Image

From the project root:

```
bash
docker build -t data-structure-service .
```

---

### 2️⃣ Run the Application in Docker

```bash
docker run -p 8000:8000 data-structure-service
```

Access the application:

* Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 3️⃣ Run Tests in Docker

Tests can be run **without stopping the running container**.
Open a new terminal and run:

```bash
docker run --rm data-structure-service pytest
```

Expected output:

```
collected 3 items
tests/test_data.py ...                             [100%]
```

`--rm` ensures the test container is removed automatically after execution.

---

## Docker Workflow Explained

* Each `docker run` command creates a **new container**
* The API container runs the FastAPI server
* The test container runs pytest independently
* Both containers are isolated and do not interfere with each other

---

## Design Decisions & Trade-offs

* **SQLite** chosen for simplicity and ease of setup
* **HTTP 409 Conflict** used for duplicate dataset creation
* **Integration tests** used instead of mocking DB logic
* **StaticPool** used in tests to support SQLite in-memory databases
* Docker used for reproducible environments

---

## Optional Enhancements

* Docker Compose support
* Authentication & authorization
* Dataset versioning
* Field-level validation rules
* Health check endpoint

---

