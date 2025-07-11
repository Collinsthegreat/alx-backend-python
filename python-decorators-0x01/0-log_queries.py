import sqlite3
import functools

# ✅ Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log the SQL query
        query = kwargs.get('query') if 'query' in kwargs else args[0]
        print(f"[LOG] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')  # Connects to SQLite database file 'users.db'
    cursor = conn.cursor()              # Creates a cursor to execute SQL commands
    cursor.execute(query)              # Executes the provided SQL query
    results = cursor.fetchall()        # Fetches all resulting records
    conn.close()                       # Closes the database connection
    return results                     # Returns the result to the caller

# ✅ Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)

