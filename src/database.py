from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class TrainingData(Base):
    __tablename__ = 'training_data'
    x = Column(Float, primary_key=True)
    y1 = Column(Float)
    y2 = Column(Float)
    y3 = Column(Float)
    y4 = Column(Float)

class IdealFunctions(Base):
    __tablename__ = 'ideal_functions'
    x = Column(Float, primary_key=True)
    y1 = Column(Float)
    y2 = Column(Float)
    # ... up to y50

class TestData(Base):
    __tablename__ = 'test_data'
    x = Column(Float, primary_key=True)
    y = Column(Float)
    delta_y = Column(Float)
    ideal_func_no = Column(Integer)

class DatabaseManager:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(__file__), '..', 'function_fitter.db')
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()