--- 
title: Newbie Bite 22
author: Russell Helmstedter
date: 2022-03-26
--- 

# `for` loops

---

# Vocabulary

**Iterable:** anything you can loop over

**Iteration:** one execution of the loop

**Index:** variable that tracks which step you're on

---

# Examples of Iterables

+ strings
+ lists
+ tuples
+ dictionaries*

# Basic Structure of `for` loops

```python
for variable in iterable:
    indent body of loop
    second line
    third line

object = value
```

---

# Example `for` loop

```python
for number in [1, 2, 3]:
    print(number)
```

---

## Break down of the `for` loop

First time through:
```python
for number in [*1*, 2, 3]:
    print(number)
```

Current output:

```python
1
```

---

## Break down of the `for` loop

Second time though:
```python
for number in [1, *2*, 3]:
    print(number)
```

Current output:

```python
1
2
```

---

## Break down of the `for` loop

Third time through:
```python
for number in [1, 2, *3*]:
    print(number)
```

Current output:

```python
1
2
3
```
