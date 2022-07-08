--- 
title: Newbie Bite 23
author: Russell Helmstedter
date: 2022-03-27
--- 

# Looping through Dictionaries

# Dictionary Data Retrieval Methods

```python
dictionary = { key1: value1, key2: value2, key3: value3 }

dictionary.keys() # returns just the keys
dictionary.values() # returns just the values
dictionary.items() # returns the keys and the values as a pair
```

# Using the for loop with `.items()`

```python
for key, value in dictionary.items():
    # do something with both the key and the value
```
