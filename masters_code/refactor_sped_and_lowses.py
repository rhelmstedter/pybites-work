from decimal import Decimal, InvalidOperation
from random import choices
from collections import Counter
from rich.progress import track


INVALID_PROBABILITY = "Please enter a valid decimal less than one."


def main() -> None:
    population, probabilities = get_school_stats()
    runs, exact, within_two_percent = run_trials(population, probabilities)
    print(
        f"""The probability of having an exact proportional representation
        of low SES students in SPED in {runs} trials is: {results.get('exact', 0.00)}%"""
    )
    print(
        f"""The probability of having proportional representation
        within two percent in {runs} trials is: {results.get('two percent', 0.00)}%"""
    )


def _validate_probs(prompt: str) -> Decimal:
    while True:
        try:
            probability = Decimal(input(prompt))
        except InvalidOperation:
            print(INVALID_PROBABILITY)
        if probability >= 1:
            print(INVALID_PROBABILITY)
            continue
        break
    return probability


def _validate_int(prompt: str) -> int:
    while True:
        try:
            integer = int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")
            continue
        break
    return integer


def get_school_stats() -> tuple[Decimal, tuple]:
    prompts = (
        "How many students are in the school?\n> ",
        "What percentage of the school is labeled as SPED? (As a decimal.)\n> ",
        "What percentage of the school is labeled as Low Socio-Econoimc Status? (As a decimal.)\n> ",
    )
    population = _validate_int(prompts[0])
    sped = _validate_probs(prompts[1])
    low_ses = _validate_probs(prompts[2])
    both = sped * low_ses
    neither = 1 - (sped + low_ses + both)
    return Decimal(population), (sped, low_ses, both, neither)


def create_trial_school(population: Decimal, probabilities: tuple[Decimal]) -> Counter:
    return Counter(
        choices(
            population=["sped", "low_ses", "both", "neither"],
            weights=[float(p) for p in probabilities],
            k=int(population),
        )
    )


def run_trials(population: Decimal, probabilities: tuple) -> tuple[int, dict]:
    runs = _validate_int("How many trials do you want to run?\n> ")
    schools_with_pr = Counter()
    for _ in track(range(runs), description="Running Trials..."):
        school = create_trial_school(population, probabilities)
        simulated_sped = Decimal(school["sped"] + school["both"])
        simulated_low_ses = Decimal(school["low_ses"] + school["both"])
        percent_low_ses = round(simulated_low_ses / population, 3)
        percent_low_ses_in_sped = round(Decimal(school["both"]) / simulated_sped, 3)

        print(f"{school=}")
        if percent_low_ses == percent_low_ses_in_sped:
            schools_with_pr.update(["exact"])
        elif 0 < abs(percent_low_ses - percent_low_ses_in_sped) <= 0.05:
            schools_with_pr.update(["with range"])
    results = {
        pr: round(Decimal(count) / runs * 100, 2)
        for pr, count in schools_with_pr.items()
    }
    return runs, results


if __name__ == "__main__":
    sped = Decimal(0.333)
    low_ses = Decimal(0.75)
    both = sped * low_ses
    print(both)
    neither = 1 - (sped + low_ses + both)
    runs, results = run_trials(Decimal(600), (sped, low_ses, both, neither))
    print(
        f"""The probability of having an exact proportional representation
        of low SES students in SPED in {runs} trials is: {results.get('exact', 0.00)}%"""
    )
    print(
        f"""The probability of having proportional representation
        within two percent in {runs} trials is: {results.get('with range', 0.00)}%"""
    )
