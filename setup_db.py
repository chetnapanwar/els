import psycopg2

# Database connection details
DB_CONFIG = {
    "dbname": "els_db",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}

def setup_database():
    try:
        # Connect to the database
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("Connected to the database successfully.")

        # Drop existing table to reset schema
        cur.execute("DROP TABLE IF EXISTS users;")
        print("Dropped existing 'users' table.")

        # Create table with password column
        create_table_query = """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        );
        """
        cur.execute(create_table_query)
        print("Table 'users' created successfully.")

        # Insert data
        users_data = [
            ('Aarav Patel', 'aarav.patel@example.com', 'dev123'),
            ('Vihaan Rao', 'vihaan.rao@example.com', 'design456'),
            ('Aditya Sharma', 'aditya.sharma@example.com', 'manage789'),
            ('Sai Gupta', 'sai.gupta@example.com', 'code999'),
            ('Arjun Singh', 'arjun.singh@example.com', 'analyze000')
        ]

        insert_query = """
        INSERT INTO users (name, email, password) 
        VALUES (%s, %s, %s)
        ON CONFLICT (email) DO NOTHING;
        """
        
        cur.executemany(insert_query, users_data)
        conn.commit()
        print(f"Inserted {cur.rowcount} rows into 'users' table.")

        # Fetch and print all users
        print("\nCurrent users in database:")
        cur.execute("SELECT * FROM users;")
        rows = cur.fetchall()
        for row in rows:
            print(row)

        # Close communication with the database
        cur.close()
        conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    setup_database()
