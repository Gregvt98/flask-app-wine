from app import db
from models import Wine
import pandas as pd


df = pd.read_csv('data/final_dataset_wines_annotated.csv')

df = df.head(100)

df.rename(columns={'Unnamed: 0':'id'}, inplace=True)

print(df.columns)

data = df.to_dict('records')
db.engine.execute(Wine.__table__.insert(), data)