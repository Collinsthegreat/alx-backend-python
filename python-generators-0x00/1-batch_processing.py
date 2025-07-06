#!/usr/bin/env python3
import mysql.connector  # For database connection
from mysql.connector import Error  # For error handling

def stream_users_in_batches(batch_size):
    """
    Generator function that yields batches of user rows from the database.

    Args:
        batch_size (int): Number of users to fetch per batch.
    Yields:
        list[dict]: List of user dictionaries per batch.
    """
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Update if your local MySQL requires a password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            # Execute query to get all rows
            cursor.execute("SELECT * FROM user_data")

            # Loop through and yield rows in batches
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                    
                     # 🔶 YIELD: Generator yields one batch at a time
                yield batch  # Yield the current batch

            cursor.close()

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            connection.close()

def batch_processing(batch_size):
    """
    Processes each batch of users and prints those over the age of 25.

    Args:
        batch_size (int): Size of each batch to process.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)  # Only print users older than 25

Sample Output
{'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
{'user_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}
{'user_id': '006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'name': 'Daniel Fahey IV', 'email': 'Delia.Lesch11@hotmail.com', 'age': 49}
{'user_id': '00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'name': 'Alma Bechtelar', 'email': 'Shelly_Balistreri22@hotmail.com', 'age': 102}
{'user_id': '01187f09-72be-4924-8a2d-150645dcadad', 'name': 'Jonathon Jones', 'email': 'Jody.Quigley-Ziemann33@yahoo.com', 'age': 116}



