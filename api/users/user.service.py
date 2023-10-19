import mysql.connector
from mysql.connector import pooling

db_config = {
    "host": "your_mysql_host",
    "user": "your_mysql_user",
    "password": "your_mysql_password",
    "database": "your_mysql_database",
    "pool_name": "mypool",
    "pool_size": 10,
}

connection_pool = pooling.MySQLConnectionPool(**db_config)

def create(data):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        query = "INSERT INTO registration (fullName, birthdate, gender, email, password, number) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (data["fullName"], data["birthdate"], data["gender"], data["email"], data["password"], data["number"])

        cursor.execute(query, values)
        connection.commit()

        return cursor.lastrowid

    except mysql.connector.Error as err:
        print(f"Error during create operation: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()

def get_users():
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT id, fullName, birthdate, gender, email, number, password FROM registration"
        cursor.execute(query)

        results = cursor.fetchall()
        return results

    except mysql.connector.Error as err:
        print(f"Error during get_users operation: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    user_data = {
        "fullName": "John Doe",
        "birthdate": "1990-01-01",
        "gender": "Male",
        "email": "john.doe@example.com",
        "password": "hashed_password",
        "number": "1234567890",
    }

    created_user_id = create(user_data)
    print(f"Created user with ID: {created_user_id}")

    users = get_users()
    print(users)
