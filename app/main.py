from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .database import engine, SessionLocal
from . import models, schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Data Structure Management Service")

@app.get("/")
def main_page():
    return  "Data Structure Management Service"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Creating Dataset

@app.post("/datasets", response_model=schemas.DatasetResponse)
def create_dataset(dataset: schemas.DatasetCreate,db: Session = Depends(get_db)):
    new_dataset = models.Dataset(name=dataset.name,description=dataset.description)
    db.add(new_dataset)
    try:
        db.commit()
        db.refresh(new_dataset)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"Dataset with name '{dataset.name}' already exists",
        )
    return new_dataset


# Get only Datasets (no data elements)
@app.get("/datasets", response_model=list[schemas.DatasetResponse])
def get_datasets(db: Session = Depends(get_db)):
    return db.query(models.Dataset).all()

# Get All Datasets with data elements
@app.get("/datasetselements", response_model=list[schemas.DatasetResponsewithElements])
def get_datasets_with_elements(db: Session = Depends(get_db)):
    return db.query(models.Dataset).all()


# get only one dataset with all data elements having same dataset_id
@app.get("/datasets/{dataset_id}",response_model=schemas.DatasetResponse)
def get_dataelements_with_dataset_id(dataset_id: int, db: Session = Depends(get_db)):
    dataset = (db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first())

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return dataset


# Adding Data Elements to Dataset

@app.post("/datasets/{dataset_id}/elements",response_model=schemas.DataElementResponse)
def adding_data_element(dataset_id: int,element: schemas.DataElementCreate,db: Session = Depends(get_db)):
    dataset = (db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first())

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    new_element = models.DataElement(
        name=element.name,
        data_type=element.data_type,
        is_required=element.is_required,
        is_pii=element.is_pii,
        dataset_id=dataset_id,
    )

    db.add(new_element)
    try:
        db.commit()
        db.refresh(new_element)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"Data element '{element.name}' already exists in this dataset",
        )

    return new_element

#updating data set for only required fields

@app.patch("/datasets/{dataset_id}", response_model=schemas.DatasetResponse)
def updating_dataset(dataset_id: int,dataset_update: schemas.DatasetUpdate,db: Session = Depends(get_db)):
    dataset = db.query(models.Dataset).filter_by(id=dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    for field, value in dataset_update.model_dump(exclude_unset=True).items():
        setattr(dataset, field, value)
    try:
        db.commit()
        db.refresh(dataset)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Dataset with this name already exists",
        )

    return dataset

#updating data elements
@app.patch("/datasets/{dataset_id}/elements/{element_id}",response_model=schemas.DataElementResponse)
def updating_data_element(dataset_id: int,element_id: int,element_update: schemas.DataElementUpdate,db: Session = Depends(get_db)):
    element = (db.query(models.DataElement).filter_by(id=element_id, dataset_id=dataset_id).first())

    if not element:
        raise HTTPException(status_code=404, detail="Data element not found")

    for field, value in element_update.model_dump(exclude_unset=True).items():
        setattr(element, field, value)

    try:
        db.commit()
        db.refresh(element)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Duplicate element name in dataset",
        )

    return element

# Deleting a Dataset 

@app.delete("/datasets/{dataset_id}", status_code=204)
def delete_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset = (
        db.query(models.Dataset)
        .filter(models.Dataset.id == dataset_id)
        .first()
    )

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    db.delete(dataset)
    db.commit()
    return "Deleted successfully"

