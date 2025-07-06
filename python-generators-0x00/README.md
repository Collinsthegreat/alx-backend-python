# Python Generators: Memory-Efficient Data Handling

## Project Directory: `python-generators-0x00`

## 🧠 Overview

This project demonstrates advanced usage of **Python generators** to handle large datasets in memory-efficient ways using SQL and Python integration. It covers streaming rows, batch processing, lazy pagination, and aggregate computation without loading entire datasets into memory.

> Generators are Pythonic tools for efficient iteration. They allow you to yield data on-demand, reducing memory usage and speeding up data processing.

## Learning Objectives

* Understand and apply **Python generator functions** (`yield`)
* Work with **large SQL datasets** using `mysql-connector-python`
* Implement **lazy evaluation** for pagination and batch processing
* Perform **memory-efficient aggregation** without SQL built-ins
* Integrate **Python and MySQL** with production-level structure and comments

# 🏗️ Project Setup

### Requirements:

* Python 3.x
* MySQL Server
* `mysql-connector-python`
* Basic SQL (CREATE TABLE, SELECT, INSERT)
* Familiarity with generators (`yield`)

### Setup Instructions:

```bash
$ mysql -u root -p
mysql> CREATE DATABASE ALX_prodev;
$ pip install mysql-connector-python
```

---

## Tasks Breakdown

### `seed.py`

**Purpose**: Sets up the `ALX_prodev` database and populates `user_data` table with data from `user_data.csv`.

**Functions**:

* `connect_db()`
* `create_database()`
* `connect_to_prodev()`
* `create_table()`
* `insert_data()`

---

### `0-stream_users.py`

**Objective**: Create a generator that streams users row-by-row.

```python
def stream_users():
    yield each user dictionary one by one
```

**Test File**: `0-main.py`

---

### `1-batch_processing.py`

**Objective**: Stream data in batches and filter users older than 25.

```python
def stream_users_in_batches(batch_size):
    yield list of rows in batches

def batch_processing(batch_size):
    filters users > 25
```

**Test File**: `2-main.py`

---

### `2-lazy_paginate.py`

**Objective**: Implement lazy loading using pagination.

```python
def paginate_users(page_size, offset):
    returns paginated data from SQL

def lazy_pagination(page_size):
    yield each page lazily using offset
```

**Test File**: `3-main.py`

---

### `4-stream_ages.py`

**Objective**: Stream ages and compute average without using SQL `AVG()`.

```python
def stream_user_ages():
    yield ages one at a time

def calculate_average():
    computes average age with minimal memory
```

**Test Command**:

```bash
$ python3 4-stream_ages.py
Average age of users: 53.7
```

---

## Files Structure

```
python-generators-0x00/
├── 0-main.py
├── 0-stream_users.py
├── 1-batch_processing.py
├── 2-lazy_paginate.py
├── 3-main.py
├── 4-stream_ages.py
├── seed.py
├── user_data.csv
├── README.md
```

---

## Best Practices Followed

*  Generator functions with `yield`
*  SQL connection cleanup with `try/finally`
*  Modular code: functions separated by task
*  Commented code for clarity
*  Limited loop usage (as required)

## How to Test

Run each script using its corresponding `main.py` file or directly with:

```bash
$ python3 <file>.py
```

Example:

```bash
$ python3 0-main.py
$ python3 2-main.py | head -n 10
```

## Acknowledgements

This project is part of the **ALX Software Engineering Backend** curriculum. It was built to demonstrate mastery of generators and memory-efficient processing using Python and MySQL.

## References

* Python Docs: [Generators](https://docs.python.org/3/howto/functional.html#generators)
* MySQL Connector: [MySQL Python API](https://pypi.org/project/mysql-connector-python/)
* ALX Africa: [https://www.alxafrica.com](https://www.alxafrica.com)

---

