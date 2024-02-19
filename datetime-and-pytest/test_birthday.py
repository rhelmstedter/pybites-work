import datetime
from unittest.mock import patch

from birthday import build_birthday, calc_days_till_next_bd


def test_build_bd():
    with patch("builtins.input", side_effect=["2000", "01", "02"]):
        actual = build_birthday()
        assert isinstance(actual, datetime.datetime)
        assert actual == datetime.datetime(2000, 1, 2)


def test_bd_hasnt_happened():
    today = datetime.datetime(2024, 1, 10)
    birthday = datetime.datetime(2000, 1, 13)
    actual = calc_days_till_next_bd(today, birthday)
    assert actual == 3


def test_bd_has_happend():
    today = datetime.datetime(2024, 1, 13)
    birthday = datetime.datetime(2000, 1, 10)
    actual = calc_days_till_next_bd(today, birthday)
    assert actual == 363
