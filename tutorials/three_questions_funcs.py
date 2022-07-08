def welcome():
    print("Welcome traveler. I will ask you three questions. You must be sure of your answer.")
    input("When you are ready to begin press enter.")


def get_name():
    name = input("What is your name? ")
    print(f"It is nice to meet you {name}. That is a great name.")
    return name


def two_questions():
    color = input("What is your favorite color? ")
    print(f"{color.title()} is an interesting choice.")
    input("What is your quest? ")
    print("That is an admirable quest")


def goodbye(name):
    print("I hope to seen you again soon {name}.")


welcome()
traveler = get_name()
two_questions()
goodbye(traveler)
