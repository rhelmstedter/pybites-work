import functools
from random import seed
from time import perf_counter

from rich import print

from original_func import run_trials as original_run_trials
from refactored import run_trials as refactored_run_trials
from improved import run_trials as improved_run_trials


def timer(func):
    """Timer decorator

    This wraps the main trial functions and returns the time elapsed in addition to the
    original return objects.
    """

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = perf_counter()
        value = func(*args, **kwargs)
        toc = perf_counter()
        elapsed_time = toc - tic
        print(f"Elapsed time for: {elapsed_time:0.4f} seconds")
        return elapsed_time, value

    return wrapper_timer


original_run_trials = timer(original_run_trials)
refactored_run_trials = timer(refactored_run_trials)
improved_run_trials = timer(improved_run_trials)

if __name__ == "__main__":
    seed(1)
    trials = 100_000
    print("Running function: [bold]original_run_trials[/bold]")
    original_time, original_results = original_run_trials(trials)

    print("Running function: [bold]refactored_run_trials[/bold]")
    refactored_time, refactored_results = refactored_run_trials(
        trials, 600, 0.166, 0.35
    )
    print("Running function: [bold]improved_run_trials[/bold]")
    improved_time, improved_results = improved_run_trials(
        trials, 600, 0.166, 0.35
    )
