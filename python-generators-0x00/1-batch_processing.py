#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """
    Generator function that yields batches of user rows from the database.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")

            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch  # ✅ This is the generator yield

            cursor.close()

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """
    Processes users in batches and prints those over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
