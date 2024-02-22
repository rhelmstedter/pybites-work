
# Table of Contents

1.  [Welcome to Hell](#org021b697)
2.  [The Original Script](#orgce4dfc3)
3.  [Refactoring Into Functions](#org530512c)
4.  [Time to Test](#org082e5d9)
5.  [The Problem](#org7729914)
6.  [Eureka](#org9157bd4)
7.  [The Solution](#orgec846b6)
8.  [What Did I learn](#orgbd80ac0)



<a id="org021b697"></a>

# Welcome to Hell

Cue the theme song from [The Fresh Prince of Bel Air](https://youtu.be/1nCqRmx3Dnw?si=XhnQO85XOa61P4u1).

> This is a story that turns out well.

> But my code got stuck in import hell.

> I tried to teach my students all about pytest.

> Instead, for two days, I was sent on a debugging quest.

I teach [middle school students](https://www.pybitespodcast.com/1501156/10519921-067-how-data-prepares-students-for-the-future) how to code in python. I reckoned it was time to talk about the `datetime` module. Students generally love projects that they can connect back to themselves. So I thought a great way to introduce `datetime` was to have python calculate how many days the user has been alive, what day of the week they were born, and, of course, calculate their age.

As our script grew in complexity, I figured it was time to start testing. We has begun looking at pytest on our last project. I thought to myself, &ldquo;how hard could it be?&rdquo; Refactor into a couple of functions, run a couple tests, and have students submit a nice little project! Famous last words&#x2026;

It&rsquo;s all fun an games until you have room full of people watching you code live. Oh yeah, and I&rsquo;m supposed to the be expert in the room who is responsible for their education. Is it hot in here, or is it just me?


<a id="orgce4dfc3"></a>

# The Original Script

Let us begin by looking at the original script.

    import datetime
    
    
    birthday = datetime.datetime(1986, 5, 19)
    today = datetime.datetime.today()
    
    days = (today - birthday).days
    age = days // 365
    
    print(f"""You were born on {birthday:%B %d, %Y}. It was a {birthday:%A}. You have been alive for {days:,} days and are {age} years old.""")

We were off to a good start. Students had a great time playing around with this. Most of them are somewhere around 4,000 days old, so I definitely took some heat for having an entire extra decimal place for my days, followed by comments like, &ldquo;Wow, you&rsquo;re older than my dad and he&rsquo;s old.&rdquo; Thanks kids.

Then, one student had a great question, &ldquo;Can we make it calculate the days until our next birthday?&rdquo; Why, yes we can! But I had not accounted for this level of complexity. We needed a compound conditional, something they had never seen before.

    import datetime
    
    
    birthday = datetime.datetime(1986, 5, 19)
    today = datetime.datetime.today()
    
    # Determine if the birthday has already happended this year.
    if (today.month == birthday.month and today.day > birthday.day
        or today.month > birthday.month):
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
    
    days = (today - birthday).days
    age = days // 365
    days_till_next_bd = (next_birthday - today).days
    
    print(f"You were born on {birthday:%B %d, %Y}. It was a {birthday:%A}. You have been alive for {days:,} days and are {age} years old. There are {days_till_next_bd} days until your next birthday.")

At this point, it was already starting to get a little complex. Keep in mind, I was teaching a room full of 41 students who are 11&#x2013;12 years old. But we pushed on. So we asked how else can we make this better? Well, at the moment, it only works for a single birthday. It would be nice to ask the user what their birthday is. It was pretty much the end of the class period, so we pushed off refactoring for the next day.


<a id="org530512c"></a>

# Refactoring Into Functions

The second day, we decided that we start moving chunks of code into functions. We identified three major components of our code.

1.  It should build a `datetime.datetime` object for the birthday.
2.  It should calculate the days until the next birthday.
3.  It should compile all that information into the paragraph.

After figuring out the main thought for each function we started asking ourselves, &ldquo;How can we make this better?&rdquo; Oh, make it interactive with `input`. We could do some data validation to ensure if the user makes a mistake, they can try again. We ended up with the following `birthday.py` module.

    import datetime
    
    
    def build_birthday() -> datetime.datetime:
        """Build a datetime object for the user's birthday."""
        while True:
            try:
                year = int(input("What year were you born? "))
                month = int(input("What month were you born? "))
                day = int(input("What day were you born? "))
            except ValueError:
                print("Please enter numbers only")
                continue
            try:
                return datetime.datetime(year, month, day)
            except ValueError:
                print("Invalid date, please try again.")
                continue
    
    
    def calc_days_till_next_bd(
            today: datetime.datetime,
            birthday: datetime.datetime,
    ) -> int:
        """Calculate the number of days between today and birthday."""
        if (today.month == birthday.month and today.day > birthday.day
            or today.month > birthday.month):
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
        return f"You were born on {birthday:%B %d, %Y}. It was a {birthday:%A}. You have been alive for {days:,} days and are {age} years old. There are {days_till_next_bd} days until your next birthday."
    
    
    birthday = build_birthday()
    paragraph = create_bd_paragraph(birthday)
    print(paragraph)

Then, we called the functions we just created at the end of the program to get the same output we had at the beginning of all this.


<a id="org082e5d9"></a>

# Time to Test

It is worth mentioning that all of my students have a school issued Chromebook. That means we have to code using web&#x2013;based platforms. My favorite is [replit](https://replit.com) and that is what were using for this project. This will become import in a minute.

At this point, I thought it would useful to start testing. Students have been exposed to pytest already, but still very new. Since the first function returned a `datetime.datetime` object, it would be a great way to introduce the `isinstance` function. Here is where the problems started.

Since we are using `input`, I had to talk about mocking and patching. I gave a short lecture on the idea of mocking and how we are going provide a values in our test so the &ldquo;wait for the user to input data&rdquo; part is skipped. So we headed back to our code in replit, installed pytest, and created the `test_birthday.py` module. I always forget the exact syntax, so I did a quick google search for testing multiple inputs And we started coding.

    import datetime
    from unittest.mock import patch
    
    from birthday import build_birthday
    
    
    def test_build_bd():
        with patch("builtins.input", side_effect=["2000", "01", "02"]):
            actual = build_birthday()
            assert isinstance(actual, datetime.datetime)
            assert actual == datetime.datetime(2000, 1, 2)

Beautiful right? I&rsquo;m showing 12 year olds how to mock `input` in pytest. I. Am. Awesome. Full of confidence, I tell the students, &ldquo;Alright everyone, head over to the shell and run pytest&rdquo;.


<a id="org7729914"></a>

# The Problem

Instead of that dopamine hit I get from seeing `1 passed` written in green, we got hit with this.

    ======================================= ERRORS ========================================
    __________________________ ERROR collecting test_birthday.py __________________________
    test_birthday.py:4: in <module>
    from birthday import build_birthday, calc_days_till_next_bd
    birthday.py:46: in <module>
    birthday = build_birthday()
    birthday.py:8: in build_birthday
    year = int(input("What year were you born? "))
    .pythonlibs/lib/python3.12/site-packages/_pytest/capture.py:205: in read
    raise OSError(
        E   OSError: pytest: reading from stdin while output is captured!  Consider using `-s`.
        ----------------------------------- Captured stdout -----------------------------------
        What year were you born?
        =============================== short test summary info ===============================
        ERROR test_birthday.py - OSError: pytest: reading from stdin while output is captured!
        Consider using `-s`.
        !!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!
        ================================== 1 error in 0.70s ===================================

An `OSError`? Ok, that is interesting. Perhaps I spelled something wrong? So I went back and checked. Nope, everything looks good. Maybe, it&rsquo;s an import issue since we are using replit. So I tried quickly refactoring to `import birthday` instead of `from birthday import build_birthday`. Nope didn&rsquo;t work. Maybe, we can&rsquo;t mock in replit from some reason? So I copy the code, and the tests to my work computer (windows). Nope, and I get the same `OSError`.

Now, if I followed the advice in the error message and ran pytest with the `-s` flag, I could provide input in the shell, and then the test would pass. I was so confused. *Clearly* (I thought) it had to be an issue with the way I was mocking the input.

At this point I had 41 adolescents getting bored as I floundered and had no idea how to fix the issue. So I turned to the students, &ldquo;Alright everyone, I&rsquo;m not sure how to fix this problem I have a couple of ideas, but it might take awhile. Go ahead an work on one of our ongoing activities.&rdquo; 10 years of teaching has taught me to always have something students could work on at any time. Go solve some PyBites, work on brilliant.org, do some typing practice.

Now, feeling embarrassed, frustrated, and still in charge of all the students I continued trying to debug. I tried use a `patch` as a decorator like I had down in previous projects. Nope, didn&rsquo;t work. Everything I tried manipulating in the testing module didn&rsquo;t work. I was stuck for the rest of the period and the day for that matter.

Once I got home, I figured I would try again on my home machine (macos). So I copied the code and tests, and ran it again. I continued to get the same error. I&rsquo;m frantically scouring the internet looking for clues for dealing with `OSError`. The only information I could find was on errors when trying to open and read files. Nothing really helpful with the context of testing and input. I finally gave up and took the dog for a walk.


<a id="org9157bd4"></a>

# Eureka

We had started the project on a Friday. The problem happened on a Monday. Because we are on a block schedule, I didn&rsquo;t see the same group of students again until Wednesday. Tuesday I didn&rsquo;t work directly on the problem. I was <del>scared</del> busy and didn&rsquo;t have time in the evening to work on in. Coming into the class on Wednesday, my plan was to skip over the testing the `build_birthday` function, and jump to the testing the `calc_days_till_next_bd` function with `isinstance`.

We began class with a review of the code we had already written the previous class period. This led to this exchange (I&rsquo;m paraphrasing and, possibly, projecting):

**Student**: *I&rsquo;ll stump him with this one*. &ldquo;Do we have to do this? This code is longer and more confusing than what we had at first.&rdquo;

**Me**: *Thinking I had the perfect response.* &ldquo;Well for one thing, it allows us give a name to a chunk of code. Instead of holding all the steps in our head at once, we give it a name, and then call that function.&rdquo;

**Student**: &ldquo;So we don&rsquo;t have to do all the work, right?&rdquo;

**Me**: &ldquo;Technically, yes. We do not have to refactor everything into functions. But it helps to organize the code. It allows us to test the code to make sure it is doing what we think it is doing.&rdquo;

**Student**: *Stares skeptically.* &ldquo;You mean the part that isn&rsquo;t working and you don&rsquo;t know how to fix?&rdquo;

**Me**: &ldquo;Uh yeah&#x2026;&rdquo;

**Student**: &ldquo;So why are we doing this?&rdquo;

**Me**: &ldquo;Ok let me try this again. So you see, as Monty reads your code (Note for the reader: we use [Stephen Gruppetta&rsquo;s](https://thepythoncodingbook.com/about/) analogy of [Monty and The White Room](https://www.thepythoncodingstack.com/p/monty-and-the-white-room-python-analogy)) he goes line by line. At the top of the code, we start by defining the functions. Once he has finished reading the through function definitions, he has read everything,built the function rooms, but hasn&rsquo;t actually used the code in the functions. Our entire program can reduced down to three chunks. Look at the last three lines of our code. It essentially describes what our program does: 1) build the birthday object. 2) build the paragraph based on the birthday object. 3) print the paragraph&#x2026;&rdquo;

And that&rsquo;s when it hit me. I had solved the problem without directly working on it.


<a id="orgec846b6"></a>

# The Solution

You may have noticed that in the test, I wrote `from birthday import build_birthday`. While it may be tempting to think that style of importing only looks at the one function, the entire `birthday.py` file is read and executed. So when I run `pytest`, my testing module reads and executes `datetime`, `unittest`, and `birthday`. And what do the final three lines of `birthday` do?

    birthday = build_birthday()
    paragraph = create_bd_paragraph(birthday)
    print(paragraph)

It calls the `build_birthday` function, including the `input` calls, as it is being imported. This is before I can actually mock it. So my tests get hung up waiting for user input that never comes.

The solution was to use the if `__name__ == "___main___"` idiom:

    if __name__ == "__main__":
        birthday = build_birthday()
        paragraph = create_bd_paragraph(birthday)
        print(paragraph)

Whenever a python module is run, there is something called a global [symbol table](https://en.wikipedia.org/wiki/Symbol_table). Essentially, this is a dictionary with information about the module. You can see this dictionary by calling the `globals` function and printing the return value. Let&rsquo;s see an example.

    from pprint import pprint
    pprint(globals())

I have imported `pprint` so that it prints each item in the dictionary on its own line. If you look at the last line, you can see `pprint` is now in the global symbol table. Also, look at the key `__name__` . The value is `__main__` . Whenever a module is run directly, for example by typing `python3 module_name` or by clicking the run button in your editor of choice, the `__name__` attribute is assigned the value `__main__` .

To get the dictionary below, I have placed a `globals` function call in the `birthday.py` module and printed the return value. Now, instead of running the module directly, I ran the testing module `python test_birthday.py`. When the birthday module is imported, the global symbol table still gets printed. Note, I edited a couple things in the dictionary like the specific locations on my hard drive, and I replaced the long `__builtins__` value with `{...}` .

    {'__builtins__': {...},
     '__cached__': ...,
     '__doc__': None,
     '__file__': '/path/to/birthday.py',
     '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x101117590>,
     '__name__': 'birthday',
     '__package__': '',
     '__spec__': ModuleSpec(name='birthday', loader=<_frozen_importlib_external.SourceFileLoader object at 0x101117590>, origin='/path/to/birthday.py'),
     'build_birthday': <function build_birthday at 0x1011189a0>,
     'calc_days_till_next_bd': <function calc_days_till_next_bd at 0x101cb96c0>,
     'create_bd_paragraph': <function create_bd_paragraph at 0x101cb9760>,
     'datetime': <module 'datetime' from '/path/to/python3.12/datetime.py'>,
     'pprint': <function pprint at 0x100e585e0>}

Notice anything? Now the `"__name__"` key is set to `"birthday"` instead of `"__main__"`. So when the `birthday.py` module is imported the `__name__` attribute matches the name of the module. So the idiom allows us to only run certain blocks of code if we are running a module directly as opposed to importing it. By moving the last three lines of `bithday.py` inside the if block, the function calls to `build_bithday` and `create_bd_paragraph` will only be execute if we are running the module directly.


<a id="orgbd80ac0"></a>

# What Did I learn

Well I&rsquo;m not sure. Everything I am about to share I already *knew*.

First, despite being hilarious, [rubber ducky debugging](https://rubberduckdebugging.com) is real. There is power in going line by line through the code and saying out loud&#x2014;or on paper&#x2014;what the code is doing. Returning to the code a couple days later, the act of reviewing the code and explaining what was happening allowed the solution to present itself. It is just in this case, my rubber ducky was a room full of adolescents students.

Second, if you believe things on the internet, it is a [superpower](https://www.theguardian.com/lifeandstyle/2019/jul/28/its-a-superpower-how-walking-makes-us-healthier-happier-and-brainier) to [walk away](https://www.psychologytoday.com/us/blog/prescriptions-life/201901/taking-walk-will-boost-your-creativity-and-problem-solving#:~:text=Einstein%20walked%20on%20the%20beach,of%20their%20lives%20and%20work) from the problem. Einstein, [Hemingway, Thoreau, and Jefferson](https://www.huffpost.com/entry/hemingway-thoreau-jeffers_b_3837002) all proclaim the virtues of walking as a way to clear the mind as they puzzled something out. Barbara Oakley describes two types of thinking: [Focused and Diffused](https://barbaraoakley.com/wp-content/uploads/2018/02/Learning-How-to-Learn-Excerpt.pdf). Focused thinking is when you are intently focused on something. Diffused thinking occurs when your mind is relaxed and you aren&rsquo;t thinking about anything in particular. When trying to solve a problem, becoming hyper-focused can actually be counter productive. We can often get lost in what Boser describes as shallow features instead of taking a step back and reviewing the deep details (for a deep dive on this see [Becoming A More Effective Learner](https://barbaraoakley.com/wp-content/uploads/2018/02/Learning-How-to-Learn-Excerpt.pdf)). Deep details are those that contain the essence of the problem. While shallow details maybe nothing more than distractions. The act of walking&#x2014;and this is important&#x2014;while not actively thinking about the problem can over lead to the solution.

I generally approach neuroscience research that draws conclusions based on brain scans with a healthy dose of skepticism. That being said, in my little N~1 experiment this does seem be the case. I became hyper focused on the shallow detail of the `OSError` instead of taking a step back and thinking about the problem overall. I should have outlined the problem and walked away a lot sooner. This is a hard lesson to learn. So I hope this article serves as a reminder for myself and everyone reading. Sometimes you just have to outline the problem and go walk the dog.

