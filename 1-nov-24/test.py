from logs import (
    count_actions,
    get_unique_users,
    filter_by_status,
    get_unique_ips,
    most_frequent_user
)

def test_count_actions():
    logs = [
        {"action": "login"},
        {"action": "login"},
        {"action": "logout"},
    ]
    result = count_actions(logs)
    assert result == {"login": 2, "logout": 1}


def test_get_unique_users():
    logs = [
        {"user": "ana"},
        {"user": "luis"},
        {"user": "ana"},
    ]
    result = get_unique_users(logs)
    assert result == {"ana", "luis"}


def test_filter_by_status():
    logs = [
        {"user": "ana", "status": 200},
        {"user": "luis", "status": 404},
        {"user": "ana", "status": 401},
    ]
    result = filter_by_status(logs)
    assert result == {"luis", "ana"}


def test_get_unique_ips():
    logs = [
        {"ip": "1.1.1.1"},
        {"ip": "2.2.2.2"},
        {"ip": "1.1.1.1"},
    ]
    result = get_unique_ips(logs)
    assert result == {"1.1.1.1", "2.2.2.2"}


def test_most_frequent_user():
    logs = [
        {"user": "ana"},
        {"user": "luis"},
        {"user": "ana"},
        {"user": "maria"},
    ]
    result = most_frequent_user(logs)
    assert result == "ana"


def run_all_tests():
    print("Running tests...")

    test_count_actions()
    print("test_count_actions OK")

    test_get_unique_users()
    print("test_get_unique_users OK")

    test_filter_by_status()
    print("test_filter_by_status OK")

    test_get_unique_ips()
    print("test_get_unique_ips OK")

    test_most_frequent_user()
    print("test_most_frequent_user OK")

    print("\nAll tests passed successfully")


if __name__ == "__main__":
    run_all_tests()
