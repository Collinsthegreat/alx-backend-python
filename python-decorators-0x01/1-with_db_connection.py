import sqlite3
import functools

# ✅ Decorator to automatically manage DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open database connection
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection as the first argument to the function
            return func(conn, *args, **kwargs)
        finally:
            # Ensure the connection is closed even if an error occurs
            conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))  # Safe parameterized query
    return cursor.fetchone()  # Return the first matching row

# ✅ Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)
