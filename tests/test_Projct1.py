import RmunroeAPIKey


def test_get_data():
    results = RmunroeAPIKey.get_data()
    assert len(results) >= 1000
