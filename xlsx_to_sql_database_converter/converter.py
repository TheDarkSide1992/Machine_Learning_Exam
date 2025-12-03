import os
import pandas as pd
from sqlalchemy import create_engine
from exam_agent.config import DATABASE as DBCONFIG

PG_USER = DBCONFIG["user"]
PG_PASSWORD = DBCONFIG["password"]
PG_HOST = DBCONFIG["host"]
PG_PORT = DBCONFIG["port"]
PG_DATABASE = DBCONFIG["database"]

data = "data/OpenFoodToxTX22809_2023.xlsx"
current_directory = os.getcwd()



csv_files =[
    "Dictionary",
    "CHEM_ASSESS",
    "COM_SYNONYM",
    "QUESTION",
    "GENOTOX_KJ",
    "ENDPOINTSTUDY_KJ",
    "COMPONENT",
    "STUDY",
    "OPINION"
]

conn_string = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
engine = create_engine(conn_string)


for file_name in csv_files:
    try:
        print(f"Reading file: {file_name}")
        df = pd.read_excel(data,sheet_name=file_name)
        df.columns = [col.lower().strip().replace(' ', '_').replace('.', '_') for col in df.columns]

        table_name = file_name
        df.to_sql(
            table_name,
            engine,
            if_exists='replace',
            index=False
        )
        print(f"Success: {file_name} is imported and converted to {table_name}")

    except Exception as e:
        print(f"Error while importing {file_name}: {e}")

print("\nXlsx fully converted to sql database")