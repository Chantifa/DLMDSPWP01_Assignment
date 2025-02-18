from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TrainingData(Base):
    __tablename__ = 'training_data'
    # Define columns...

# Other model classes...