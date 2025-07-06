#!/usr/bin/env python3
import seed  # Importing your database helper module


def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database.
    
    Args:
        page_size (int): Number of users per page
        offset (int): Starting point for the current page
    Returns:
        list[dict]: A list of user records
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily paginates through user data using yield.

    Args:
        page_size (int): Number of users per page

    Yields:
        list[dict]: Each page of users, loaded on demand
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break  # Exit when there are no more results
        yield page  # Yield one page at a time
        offset += page_size  # Move to the next offset


Sample Output
(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00 % python3 3-main.py | head -n 5

{'user_id': '00234e50...', 'name': 'Dan...', 'email': 'Molly...', 'age': 67}
{'user_id': '006bfede...', 'name': 'Glenda...', 'email': 'Miriam...', 'age': 119}
...

