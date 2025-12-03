import psycopg2
from typing import TypedDict, Optional
from exam_agent.config import DATABASE as DBCONFIG

class ToxicEntry(TypedDict):
    sub_name: str
    sub_description: str
    molecularformula: str
    com_type: str
    sub_op_class: Optional[str]
    is_mutagenic: Optional[str]
    is_genotoxic: Optional[str]
    is_carcinogenic: Optional[str]
    remarks_study: str
    riskunit: str
    remarks :str
    assess: str


def search_database(search: str):
    global dict

    _rows = """
                sub_name,
                sub_description,
                molecularformula,
                com_type,
                sub_op_class,
                is_mutagenic,
                is_genotoxic,
                is_carcinogenic,
                remarks_study,
                riskunit,
                remarks,
                assess
                """

    connection = psycopg2.connect(database=DBCONFIG["database"], user=DBCONFIG["user"], password=DBCONFIG["password"],
                                  host=DBCONFIG["host"], port=DBCONFIG["port"])

    cursor = connection.cursor()

    query = f"""SELECT {_rows}            
                FROM "COMPONENT"
                JOIN "STUDY" ON "COMPONENT".sub_com_id = "STUDY".study_id
                JOIN "CHEM_ASSESS" ON "STUDY".hazard_id = "CHEM_ASSESS".hazard_id
                WHERE comparamname LIKE '%{search}%';"""

    cursor.execute(query=query)

    record = cursor.fetchall()

    # gets fields
    field_names = list(ToxicEntry.__annotations__.keys())

    # maps to dictionarry
    dict = dict(map(lambda field_names, record: (field_names, record), field_names, record))

    return record


if __name__ == "__main__":
    result = search_database("Vanadium")
    print(result)
