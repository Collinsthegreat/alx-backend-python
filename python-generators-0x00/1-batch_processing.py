#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

def stream_users():
    """
    Generator function that connects to the database and yields one user at a time.

    Yields:
        dict: A dictionary representing a user row.
    """
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Update if your MySQL setup uses a password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")

            # Yield each row one by one
            for row in cursor:
                yield row  # 🔄 Yield each user row individually

            cursor.close()

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            connection.close()

def batch_processing():
    """
    Processes users one by one and prints those over the age of 25.
    """
    for user in stream_users():
        if user['age'] > 25:
            print(user)
