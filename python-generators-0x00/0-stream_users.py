#!/usr/bin/env python3

import mysql.connector  # Used to connect to the MySQL database
from mysql.connector import Error  # To catch and handle connection-related errors

def stream_users():
    """
    Generator function that connects to the 'ALX_prodev' MySQL database
    and yields rows from the 'user_data' table one at a time.
    """
    try:
        # Establish a connection to the ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Replace with your actual password if set
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)  # Use dictionary format for row output
            cursor.execute("SELECT * FROM user_data")  # Execute query to fetch all user_data rows

            # Loop through each row in the result set one by one
            for row in cursor:
                yield row  # Yield the current row to the calling context

            # Close cursor after streaming is done
            cursor.close()

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        # Ensure the connection is properly closed even if an error occurred
        if connection.is_connected():
            connection.close()

Usage Example 
#!/usr/bin/python3
from itertools import islice  # islice helps limit how many results we print from the generator
stream_users = __import__('0-stream_users').stream_users

# Iterate through the generator and print only the first 6 user records
for user in islice(stream_users(), 6):
    print(user)


Sample Output
{'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
{'user_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}
...
