from sqlalchemy import Column, String, Boolean, ForeignKey ,Integer,UniqueConstraint,DateTime,func
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True,nullable=False)
    description = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)

    elements = relationship("DataElement", back_populates="dataset",cascade="all, delete-orphan")


class DataElement(Base):
    __tablename__ = "data_elements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False)
    data_type = Column(String,nullable=False)
    is_required = Column(Boolean,default=False)
    is_pii = Column(Boolean, default=False)
    dataset_id = Column(Integer, ForeignKey("datasets.id",ondelete="CASCADE"),nullable=False,index=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)

    dataset = relationship("Dataset", back_populates="elements")

    __table_args__ = (
        UniqueConstraint("dataset_id", "name", name="uq_dataset_element"),
        )



