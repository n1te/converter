from json import dumps
from config import Config


class TestConfig(Config):
    fixerio_api_key = 'test_api_key'
    symbols = ['ONE', 'TWO']


config = TestConfig()


def mock_fixerio_responce(mocked):
    """
    Mocking correct server response
    """
    body = dumps({
        "success": True,
        "timestamp": 1525872307,
        "base": "EUR",
        "date": "2018-05-09",
        "rates": {
            "ONE": 5,
            "TWO": 100
        }
    })
    mocked.get('http://data.fixer.io/api/latest?symbols=ONE,TWO&access_key=test_api_key', status=200, body=body)

    body = dumps({
        "success": True,
        "symbols": {
            "EUR": "Euro",
            "ONE": "One",
            "TWO": "Two"
        }
    })
    mocked.get('http://data.fixer.io/api/symbols?access_key=test_api_key', status=200, body=body)
