import mysql.connector
from mysql.connector import Error

def test_connection():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Change this to your MySQL root password
            database='dental_clinic_system'
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            cursor = connection.cursor()
            cursor.execute("select database();")
            database = cursor.fetchone()
            print(f"Connected to database: {database[0]}")
            return True
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    test_connection()