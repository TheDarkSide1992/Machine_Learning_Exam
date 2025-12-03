import psycopg2
from typing import TypedDict, Optional
from exam_agent.config import DATABASE as DBCONFIG


class ToxicEntry(TypedDict):
    name: str
    ec_number: Optional[str]
    cas_number: Optional[str]
    description: Optional[str]
    display_name: str
    substance_type: str
    form: str
    common_name: str
    iupac_name: Optional[str]
    label: str
    formula: Optional[str]
    additional1: Optional[str]
    additional2: Optional[str]
    category: str
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    group: str
    assessment: Optional[str]
    tox_eval: Optional[str]
    safety_eval: Optional[str]
    context: Optional[str]
    unit: Optional[str]
    unit_description: Optional[str]
    unit_alt: Optional[str]
    extra: Optional[str]
    notes: Optional[str]
    conclusion: Optional[str]


def search_database(search: str):
    global dict

    _rows = """
                sub_name,
                sub_ecsubinvententryref,
                sub_casnumber,
                sub_description,
                subparamname,
                sub_type,
                qualifier,
                com_name,
                iupacname,
                comparamname,
                molecularformula,
                smilesnotation,
                inchi,
                com_type,
                com_structureshown,
                smilesnotationsource,
                inchi_notationsource,
                sub_op_class,
                is_mutagenic,
                is_genotoxic,
                is_carcinogenic,
                remarks_study,
                riskunit,
                riskunitfulltext,
                riskunit_milli,
                safety_factor,
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

    return dict


if __name__ == "__main__":
    result = search_database("Vanadium")
    print(result)
