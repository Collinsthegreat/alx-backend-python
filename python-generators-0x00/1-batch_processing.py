#!/usr/bin/env python3

import mysql.connector
import sys
import seed  # assumes this provides `connect_to_prodev()` and `user_data`

def stream_users_in_batches(batch_size):
    """
    Connects to ALX_prodev and yields users one-by-one in batches from the user_data table.

    Args:
        batch_size (int): Number of rows to fetch per batch.

    Yields:
        dict: A single user dictionary at a time.
    """
    connection = None
    cursor = None
    try:
        connection = seed.connect_to_prodev()
        if not connection:
            print("Failed to connect to the database. Cannot stream users.", file=sys.stderr)
            return

        cursor = connection.cursor(dictionary=True)
        select_query = f"SELECT user_id, name, email, age FROM {seed.user_data};"
        cursor.execute(select_query)

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            # ✅ Only 1 loop used: yield each user from the batch
            yield from batch

    except mysql.connector.Error as err:
        print(f"Database error: {err}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception:
                pass
        if connection:
            try:
                connection.close()
            except Exception:
                pass

def batch_processing(batch_size):
    """
    Processes users streamed from the database and yields only those over age 25.

    Args:
        batch_size (int): Number of users to fetch per batch.

    Yields:
        dict: A user dictionary for users over age 25.
    """
    for user in stream_users_in_batches(batch_size):  # ✅ 2nd and final loop
        if user.get('age') is not None and user['age'] > 25:
            yield user
