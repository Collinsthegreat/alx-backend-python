

#!/usr/bin/env python3
import mysql.connector  # For database connection
from mysql.connector import Error  # For error handling

def stream_users_in_batches(batch_size):
    """
    Generator function that yields users one at a time from the database in batches.

    Args:
        batch_size (int): Number of users to fetch per batch.
    Yields:
        dict: One user dictionary at a time.
    """
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Update if your MySQL requires a password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")

            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break

                # ✅ Instead of yield batch, we yield one item at a time using yield from
                yield from batch  # 🔄 This expands the list and yields each user

            cursor.close()

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            connection.close()

def batch_processing(batch_size):
    """
    Processes each user and prints those over the age of 25.

    Args:
        batch_size (int): Size of each fetch batch.
    """
     for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user.get('age') is not None and user['age'] > 25:
                yield user

