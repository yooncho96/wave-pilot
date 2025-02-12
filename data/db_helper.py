import cx_Oracle
import os

from dotenv import load_dotenv
import json
load_dotenv()

oracle_username = os.getenv('oracle_username')
oracle_password = os.getenv('oracle_password')
oracle_dsn = os.getenv('oracle_dsn')

class DBHelper:

    def __init__(self):
        # Connect to Oracle Database
        try:
            connection = cx_Oracle.connect(oracle_username, oracle_password, oracle_dsn)
            print("Successfully connected to Oracle Database")
        except cx_Oracle.DatabaseError as e:
            print(f"Error connecting to Oracle DB: {e}")
            exit()

        self.cursor = connection.cursor()

    def create_tables(self):
        try:
            self.cursor.execute("""
                CREATE TABLE UserInfo (
                    id          NUMBER PRIMARY KEY,
                    wave_id     NUMBER NOT NULL,
                    wave_id INT,
                    password VARCHAR(50),
                    code VARCHAR(4),
                    email VARCHAR(100),
                    phone VARCHAR(20),  # in format ###-###-####
                    street_address VARCHAR(255),
                    city VARCHAR(255),
                    state VARCHAR(2),
                    zip_code VARCHAR(5),
                    crisis_name1 VARCHAR(100),
                    crisis_relationship1 VARCHAR(100),
                    crisis_phone1 VARCHAR(20)   # in format ###-###-####,
                    crisis_name2 VARCHAR(100),
                    crisis_relationship2 VARCHAR(100),
                    crisis_phone2 VARCHAR(20)   # in format ###-###-####
                )
            """)

            self.cursor.execute("""
                CREATE TABLE Emotions (
                    id              NUMBER PRIMARY KEY,
                    wave_id         INT
                    timestamp       TIMESTAMP,
                    transcript      TEXT,
                    anger           FLOAT,
                    sadness         FLOAT,
                    fear            FLOAT,
                    shame           FLOAT,
                    guilt           FLOAT,
                    jealousy        FLOAT,
                    envy            FLOAT,
                    joy             FLOAT,
                    love            FLOAT,
                    sorted          JSON,
                    correct         BOOLEAN,
                    adjusted_main   JSON
                )
            """)

            self.cursor.execute("""
                CREATE TABLE selected_skills (
                    id                  INT AUTO_INCREMENT PRIMARY KEY,
                    wave_id             INT
                    timestamp           TIMESTAMP,
                    Paced_breathing     BOOLEAN,
                    Counting_down_from_10 BOOLEAN,
                    Search_for_that_color BOOLEAN,
                    Search_for_that_shape BOOLEAN,
                    5_4_3_2_1           BOOLEAN,
                    Body_Scan           BOOLEAN,
                    Narrate_a_task      BOOLEAN,
                    Learning_from_an_animal_friend BOOLEAN,
                    Blindfolded_movement BOOLEAN,
                    Blindfolded_snack_time   BOOLEAN,
                    Coloring            BOOLEAN,
                    Doodling            BOOLEAN,
                    Taking_a_walk       BOOLEAN,
                    Dancing             BOOLEAN,
                    Light_a_candle      BOOLEAN,
                    Journaling          BOOLEAN
                )
            """)

        except cx_Oracle.DatabaseError as e:
            print(f"Error creating tables: {e}")
            connection.rollback()

    def insert_data():
        try:
            # Insert into UserInfo
            cursor.execute("""
                INSERT INTO UserInputs_Core (id, user_id, input_text, created_at)
                VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD HH24:MI:SS'))
            """, (1, 101, 'Hello World', '2025-02-10 10:00:00'))
            print("Inserted data into UserInputs_Core")

            # Insert into UserInputs_Attachments (with empty BLOB for now)
            cursor.execute("""
                INSERT INTO UserInputs_Attachments (id, user_input_id, large_attachment)
                VALUES (:1, :2, EMPTY_BLOB())
            """, (1, 1))
            print("Inserted data into UserInputs_Attachments")

            connection.commit()

        except cx_Oracle.DatabaseError as e:
            print(f"Error inserting data: {e}")
            connection.rollback()

    # 3. Query Data Without Attachment (Fast Query)
    def query_core_data():
        try:
            cursor.execute("""
                SELECT id, user_id, input_text, TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS') as created_at
                FROM UserInputs_Core
                WHERE user_id = :user_id
            """, {'user_id': 101})

            rows = cursor.fetchall()
            print("\n--- Core Data ---")
            for row in rows:
                print(f"ID: {row[0]}, User ID: {row[1]}, Input: {row[2]}, Created At: {row[3]}")

        except cx_Oracle.DatabaseError as e:
            print(f"Error querying core data: {e}")

    # 4. Query Data With Attachment (Full Data)
    def query_full_data():
        try:
            cursor.execute("""
                SELECT c.id, c.user_id, c.input_text, TO_CHAR(c.created_at, 'YYYY-MM-DD HH24:MI:SS') as created_at, a.large_attachment
                FROM UserInputs_Core c
                LEFT JOIN UserInputs_Attachments a ON c.id = a.user_input_id
                WHERE c.user_id = :user_id
            """, {'user_id': 101})

            rows = cursor.fetchall()
            print("\n--- Full Data (With Attachments) ---")
            for row in rows:
                print(f"ID: {row[0]}, User ID: {row[1]}, Input: {row[2]}, Created At: {row[3]}, Attachment: {row[4]}")

        except cx_Oracle.DatabaseError as e:
            print(f"Error querying full data: {e}")

    # Run Functions
    create_tables()
    insert_data()
    query_core_data()
    query_full_data()

    # Close Connection
    cursor.close()
    connection.close()
