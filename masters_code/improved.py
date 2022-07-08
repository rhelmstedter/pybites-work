from collections import Counter
from random import choices, seed

from rich.progress import track


def _create_trial_shool(
    population: int, prob_sped: float, prob_low_ses: float
) -> Counter:
    """Creates a counter of students with one of four possible labels: 'sped low',
    'sped high', 'gen_ed low' 'gen_ed high'.

    :population: int The number of students in the school.
    :prob_sped: float The probability that a student is labeled as sped.
    :prob_low_ses: float The probability that a student labeled as low ses.
    :returns: Counter The number of students with each label.
    """

    prob_gen_ed = 1 - prob_sped
    prob_high_ses = 1 - prob_low_ses
    labels = ["sped low", "sped high", "gen_ed low", "gen_ed high"]
    probabilities = [
        round(prob_sped * prob_low_ses, 3),
        round(prob_sped * prob_high_ses, 3),
        round(prob_gen_ed * prob_low_ses, 3),
        round(prob_gen_ed * prob_high_ses, 3),
    ]
    school = Counter(choices(population=labels, weights=probabilities, k=population))
    return school


def _update_pr_counts(
    pr_counter: Counter,
    percent_low_ses_overall: float,
    percent_low_ses_in_sped: float,
) -> None:
    """Upates the number of schools that have proportional representation.

    :pr_counter: Counter The proportional representation counter to be updated.
    :percent_low_ses_overall: float The percentage of students at the school who are
        labeled low income.
    :percent_low_ses_in_sped: float The percentage of students who are labeled both as
        low income and sped.
    :returns: Counter The proportional representation counter updated if the school has
        proportional representation.
    """

    if percent_low_ses_overall == percent_low_ses_in_sped:
        pr_counter.update(["exact"])
    if 0 <= percent_low_ses_overall - percent_low_ses_in_sped <= 0.02:
        pr_counter.update(["within range"])
    return pr_counter


def run_trials(
    trials: int,
    population: int,
    prob_sped: float,
    prob_low_ses: float,
    print_results: bool = True,
) -> dict[str, float]:
    """Run the trials to simulate a school with a given probabilities of students being
    labeled sped and low ses.

    :trials: int The number of trials to run.
    :population: int The number of students at the school.
    :prob_sped: float The probability that a student is labeled as sped.
    :prob_low_ses: float The probability that a student is labeled as low ses.
    :returns: dict Contains the percentages of schools that have proportional
        representation across all trials.
    """
    proportional_representation = Counter()
    for i in track(range(trials), f"With {trials:,} trials"):
        school = _create_trial_shool(population, prob_sped, prob_low_ses)
        count_sped = school["sped low"] + school["sped high"]
        count_low_ses = school["sped low"] + school["gen_ed low"]
        proportional_representation = _update_pr_counts(
            proportional_representation,
            percent_low_ses_overall=round(count_low_ses / population, 3),
            percent_low_ses_in_sped=round(school["sped low"] / count_sped, 3),
        )
    results = {
        pr: round(count / trials * 100, 2)
        for pr, count in proportional_representation.items()
    }
    if print_results:
        print(
            f"The probability of having exact proportional representation in {trials:,} trials is: {results.get('exact', 0.0)}%"
        )
        print(
            f"The probability of being within 2% in {trials:,} trials is: {results.get('within range', 0.0)}%"
        )
    return results


if __name__ == "__main__":
    seed(1)
    trials = 10000
    results = run_trials(trials, 600, 0.166, 0.35)
