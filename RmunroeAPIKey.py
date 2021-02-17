import requests
import sqlite3
from typing import Tuple
import Secrets


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)                           #connect to existing DB or create new one
    cursor = db_connection.cursor()                                     #get ready to read/write data
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()                                                 #make sure any changes get saved
    connection.close()


def get_data():
    all_data = []

    for page in range(5):
        response = requests.get(f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_"
                                f"awarded.predominant=2,3"
                                f"&fields=school.name,school.city,school.state,2018.student.size,2017.student.size,"
                                f"2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,"
                                f"2016.repayment.3_yr_repayment.overall&api_key={Secrets.api_key}&page={page}")
        if response.status_code != 200:
            print("error getting data!")
            exit(-1)
        page_of_data = response.json()
        page_of_school_data = page_of_data['results']
        all_data.extend(page_of_school_data)
    return all_data


def main():

    conn, cursor = open_db("demo_db.sqlite")
    print(type(conn))
    close_db(conn)

    f = open("School_Data.txt", "w")
    final_data = ' '.join([str(elem) for elem in get_data()])
    f.write(final_data)

    f.close()
    f = open("School_Data.txt", "r")
    print(f.read())
    f.close()


if __name__ == '__main__':
    main()
