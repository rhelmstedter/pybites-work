import datetime
from pprint import pprint


def build_birthday() -> datetime.datetime:
    """Build a datetime object for the user's birthday."""
    while True:
        year = int(input("What year were you born? "))
        month = int(input("What month were you born? "))
        day = int(input("What day were you born? "))
        return datetime.datetime(year, month, day)


def calc_days_till_next_bd(
    today: datetime.datetime,
    birthday: datetime.datetime,
) -> int:
    """Calculate the number of days between today and birthday."""
    if (
        today.month == birthday.month and today.day > birthday.day
        or today.month > birthday.month
    ):
        next_birthday = datetime.datetime(
            today.year + 1,
            birthday.month,
            birthday.day,
        )
    else:
        next_birthday = datetime.datetime(
            today.year,
            birthday.month,
            birthday.day,
        )
    return (next_birthday - today).days


def create_bd_paragraph(birthday: datetime.datetime) -> str:
    """Create a paragraph about the user's birthday that includes days, age, and days until their next birthday."""
    today = datetime.datetime.today()
    days = (today - birthday).days
    age = days // 365
    days_till_next_bd = calc_days_till_next_bd(today, birthday)
    return f"""You were born on {birthday:%B %d, %Y}. It was a {birthday:%A}. You have been alive for {days:,} days and are {age} years old. There are {days_till_next_bd} days until your next birthday."""


if __name__ == "__main__":
    birthday = build_birthday()
    paragraph = create_bd_paragraph(birthday)
    print(paragraph)

pprint(globals())
