# Progress

 I have learned a lot over the past 2.5 years of my python journey. What started out as a hobby during covid-19 lock downs in 2020, has now become a major component of my professional workload. This article is designed to highlight the importance of the iterative process: write some code -> learn new stuff -> review some code -> refactor. I will share some code I wrote in May 2020 (approximately two months into learning python), my thought process at the time, how I decided to refactor it, and finally a performance comparison of the programs. One big factor that I will not mention in this particular article is testing. Yes, I should have had some tests to run against my refactored code to ensure I was not wandering off course. However, this code was made to be used by only me and not in production. I mean, when I first wrote the code, I didn't even know what tests were. Instead, I will focus design decisions and the surprising, if not incidental, performance impacts.
 

## Background

I recently earned a master's degree in Curriculum and Instruction. One class in the program was centered on a text that I had strong opinions about. I interpreted the text as blaming educators and didn't appreciate it at all. So the thesis of one of my papers ([Specious Solutions](https://github.com/rhelmstedter/pybites-work/blob/main/masters_code/assests/specious_solutions.pdf) if you are interested in reading the whole thing) focused on dismantling their argument on proportional representation (PR). In schools, at least here in California, US, we have different categories for students. For example, if a student needs extra academic or emotional support or have some kind of disability, they can receive special education services and are subsequently categorized as Special Education (SPED). If students come from poor families as indexed by federal standards they are categorized as low Socio-Economic Status (SES). Assuming that you didn't go read the linked paper, here is part of the argument that got me so worked up:

>Because proportional representation anchors the equity audit (as discussed above), the equity audit form requires that data collection include fractions along with percentages to be able to measure proportional representation. For example, of 100 students labeled with disabilities, if 70 of these students receive free and reduced-priced lunch, then the fraction for this data is 70/100 and the percent is 70%. This data can then be compared to the percent of students in the school who are receiving free and reduced-price lunch, which in this example is 210 students out of 600 (210/600 = 35%). Thus, in this example, at this school, we know that students from low-income homes are twice as likely to be labeled for special education, and thus are over-represented in special education. Proportional representation of students from low-income homes in special education should be 35% or less.

Without getting too far into the weeds (if you enjoy getting into the weeds, go read the paper), their argument assumes that SPED and low SES are independent, and randomly distributed across the population. But even if that were the case—and I cite evidence in the paper that is most likely not the case—I was not convinced that PR would be likely to occur naturally. Given that, at that time, I had been learning python for a few months, I decided to create a simulation.

## Original ~~Sin~~ Code

My idea was to simulate a school by randomly label students as SPED or Low SES using the given probabilities from the text. The program would then count how many students were labeled as SPED, low SES, or both, calculate the portion of low SES students overall and of low SES students in SPED, and finally, if the portions matched precisely, the school would have PR. Repeat this process for a large number of trials and see how often it would actually happen. One more detail before we get to the code, though the text claims that PR for low SES students in SPED should be 35% or less, this is the first flaw of their argument. If low SES students are _under_ represented in SPED that must be accompanied by an _over_ representation of another population. Still, I cut them some slack and gave them a 2% buffer.


I must warn you, the code you are about to see is painful. I didn't really know how to accomplish the simulation, but I did know that I could generate random numbers with python. So I start googling something along the lines of "choosing random numbers based on a probability". Somewhere across the internet I stumbled on [numpy.random.binomial](https://numpy.org/doc/stable/reference/random/generated/numpy.random.binomial.html). This returned either 0 or 1 based on the probability of the label. I ran this twice with the probability for sped and low SES respectively, converted them to a string so I could concatenated them. Converting them back to `ints`,  10 represented a student being labeled as SPED, 1 represented a student being labeled as low SES, and 11 was labeled both. (Why didn't I just compare the strings? I'm not sure. Maybe at the time I thought I could only compare numerical values? I don't really remember.) Here is my original script in all its glory:

```python
import numpy as np
import random

n = 1
p_sped = (1/6)
p_lowin = (7/20)

runs = 10000
pop = 600

PR_exact = 0
PR_twoper = 0
for i in range(runs):
    sped = 0
    lowin = 0
    both = 0
    sample_school = []
    for s in range(pop):
        student = str(np.random.binomial(n,p_sped)) + str(np.random.binomial(n,p_lowin))
        if int(student) == 10:
            sped += 1
        elif int(student) == 1:
            lowin += 1
        elif int(student) == 11:
            both += 1
        sample_school.append(student)
    per_lowsped = both/(sped + both)
    per_lowpop = (lowin+both)/(pop)
    if 0<(per_lowsped-per_lowpop)<= 0.02:
        PR_twoper += 1
    elif per_lowsped==per_lowpop:
        PR_exact +=1

prob_PR_exact = (PR_exact/runs)*100
prob_PR_twoper = (PR_twoper/runs)*100
print('The probability of having exact proportional representation in ' +str(runs) + ' trials is: '
      + str(prob_PR_exact) + '%')
print('The probability of having proportional representation within 2% in ' +str(runs) + ' trials is: '
      + str(prob_PR_twoper) + '%')
```

I know, I know... It is rough. Reading this code in the last week or so, I can not believe I had included it in my final paper. Let's identify some issues:

+ **formatting**: super difficult to read. I clearly had not heard of [black](https://pypi.org/project/black/).
+ **naming variables**: objectively terrible. C'mon man, I wrote this and still struggled with `PR_twoper`. I had forgotten what much of stood for until I went back and read the paper.
+ **unused imports**: why was I importing random, I didn't even use it?
+ **inefficient**: I am using numpy (which is supposed to be super fast!), but then converting to a string because I needed to get two labels and then converting it back to an integer for the conditionals. I am also created a sample school, appending students to it, but then I never use it. What?!?
+ **inaccurate**: I wasn't aware how inaccurate floats could be I didn't include any kind of rounding. Also, during the refactoring process I realized I should have included the exact proportional representation in the "within 2%" calculation as well. This is a small difference and doesn't change the analysis of the paper, but still important.

If for some reason—unfathomable to the average human mind—you want to work with this code it is available in [the repo](https://github.com/rhelmstedter/pybites-work/blob/main/masters_code/original.py). 


## Refactoring

In this section I will describe my thought process in refactoring the original code into something that is more readable. My goal was to abstract chunks of code that were responsible for specific behavior into functions. I did not try to come up with all the functions at once and the ended code that I am sharing with you happened incrementally. Step one I ran my code against black. While this alone made it easier to read ([don't want to miss the gorilla](https://youtu.be/wf-BqAjZb8M?t=661)), I knew that wasn't the biggest problem. I knew I needed to have better variable names, but decided to let that happen organically as I created the functions. As an added bonus, abstracting behavior into functions lets me add [docstrings](https://peps.python.org/pep-0257/) and [type hints](https://docs.python.org/3/library/typing.html). This way when I try to review this again in the future, I will know what past me was thinking.

### Creating a School

The first consequential issue that jumped out at me was the nested `for` loops. Starting with the inner loop, I tried to describing in simple plain language what was happening. _I was creating a school and counting the numbers of students with each label_. This lead to the helper function `_create_trial_school()`.

```python
def _create_trial_school(
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
```

Current me now knows that [counters]() exist, so I used a counter instead of counting manually with `if/else` statements. Next, I needed to address that awful use of `numpy.random.binomial()`. Again, utilizing my favorite tool ever, googling until I find an answer (sure I use duck duck go, but doesn't everyone just calling it googling?), I searched for an alternative. I settled on `random.choices()`. This lets me assign a probability and choose from a list of strings. I can get rid of the embarrassing `int` -> `str` -> `int` conversions. (Honestly, I would appreciate it if we never spoke of that again. Not my proudest moment. Thanks in advance.) So now I run `random.choices()` twice, once for SPED and once for SES. Since I am using strings, I need labels for the [compliments](https://en.wikipedia.org/wiki/Complementary_event) of my labels as well. The compliment of SPED is general education (gen_ed) and the compliment of low SES is high SES (high). I concatenated the randomly choosen labels resulting in four possibilities `["sped low", "sped high", "gen_ed low", "gen_ed high"]`. The school counter is updated with each student and returned by the function. The difference between the original and refactored code is shown below. I am using the ellipse to show that there is code above and below the snippets.

```python
# This original code
...
    sped = 0
    lowin = 0
    both = 0
    sample_school = []
    for s in range(pop):
        student = str(np.random.binomial(n,p_sped)) + str(np.random.binomial(n,p_lowin))
        if int(student) == 10:
            sped += 1
        elif int(student) == 1:
            lowin += 1
        elif int(student) == 11:
            both += 1
        sample_school.append(student)
...

# Becomes this refactored code
...
    school = _create_trial_school(population, prob_sped, prob_low_ses)
...
```

### Counting Proportional Representation

Up next, another counter! I realized that I am again counting how many of my newly created trial schools actually have proportional representation. However, I need this counter to persist across schools. So I create a `Counter()` outside of the first for loop of my original code and then create the helper function `_update_pr_counts()`.

```python
def _update_pr_counts(
    pr_counter: Counter,
    percent_low_ses_overall: float,
    percent_low_ses_in_sped: float,
) -> None:
    """Updates the number of schools that have proportional representation.

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
```
This fixes my inaccuracies of not including exact PR in the 2% range, and uses more clear variable names. Having `_create_trial_school()` return a counter slightly changes how I count and calculate the portion of low SES students in SPED, and low SES overall. I split it into two parts. Just calculate the counts and then pass the portion directly as part of the next function.

```python
# This original code
...
for i in range(runs):
    ...
    per_lowsped = both / (sped + both)
    per_lowpop = (lowin + both) / (pop)
    if 0 < (per_lowsped - per_lowpop) <= 0.02:
        PR_twoper += 1
    elif per_lowsped == per_lowpop:
	   PR_exact += 1
...

# Becomes this refactored code
...
    proportional_representation = Counter()
    for _ in range(trials):
	   ...
        count_sped = school["sped low"] + school["sped high"]
        count_low_ses = school["sped low"] + school["gen_ed low"]
        proportional_representation = _update_pr_counts(
            proportional_representation,
            percent_low_ses_overall=round(count_low_ses / population, 3),
            percent_low_ses_in_sped=round(school["sped low"] / count_sped, 3),
        )
...
```

### Calculating and Printing Results

The last item I needed to address is how the results are calculated. Since I now had a counter for PR, I went with a [dictionary comprehension](https://peps.python.org/pep-0274/) to convert the counts to percents. Apparently, past me had not yet learned about [f-strings](https://peps.python.org/pep-0498/) either so I cleaned up the print statements as well. Finally, you'll notice a little if statement. This is a flag that lets me decide if I was to to print the results or not. This is for when I compare the performance later. When the number of trials is small, it is possible to have no schools with PR so I used the dict method `.get()` to provide a default value.

```python
# This original code
...
prob_PR_exact = (PR_exact/runs)*100
prob_PR_twoper = (PR_twoper/runs)*100
print('The probability of having exact proportional representation in ' +str(runs) + ' trials is: '
      + str(prob_PR_exact) + '%')
print('The probability of having proportional representation within 2% in ' +str(runs) + ' trials is: '
      + str(prob_PR_twoper) + '%')
...

# Becomes this refactored code
...
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
...
```

# Putting it All Together

I decided that I should abstract the entire simulation into a function called `run_trials()`. This allows me to run the trials utilizing the [if __name__ == "__main__":](https://docs.python.org/3/library/__main__.html) idiom. I believe the resulting refactoring makes it easier to follow what is happening in the simulation, is much better documented, and makes it simpler to run simulations with different parameters.
```python

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
    for _ in range(trials):
        school = _create_trial_school(population, prob_sped, prob_low_ses)
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
```

The entirety of the [refactored code](https://github.com/rhelmstedter/pybites-work/blob/main/masters_code/refactored.py) can be found in the github repo.

### Improving The Code Even Further

There was still something that bothered me about the refactoring. I was really unhappy with `_create_trial_school()`. I didn't like that `random.choices()` returned a list so I had to get the item out of the list then concatenate the labels together. It would be so much easier if I could just call choices once with the appropriate probabilities for each label. And after during some more digging (and actually reading the friendly manual) I saw that `random.choices()` actually has a `k` argument and returns "[a k sized list of elements chosen from the population with replacement](https://docs.python.org/3/library/random.html#random.choices)". That means I could label the entire student population in one fell swoop. But how to calculate the correct probabilities. I no longer had a coding problem, I had a math problem.

I thought and thought. I wrote some code that resulted in that 200% of low SES being in SPED (I really don't want to talk about it). I emailed a colleague asking about probability and he (very politely) informed me I was COMPLETELY wrong. And then I finally, begrudgingly did what I also ask of my students. Draw a picture.

OK, I know that the entire student body is the whole (100%). My problem is two-dimensional: SPED and SES so I need a rectangle. The probability of being labeled SPED is 7/20, which means the probability of being general ed is 13/20. The second dimension is a probability of being low SES (1/6) and high SES (5/6). This leads to the picture:

![probability rectangle](https://raw.githubusercontent.com/rhelmstedter/pybites-work/main/masters_code/assests/prob_rect.png)

![Oh my god](https://raw.githubusercontent.com/rhelmstedter/pybites-work/main/masters_code/assests/omg.gif)

It was so simple. Why did I not think of this before? I knew exactly what to do. Refactoring `_create_trial_school()` for a second time yielded:

```python
def _create_trial_school(
    population: int, prob_sped: float, prob_low_ses: float
) -> Counter:
    """Creates a counter of students with one of four possible labels: ['sped low',
    'sped high', 'gen_ed low' 'gen_ed high'].

    :population: int The number of students in the school.
    :prob_sped: float The probability that a student is labeled as sped.
    :prob_low_ses: float The probability that a student labeled as low ses.
    :returns: Counter The number of students with each label.
    """

    prob_gen_ed = 1 - prob_sped
    prob_high_ses = 1 - prob_low_ses
    labels = ("sped low", "sped high", "gen_ed low", "gen_ed high")
    probabilities = (
        round(prob_sped * prob_low_ses, 3),
        round(prob_sped * prob_high_ses, 3),
        round(prob_gen_ed * prob_low_ses, 3),
        round(prob_gen_ed * prob_high_ses, 3),
    )
    return Counter(choices(population=labels, weights=probabilities, k=population))
```

I decided to explicitly label the probabilities for the compliments so that when I created the tuple later, it was easy to quickly read what was happening. I also made a tuple of the labels instead of concatenating them. Again, much easier to read and see what is happening. The beauty of this is I can directly return the counter where `random.choices()` returns a list of the simulated student body. The [improved simulation](https://github.com/rhelmstedter/pybites-work/blob/main/masters_code/improved.py) can also be found in the repo.

## Comparing performance

I had done all of this refactoring with the goal of making the code easier to read, understand, and maintain. Performance was an afterthought. But now I was curious... Had all of these changes impacted performance? So I returned to google and found a timer decorator from [Real Python](https://realpython.com/python-timer/#a-python-timer-decorator) and modified to fit my needs. Then I moved my original code in a function, but did not change anything that impacted performance ([code](https://github.com/rhelmstedter/pybites-work/blob/main/masters_code/original_func.py) if you're interested). I ran black, and gave it the same arguments as the refactored code so I could run all three with the same parameters. To accomplish that, I created `comparison_runner()` to run each of the three versions ([original](), [refactored](https://github.com/rhelmstedter/pybites-work/blob/main/masters_code/refactored.py), and [improved](https://github.com/rhelmstedter/pybites-work/blob/main/masters_code/improved.py)). 

```python

def comparison_runner(funcs: dict, trials: int, trial_params: dict) -> dict[float]:
    """Run the three functions with the same number of trials and stats.

    :funcs: dict Keys are a printable name, values are the function itself.
    :trials: int The number of trials to run.
    :trial_params: dict Contains school poplulation and probabilities of labels.
    """

    seed(1)
    comparison_results = {"Trials": trials}
    for i, (func_name, func) in enumerate(funcs.items()):
        func = timer(func)  # Since functions are imported, I can't use the @timer syntactic sugar  
        elapsed_time = func(trials, **trial_params)
        comparison_results[func_name] = elapsed_time
    return comparison_results
```

I passed in the functions as a dictionary because the functions are all called `run_trials()` in their original module. When I tried to print the names, I didn't know which was which. The dictionary gave me a way to label each function. The trials needed to be passed independently of the other parameters so I could run a different number of trials. And I was able to finally able to make use of the [**](https://peps.python.org/pep-0448/) unpacking operator (and felt like a badass). This returns a dictionary with the number of trials, function names and the elapsed time.

I may be slightly obsessed with [rich](https://pypi.org/project/rich/) and this seemed to be the perfect opportunity to create a table.

```python
def display_table(comparison_results: list[dict]) -> None:
    """Display table that compares function performance across a range of trials.

    :comparison_results: list A list of results dictionaries from the comparison_runner.
    :returns: None
    """

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
```

This produces the following table.

![comparison results table]()


## Moral of the Story 

>It doesn't matter where you start. Just be better tomorrow than you are today.

When I first started learning python, I didn't even know what I didn't know. I wrote spaghetti code, and flung it against the wall to see what sticks. Today is not much different. I still try things that often don't work. In fact, my first attempt at refactoring the code I shared with you today hit a dead end. I put in hours of work only to realize I was solving the wrong problem. The biggest difference between today and when I first started is knowing how to search for help, and time in the saddle.
