
# Table of Contents

1.  [Welcome to Hell](#orgee0a26d)
2.  [The Original Script](#org2a2a5de)
3.  [Refactoring Into Functions](#orgcd2f30d)
4.  [Testing](#orgee4e0e6)
5.  [The Problem](#org66afdbe)
6.  [Eureka](#org08920e7)
7.  [The Solution](#orgbf32042)
8.  [What Did I learn](#org96559fa)



<a id="orgee0a26d"></a>

# Welcome to Hell

<p class="verse">
This is a story that turns out well.<br />
But my code got stuck in import hell.<br />
I tried to teach my students all about pytest.<br />
Instead, for two days, I was sent on a debugging quest.<br />
</p>

I teach [middle school students](https://www.pybitespodcast.com/1501156/10519921-067-how-data-prepares-students-for-the-future) how to code in python. Given it is the start of our second semester together, I reckoned it was time to talk about the `datetime` module. Students generally love projects that they can connect back to themselves. So I thought a great way to introduce `datetime` was to have it calculate how many days the user has been alive, what day of the week they were born, and, of course, calculate their age.

As our script grew in complexity, I figured it was time to start testing. We has begun looking at pytest on our last project. I thought to myself, &ldquo;how hard could it be?&rdquo; Refactor into a couple of functions, run a couple tests, and have students submit! Famous last words&#x2026;

TODO flesh out the embarrassment of coding live


<a id="org2a2a5de"></a>

# The Original Script

Let us begin by looking at the original script.

    import datetime
    
    
    birthday = datetime.datetime(1986, 5, 19)
    today = datetime.datetime.today()
    
    days = (today - birthday).days
    age = days // 365
    
    paragraph = f"""You were born on {birthday:%B %d, %Y}. It was a {birthday:%A}. You have been alive for {days:,} days and are {age} years old."""
    print(paragraph)

    You were born on May 19, 1986. It was a Monday. You have been alive for 13,790 days and are 37 years old.

We were off to a good start. Students had a great time playing around with this. Most of them are somewhere around 4,000 days old, so I definitely took some heat for having an entire decimal place extra for my days, followed by comments like, &ldquo;wow, you&rsquo;re older than my dad.&rdquo; Thanks kids.

Then, one student had a great questions, &ldquo;Can we make it calculate the days until our next birthday?&rdquo; Why, yes we can! But I had not account for this level of complexity. We needed a compound conditional. This is something they had never seen before.

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
    
    paragraph = f"""You were born on {birthday:%B %d, %Y}. It was a {birthday:%A}. You have been alive for {days:,} days and are {age} years old. There are {days_till_next_bd} days until your next birthday."""
    print(paragraph)

    You were born on May 19, 1986. It was a Monday. You have been alive for 13,790 days and are 37 years old. There are 89 days until your next birthday.

At this point, it was already starting to get a little complex. Remember, I was teaching a room full of 41 students who are 11&#x2013;12 years old. But we pushed on. So we asked how else can we make this better? Well, at the moment, it only works for a single birthday. It would be nice to ask the user what their birthday is. It was pretty much the end of the class period, so we pushed off refactoring for the next day.


<a id="orgcd2f30d"></a>

# Refactoring Into Functions

The second day, we decided that we start moving chunks of code into functions. We ended up with the following.

    import datetime
    
    
    def build_birthday() -> datetime.datetime:
        """Build a datetime object for the user's birthday."""
        while True:
            year = int(input("What year were you born? "))
            month = int(input("What month were you born? "))
            day = int(input("What day were you born? "))
            return datetime.datetime(year, month, day)
    
    
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
        return f"""You were born on {birthday:%B %d, %Y}. It was a {birthday:%A}. You have been alive for {days:,} days and are {age} years old. There are {days_till_next_bd} days until your next birthday."""
    
    
    birthday = build_birthday()
    paragraph = create_bd_paragraph(birthday)
    print(paragraph)

Excellent! We were just about done. But I asked one more time, &ldquo;How else can we make this better?&rdquo; And then we realized. What if the user makes a mistake? They don&rsquo;t type just numbers, or mix up the days and the months and end up entering they were born during the 15th month. So we refactored that first function one more time using `try` and `except.`

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

This was sneaky because both `input` and `datetime.datetime` raise a `ValueError`. So we ended up having to use two `try` / `except` blocks.


<a id="orgee4e0e6"></a>

# Testing

It is worth mentioning that all of my students have a school issued Chromebook. That means we have to code using web&#x2013;based platforms. My favorite is [replit](https://replit.com) and that is what were using for this project. This will become import in a minute.

At this point, I thought it would useful to start testing. Students have been exposed to pytest already, but still very new. Since the first function returned a `datetime.datetime` object, it would be a great way to introduce the `isinstance` function. Here is where the problems started.

Since we are using `input`, I had to talk about mocking and patching. I gave a short lecture on the idea of mocking and how we are going to skip over the input process, and provide a value in our test. So we headed back to our code in replit, installed pytest, and created the test module. I always forget the exact syntax, so I did a quick google search for testing multiple inputs And we started coding.

    import datetime
    from unittest.mock import patch
    
    from birthday import build_birthday
    
    
    def test_build_bd():
        with patch("builtins.input", side_effect=["2000", "01", "02"]):
            actual = build_birthday()
            assert isinstance(actual, datetime.datetime)
            assert actual == datetime.datetime(2000, 1, 2)

Beautiful right? I&rsquo;m showing 12 year olds how to mock inputs in pytest. I. Am. Awesome. &ldquo;Alright everyone, head over to the shell and run `pytest`&rdquo;.


<a id="org66afdbe"></a>

# The Problem

Instead of that dopamine hit I get from seeing `1 passed` written in green, we got hit with this.

    ======================================= ERRORS ========================================
    __________________________ ERROR collecting test_birthday.py __________________________
    test_birthday.py:4: in <module>
        from birthday import build_birthday, calc_days_till_next_bd
    birthday.py:49: in <module>
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

An `OSError`? Ok, that is interesting. Perhaps I spelled something wrong? So I went back and checked. Nope, everything looks good. Maybe, its an import issue since we are using replit. So I tried quickly refactoring to `import birthday` instead of `from birthday import build_birthday`. Nope didn&rsquo;t work. Maybe, we can&rsquo;t mock in replit from some reason? So I copy the code, and the tests to my work computer (windows). Nope, and I get the same `OSError`.

If I ran pytest with the `-s` flag, I could provide input in the shell, and then the test would pass. I was so confused. *Clearly* (I thought) it had to be an issue with the way I was mocking the input.

At this point I had 41 adolescents getting bored as I floundered and had no idea how to fix the issue. So I turned to the students, &ldquo;Alright everyone, I&rsquo;m not sure how to fix this problem I have a couple of ideas, but it might take awhile. Go ahead an work on one of our ongoing activities.&rdquo; 10 years of teaching has taught me to always have something students could work on at any time. Go solve some PyBites, work on brilliant.org, do some typing practice.

Now, feeling embarrassed, frustrated, and still in charge of all the students I continued trying to debug. I was stuck for the rest of the period and the day for that matter. Once I got home, I figured I would try again on my home machine (macos). So I copied the code and tests, and ran it again. I continued to get the same error. I&rsquo;m frantically scouring the internet looking for clues for dealing with `OSError`. The only information I could find was on errors when trying to open and read files. Nothing really helpful with the context of testing and input. I finally gave up and took the dog for a walk.


<a id="org08920e7"></a>

# Eureka

This all happened on a Monday. Because we are on a block schedule, I didn&rsquo;t see the same group of students again until Wednesday. Tuesday I didn&rsquo;t think about the problem. Coming into the class on Wednesday, my plan was to skip over the testing the function with input, and head to the testing the second function, `calc_days_till_next_bd`.

We began class with a review of the code we had already written the previous class period. This led to this exchange:

Student: &ldquo;Do we have to do this? This code is longer and more confusing than what we had at first.&rdquo;
Me: *Thinking I had the perfect response.* &ldquo;Well for one thing, it allows us give a name to a chunk of code. Instead of holding all the steps in our head at once, we give it a name, and then call that function.&rdquo;
Student: &ldquo;So we don&rsquo;t have to do all the work, right?&rdquo;
Me: &ldquo;Technically, yes. We do not have to refactor everything into functions. But it helps to organize the code. It allows us to test the code to make sure it is doing what we think it is doing.&rdquo;
Student: ::stares skeptically:: &ldquo;You mean the part that isn&rsquo;t working and you don&rsquo;t know how to fix?&rdquo;
Me: &ldquo;Uh yeah&#x2026;&rdquo;
Student: &ldquo;So why are we doing this?&rdquo;
Me: &ldquo;Ok let me try this again. So you see, as Monty reads your code (we use [Stephen Gruppetta&rsquo;s](https://thepythoncodingbook.com/about/) analogy of [Monty and The White Room](https://www.thepythoncodingstack.com/p/monty-and-the-white-room-python-analogy)) he goes line by line. At the top of the code, we start by defining the functions. Once he has finished reading the through function definitions, he has read everything,built the function rooms, but hasn&rsquo;t actually used the code in the functions. Our entire program can reduced down to three chunks. Look at the last three lines of our code. It essentially describes what our program does: 1) build the birthday object. 2) build the paragraph based on the birthday object. 3) print the paragraph&#x2026;&rdquo;

And that&rsquo;s when it hit me. I had solved the problem without directly working on it.


<a id="orgbf32042"></a>

# The Solution

You may have noticed that in my test, I wrote `from birthday import build_birthday`. While it may be tempting to think that style of importing only imports the one function, the entire `birthday.py` file is read and executed. So when I run pytest, my testing module reads and executes `datetime`, `unittest`, and `birthday`. And what do the final three lines of `birthday` do?

    birthday = build_birthday()
    paragraph = create_bd_paragraph(birthday)
    print(paragraph)

It calls the `build_birthday` function,     '__doc__': None,
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

Notice anything? Now the `__name__` key is set to `"birthday"` instead of `"__main__"`. So by using the


<a id="org96559fa"></a>

# What Did I learn

