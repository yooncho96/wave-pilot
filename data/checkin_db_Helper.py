# data/checkin_db_helper.py

import mysql.connector
import os
import json
from user_db_helper import ID

from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')

class DBHelper:
    """
    Manages database connection and queries using SSL.
    This database stores:
     1) emotion data from OpenAI for each user
     2) data from check-in tab
     3) log of user interactions for each user
    """

    def __init__(self):
        # Connect to MySQL
        # For MySQL:
        self.conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        self.cursor = self.conn.cursor()

        global ID
        self.ID = ID
        global emotion_list 
        emotion_list = ['anger', 'sadness', 'fear', 'shame', 'guilt', 'jealousy', 'envy', 'joy', 'love']

    def get_current_idx(self, tablename: str):
        select_query = "SELECT id FROM %s ORDER BY id DESC LIMIT 1"
        self.cursor.execute(select_query, (f"{tablename}_{self.ID}",))
        idx = self.cursor.fetchall()[0][0]
        return idx

    ## check-in data table
    ## unique table for each user
    def create_checkin_table(self):
        """
        Creates a table to store check-in data.
        """
        create_query = """
        CREATE TABLE IF NOT EXISTS %s (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp TIMESTAMP,
            mindfulness TEXT,
            diary INT,
            ABC_A BOOLEAN,
            ABC_B BOOLEAN,
            ABC_C BOOLEAN,
            PLEASE_Physical_iLlness BOOLEAN,
            PLEASE_balanced_Eating BOOLEAN,
            PLEASE_mood_Altering_substances BOOLEAN,
            PLEASE_Sleep BOOLEAN,
            PLEASE_Exercise BOOLEAN
        )
        """
        self.cursor.execute(create_query, (f"checkin_data_{self.ID}",))
        self.conn.commit()
    
    def insert_checkin_data(self, mindfulness, diary, ABC_A, ABC_B, ABC_C, 
                            PLEASE_Physical_iLlness, PLEASE_balanced_Eating, 
                            PLEASE_mood_Altering_substances, PLEASE_Sleep, PLEASE_Exercise):
        """
        Insert a row into the checkin_data table.
        """
        select_query = "SELECT NOW()"
        self.cursor.execute(select_query)
        timestamp = self.cursor.fetchall()

        insert_query = """
        INSERT INTO %s (
            timestamp, 
            mindfulness, 
            diary, 
            ABC_A, ABC_B, ABC_C, 
            PLEASE_Physical_iLlness, PLEASE_balanced_Eating, PLEASE_mood_Altering_substances, PLEASE_Sleep, PLEASE_Exercise
        )
        VALUES (
            %s,     -- timestamp, 
            %s,     -- mindfulness, 
            %s,     -- diary, 
            %s,     -- ABC_A, 
            %s,     -- ABC_B, 
            %s,     -- ABC_C, 
            %s,     -- PLEASE_Physical_iLlness, 
            %s,     -- PLEASE_balanced_Eating, 
            %s,     -- PLEASE_mood_Altering_substances, 
            %s,     -- PLEASE_Sleep, 
            %s,     -- PLEASE_Exercise
        )
        """
        data = (
            f"checkin_data_{self.ID}",
            timestamp,
            mindfulness, diary, ABC_A, ABC_B, ABC_C, 
            PLEASE_Physical_iLlness, PLEASE_balanced_Eating, 
            PLEASE_mood_Altering_substances, PLEASE_Sleep, PLEASE_Exercise
        )
        self.cursor.execute(insert_query, data)
        self.conn.commit()

    def get_all_checkin_data(self):
        """
        Fetch all rows from checkin_data.
        """
        # Fetch all rows from checkin_data.
        select_query = "SELECT * FROM %s"
        self.cursor.execute(select_query, (f"checkin_data_{self.ID}",))
        return self.cursor.fetchall()

    ## store user interactions
    ## unique table for each user
    def create_log_table(self):
        """
        Creates a table to store user interactions.
        """
        create_query = """
        CREATE TABLE IF NOT EXISTS %s (
            id INT AUTO_INCREMENT PRIMARY KEY,
            action VARCHAR(255),
            details TEXT
        )
        """
        self.cursor.execute(create_query, (f"log_data_{self.ID}",))
        self.conn.commit()

    def insert_log_data(self, action, details):
        """
        Insert a row into the log_data table.
        """
        insert_query = """
        INSERT INTO %s (action, details)
            VALUES (%s, %s)
        """
        data = (f"log_data_{self.ID}",action, details)
        self.cursor.execute(insert_query, data)
        self.conn.commit()

    def close(self):
        """
        Close the connection.
        """
        self.cursor.close()
        self.conn.close()