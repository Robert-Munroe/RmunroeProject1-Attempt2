import RmunroeAPIKey


def test_get_data():
    results = RmunroeAPIKey.get_data()
    assert len(results) >= 100


def test_data_save():
    # first lets add test data
    conn, cursor = RmunroeAPIKey.open_db('testdb.sqlite')
    RmunroeAPIKey.setup_db(cursor)
    test_data = [{'school.name': 'Test University', '2018.student.size': 1000, 'school.state': 'MA', 'id': 11001,
                  '2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 456,
                  '2016.repayment.3_yr_repayment.overall': 4004}]
    RmunroeAPIKey.insert_data(test_data, cursor)
    RmunroeAPIKey.close_db(conn)
    # test data is saved - now lets see if it is there
    conn, cursor = RmunroeAPIKey.open_db('testdb.sqlite')
    # the sqlite_master table is a metadata table with information about all the tables in it
    cursor.execute('''SELECT name FROM sqlite_master
    WHERE type ='table' AND name LIKE 'university_%';''')  # like does pattern matching with % as the wildcard
    results = cursor.fetchall()
    assert len(results) == 1
    cursor.execute(''' SELECT university_name FROM university_data''')
    results = cursor.fetchall()
    test_record = results[0]
    assert test_record[0] == 'Test University'
