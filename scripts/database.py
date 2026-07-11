import mysql.connector


def create_connection():
    """
    Connect to MySQL database.
    """

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",      # <-- We will update this if you have a password
        database="finflow_etl"
    )

    print("✅ Connected to MySQL Successfully!")

    return connection