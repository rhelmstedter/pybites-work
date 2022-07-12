import functools
from random import seed
from time import perf_counter

from rich.console import Console
from rich.table import Table
from rich.status import Status

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
        func(*args, **kwargs)
        toc = perf_counter()
        elapsed_time = round(toc - tic, 4)
        return elapsed_time

    return wrapper_timer


def comparison_runner(funcs: dict, trials: int, trial_params: dict) -> dict[float]:
    """Run the three functions with the same number of trials and stats.

    :funcs: dict Keys are a printable name, values are the function itself.
    :trials: int The number of trials to run.
    :trial_params: dict Contains school poplulation and probabilities of labels.
    """

    seed(1)
    comparison_results = {"Trials": trials}
    for i, (func_name, func) in enumerate(funcs.items()):
        func = timer(func)
        elapsed_time = func(trials, **trial_params)
        comparison_results[func_name] = elapsed_time
    return comparison_results


def display_table(comparison_results: list[dict]):
    console = Console()
    table = Table(title="Comparison Results (in seconds)")
    for column in comparison_results[0].keys():
        table.add_column(column, justify="center")

    for results in comparison_results:
        refactored_ratio = round(results["Original"] / results["Refactored"], 1)
        improved_ratio = round(results["Original"] / results["Improved"], 1)
        last_trial_width = len(str(trial_sets[-1]))
        longest_time_width = len(str(comparison_results[-1]["Original"]))
        table.add_row(
            f"{results['Trials']:{last_trial_width}d}",
            f"{results['Original']:0{longest_time_width}.4f}",
            f"{results['Refactored']:0{longest_time_width}.4f} [green]({refactored_ratio}x)[/green]",
            f"{results['Improved']:0{longest_time_width}.4f} [green]({improved_ratio}x)[/green]",
        )
    console.print(table)


if __name__ == "__main__":
    funcs = {
        "Original": original_run_trials,
        "Refactored": refactored_run_trials,
        "Improved": improved_run_trials,
    }
    trial_sets = [10**n for n in range(6)]
    trial_params = {
        "population": 600,
        "prob_sped": 0.166,
        "prob_low_ses": 0.35,
        "print_results": False,
    }
    comparison_results = []
    for trials in trial_sets:
        with Status(f"Running comparisons with {trials:,} trials..."):
            results = comparison_runner(funcs, trials, trial_params)
            comparison_results.append(results)
    display_table(comparison_results)
