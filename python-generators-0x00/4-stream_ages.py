#!/usr/bin/env python3
import seed  # Using seed module to connect to the database


def stream_user_ages():
    """
    Generator function that yields user ages one by one from the database.
    
    Yields:
        int: Age of each user
    """
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor()

        cursor.execute("SELECT age FROM user_data")

        # Yield one age at a time
        for row in cursor:
            yield row[0]  # row[0] is the 'age' field

        cursor.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()


def compute_average_age():
    """
    Calculates and prints the average age of all users using a generator.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found.")


# Execute aggregation when run as a script
if __name__ == "__main__":
    compute_average_age()

Sample Output

Average age of users: 53.62

