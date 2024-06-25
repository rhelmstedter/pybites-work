import simple_calculator


def test_add():
    actual = simple_calculator.add(3, 7)
    expected = 10
    assert actual == expected


def test_subtract():
    actual = simple_calculator.subtract(10, 7)
    expected = 3
    assert actual == expected
