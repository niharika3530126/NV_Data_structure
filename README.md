# NV_Data_structure
Data Structure Management Service

This project handles Datasets and DataElements of a service using FastAPI and SQLite

**Tech stack Used :**

	•	Language: Python 
	
	•	Framework: FastAPI
	
	•	Database: SQLite
	
	•	ORM: SQLAlchemy
	
	•	Testing: pytest

**Project Structure:**

project

	├── app/
	│   ├── __init__.py
	│   ├── main.py          # FastAPI app & routes
	│   ├── database.py      # DB engine & session
	│   ├── models.py        # SQLAlchemy models
	│   └── schemas.py       # Pydantic schemas
	│         
	├── tests/
	│   └── test_data.py     # Pytest test cases
	├── conftest.py          # Pytest path configuration
	├── requirements.txt      
	└── Dockerfile

**Testing Strategy**

	•	Tests are written using pytest
	
	•	FastAPI’s TestClient is used for integration testing
	
	•	Each test runs with a fresh in-memory SQLite database
	
	
	
