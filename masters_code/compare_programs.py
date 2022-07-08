import functools
from collections import Counter
from random import choices, seed
from time import perf_counter

import numpy as np
from rich.progress import track


def timer(func):
    """Timer decorator

    This wraps the main trial functions and returns the time elapsed in addition to the
    original return objects.
    """

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = perf_counter()
        print(f"Running {func.__name__}")
        value = func(*args, **kwargs)
        toc = perf_counter()
        elapsed_time = toc - tic
        print(f"Elapsed time for: {elapsed_time:0.4f} seconds")
        return elapsed_time, value

    return wrapper_timer


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

    school = Counter()
    for s in range(population):
        student = (
            choices(
                population=["sped ", "gen_ed "],
                weights=[prob_sped, 1 - prob_sped],
            )[0]
            + choices(
                population=["low", "high"],
                weights=[prob_low_ses, 1 - prob_low_ses],
            )[0]
        )
        school.update([student])
    return school


def _update_pr_counts(
    pr_counter: Counter,
    percent_low_ses_overall: float,
    percent_low_ses_in_sped: float,
) -> None:
    """Upates the number of schools that have proportional representation.

    :pr_counter: Counter The proportional representation counter to be updated.
    :percent_low_ses_overal: float The percentage of students at the school who are
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


@timer
def refactored_run_trials(
    trials: int,
    population: int,
    prob_sped: float,
    prob_low_ses: float,
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
    for i in track(range(trials), f"Running {trials:,} trials"):
        school = _create_trial_shool(population, prob_sped, prob_low_ses)
        count_sped = school["sped low"] + school["sped high"]
        count_low_ses = school["sped low"] + school["gen_ed low"]
        proportional_representation = _update_pr_counts(
            proportional_representation,
            percent_low_ses_overall=round(count_low_ses / population, 3),
            percent_low_ses_in_sped=round(school["sped low"] / count_sped, 3),
        )
    return {
        pr: round(count / trials * 100, 2)
        for pr, count in proportional_representation.items()
    }


@timer
def original_run_trials(trials):
    """Original version of of script"""
    np.random.seed(1)
    n = 1
    p_sped = 1 / 6
    p_lowin = 7 / 20
    runs = trials
    pop = 600
    PR_exact = 0
    PR_twoper = 0

    for i in track(range(runs), f"With {trials:,} trials"):
        sped = 0
        lowin = 0
        both = 0
        sample_school = []
        for s in range(pop):
            student = str(np.random.binomial(n, p_sped)) + str(
                np.random.binomial(n, p_lowin)
            )
            if int(student) == 10:
                sped += 1
            elif int(student) == 1:
                lowin += 1
            elif int(student) == 11:
                both += 1
            sample_school.append(student)
        per_lowsped = both / (sped + both)
        per_lowpop = (lowin + both) / (pop)
        if 0 < (per_lowsped - per_lowpop) <= 0.02:
            PR_twoper += 1
        elif per_lowsped == per_lowpop:
            PR_exact += 1
    return (PR_exact / runs) * 100, (PR_twoper / runs) * 100


if __name__ == "__main__":
    seed(1)
    trials = 1_00
    original_time, original_results = original_run_trials(trials)
    print(
        f"The probability of having exact proportional representation in {trials:,} trials is: {original_results[0]}%"
    )
    print(
        f"The probability of being within 2% in {trials:,} trials is: {original_results[1]}%"
    )

    refactored_time, refactored_results = refactored_run_trials(
        trials, 600, 0.1666, 0.35
    )
    print(
        f"The probability of having exact proportional representation in {trials:,} trials is: {refactored_results.get('exact', 0.0)}%"
    )
    print(
        f"The probability of being within 2% in {trials:,} trials is: {refactored_results.get('within range', 0.0)}%"
    )
    print(f"This is a test of the elapsed time @ {refactored_time:.04f}")
