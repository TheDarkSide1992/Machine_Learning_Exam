import psycopg2
from exam_agent.config import DATABASE as DBCONFIG


def search_database(search: str):
    connection = psycopg2.connect(database=DBCONFIG["database"], user=DBCONFIG["user"], password=DBCONFIG["password"],
                                  host=DBCONFIG["host"], port=DBCONFIG["port"])

    cursor = connection.cursor()

    query = f"""SELECT
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
                FROM "COMPONENT"
                JOIN "STUDY" ON "COMPONENT".sub_com_id = "STUDY".study_id
                JOIN "CHEM_ASSESS" ON "STUDY".hazard_id = "CHEM_ASSESS".hazard_id
                WHERE comparamname LIKE '%{search}%';"""

    # TODO Replace Table and * with relevant information once actual schema is nown
    cursor.execute(query=query)

    record = cursor.fetchall()

    return record


if __name__ == "__main__":
    result = search_database("Vanadium")
    print(result)
