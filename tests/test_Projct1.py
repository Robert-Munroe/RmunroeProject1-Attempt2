import RmunroeAPIKey


def test_get_data():
    results = RmunroeAPIKey.get_data()
    assert len(results) >= 100


def test_pop_database():
    data = "test data"
    conn, cursor = RmunroeAPIKey.open_db("test_database.sqlite")
    print(type(conn))
    RmunroeAPIKey.setup_db(cursor)

    RmunroeAPIKey.insert_data(cursor, data)

    data_in_table = RmunroeAPIKey.select_data(cursor, data)
    RmunroeAPIKey.close_db(conn)

    assert data_in_table == data
