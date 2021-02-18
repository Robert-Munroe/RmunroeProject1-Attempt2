import requests
import Secrets
import sqlite3
from typing import Tuple


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


def setup_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS Schools_Database(
    school_data BLOB
    );''')


def insert_data(cursor: sqlite3.Cursor, data):
    for i in range(len(data)):
        school_data = data[i]
        school_data = list_to_string(school_data)
        cursor.execute("INSERT INTO Schools_Database VALUES (:school_data)", {'school_data': school_data})


def list_to_string(string):
    str1 = ""
    for ele in string:
        str1 += ele
    return str1


def get_data():
    all_data = []

    for page in range(1):
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

    conn, cursor = open_db("Schools_Database.sqlite")
    print(type(conn))

    setup_db(cursor)
    insert_data(cursor, get_data())
    close_db(conn)


if __name__ == '__main__':
    main()
