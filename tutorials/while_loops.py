import random

jokes = {
    "Why'd the fisherman order the halibut?": "Just for the halibut!",
    "Why is Peter Pan always flying?": "Because he Neverlands.",
    "What do you call a sleeping bull?": "A bulldozer.",
    "How do you throw a party in outer space?": "You planet.",
    "Why was the broom late to class?": "It over-swept.",
    "How do you make an octopus laugh?": "With ten-tickles!",
    "What do you say to a rabbit on its birthday?": "Hoppy Birthday!",
    "What type of tree fits in your hand?": "A palm tree.",
    "Why couldn't the bicycle stand up by itself?": "It was two tired!",
    "Wanna hear a joke about construction?": "I'm still workin' on it!",
    "What do you call a fake noodle?": "An impasta.",
    "How does a lawyer say goodbye?": "I'll be suing ya!",
    "What made the tomato blush?": "It saw the salad dressing.",
    "Can I dive in this pool?": "It deep-ends.",
    "What did the buffalo say to its son when he left?": "Bison!",
    "Why do vampires always seem sick?": "They're coffin.",
    "What musical instrument do you find in the bathroom?": "A tuba toothpaste!",
    "Which state has the most streets?": "Rhode Island.",
    "How do astronomers organize a party?": "They planet.",
    "Why do bees have sticky hair?": "Because they use a honeycomb.",
    "Why do melons have weddings?": "They cantaloupe!",
    "What did the police officer say to her belly button?": "You're under a vest!",
    "What do you call a fibbing cat?": "A lion.",
    "What does a nosey pepper do?": "It gets jalapeño business.",
}

while True:
    print("Want to hear a joke?")
    ask_for_joke = input("Enter [y] or [n]:").lower()
    if ask_for_joke == "y":
        setup = random.choice(list(jokes.keys()))
        punchline = jokes[setup]
        print("Press enter for punchline")
        input(setup)
        print(punchline)
    elif ask_for_joke == "n":
        print("OK, bye")
        break
    else:
        print("I don't understand. Enter [y] or [n]")
