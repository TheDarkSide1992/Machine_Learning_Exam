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
    remarks: str
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

    records = cursor.fetchall()

    """"
    data_out = list([
        (map(lambda x: {
            "sub_name": x[0],
            "sub_description": x[1],
            "molecularformula": x[2],
            "com_type": x[3],
            "sub_op_class": x[4],
            "is_mutagenic": x[5],
            "is_genotoxic": x[6],
            "is_carcinogenic": x[7],
            "remarks_study": x[8],
            "riskunit": x[9],
            "remarks": x[10],
            "assess": x[11],
        }, record)) for record in records
    ])"""


    data_out:list = [ToxicEntry]
    for record in records:
        data_out.append({"sub_name": record[0],
            "sub_description": record[1],
            "molecularformula": record[2],
            "com_type": record[3],
            "sub_op_class": record[4],
            "is_mutagenic": record[5],
            "is_genotoxic": record[6],
            "is_carcinogenic": record[7],
            "remarks_study": record[8],
            "riskunit": record[9],
            "remarks": record[10],
            "assess": record[11],
            })

    return data_out


if __name__ == "__main__":
    result = search_database("Vanadium")
    print(result)
