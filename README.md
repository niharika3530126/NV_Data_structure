# NV_Data_structure
Data Structure Management Service

This project handles Datasets and DataElements of a service using FastAPI and SQLite

**Tech stack Used :**

	•	Language: Python 
	
	•	Framework: FastAPI
	
	•	Database: SQLite
	
	•	ORM: SQLAlchemy
	
	•	Testing: pytest

	•	Containerization : Docker

**Project Structure:**

project

	├── app/
	│   ├── __init__.py
	│   ├── main.py          
	│   ├── database.py      
	│   ├── models.py        
	│   └── schemas.py      
	│         
	├── tests/
	│   └── test_data.py    
	├── conftest.py          
	├── requirements.txt      
	└── Dockerfile

## Data Models

### Dataset

Represents a business entity 

Fields:

* id
* name (unique)
* description
* created_by

### DataElement

Represents a field belonging to a dataset.

Fields:

* id
* dataset_id (FK → Dataset)
* name
* data_type
* is_required
* is_pii
* created_at

### Constraints

* Dataset name must be **unique**
* Data element names must be **unique per dataset**
* Foreign key enforced with cascade delete

## API Endpoints

### Create a Dataset

POST /datasets

Example:

json

{

  "name": "Customer",
  
  "description": "Customer data"
  
}

### List only Datasets without data elements

GET /datasets

### List Datasets with data elements

GET /datasetselements

### Retrive data elements belonging to particluar dataset

GET /datasets/{dataset_id}

### Add Data Element to Dataset

POST /datasets/{dataset_id}/elements

Example

json

{

  "name": "email",
  
  "data_type": "string",
  
  "is_required": true,
  
  "is_pii": true
  
}

### Updating a Dataset

PATCH /datasets/{dataset_id}

whichever field is required to update only give that field

Example:

json
{
  
  "description": "Customer data"
  
}

### Updating Data Element to Dataset

PATCH /datasets/{dataset_id}/elements/{element_id}

whichever field is required to update only give that field

Example

json

{

  "name": "email"
  
}

### Deleting Dataset

DELETE /datasets/{dataset_id}


## Running with Docker

Requires Docker-Desktop

### 1️ Build Docker Image

From the project root:
 Build the image
 
 	docker build -t data-structure-service .

### 2️ Run the Application in Docker

docker run -p 8000:8000 data-structure-service

Access the application:

I have used http://0.0.0.0:8000 in docker file

* Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)

### 3️ Run Tests in Docker

docker run --rm data-structure-service pytest


Expected output:

```
collected 3 items
tests/test_data.py ...                             [100%]
```

`--rm` ensures the test container is removed automatically after execution.


	**Testing Details**
	
		•	Tests are written using pytest
		
		•	FastAPI’s TestClient is used for integration testing
		
		•	Each test runs with a fresh in-memory SQLite database
	
	
	
