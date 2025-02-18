import pandas as pd

from src.database import engine

# Example for training data:
df = pd.read_csv('training_data.csv')
df.to_sql('training_data', con=engine, if_exists='replace', index=False)
