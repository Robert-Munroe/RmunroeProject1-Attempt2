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


def test_get_excel():
    row_count = 36383
    list_of_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
                      'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Louisiana',
                      'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
                      'Montana', 'Nebraska', 'Nevada', 'New Hampshire', ' New Jersey', 'New Mexico', 'New York',
                      'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
                      'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia',
                      'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

    excel_state = []
    excel_occupation_title = []
    excel_total_employment = []
    excel_25th_percent = []
    excel_occupation_code = []
    excel_state, excel_occupation_title, excel_total_employment, excel_25th_percent, excel_occupation_code = \
        RmunroeAPIKey.get_data_excel(row_count)

    excel_state_stripped = []
    [excel_state_stripped.append(x) for x in excel_state if x not in excel_state_stripped]
    print(excel_state_stripped)

    all_states_found = False
    if excel_state_stripped == list_of_states:
        all_states_found = True
    assert all_states_found == True
