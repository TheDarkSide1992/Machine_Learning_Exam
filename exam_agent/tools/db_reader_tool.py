import psycopg2
from exam_agent.config import DATABASE as DBCONFIG

def search_database(name:str):
    connection = psycopg2.connect(database=DBCONFIG["database"], user=DBCONFIG["user"], password=DBCONFIG["password"], host=DBCONFIG["host"], port=DBCONFIG["port"])

    cursor = connection.cursor()

    #TODO Replace Table and * with relevant information once actual schema is nown
    cursor.execute(f"SELECT * FROM Table WHERE Name = '%{name}%'")

    record = cursor.fetchall()

    return record

if __name__ == "__main__":
    search_database()