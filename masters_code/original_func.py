import numpy as np


def run_trials(trials: int, population: int, prob_sped: float, prob_low_ses: float, print_results: bool = True):
    """Original version of of script"""
    np.random.seed(1)
    n = 1
    p_sped = prob_sped
    p_lowin = prob_low_ses
    runs = trials
    pop = 600
    PR_exact = 0
    PR_twoper = 0

    for i in range(runs):
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
        results = (PR_exact / runs) * 100, (PR_twoper / runs) * 100
    if print_results:
        print(
            f"The probability of having exact proportional representation in {trials:,} trials is: {results[0]}%"
        )
        print(
            f"The probability of being within 2% in {trials:,} trials is: {results[1]}%"
        )
    return results


if __name__ == "__main__":
    trials = 10000
    results = run_trials(trials, 0.166, 0.35)
