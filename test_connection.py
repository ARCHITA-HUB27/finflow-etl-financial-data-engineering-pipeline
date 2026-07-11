from scripts.database import create_connection

conn = create_connection()

if conn.is_connected():
    print("🎉 Database connection successful!")

conn.close()