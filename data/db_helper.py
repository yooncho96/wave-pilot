# data/db_helper.py

import mysql.connector
import os

from dotenv import load_dotenv
import json
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
     1) user information to use when logging in
     2) emotion data from OpenAI for each user
     3) data from check-in tab
     4) log of user interactions for each user
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

        self.entry = 0

    ## User data table

    def create_user_table(self):
        """
        Example method to create a table if it doesn't exist.
        Adjust the schema as needed.
        """
        create_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            id INT,
            password VARCHAR(50),
            email VARCHAR(100),
            phone VARCHAR(20),  # in format ###-###-####
            street_address VARCHAR(255),
            city VARCHAR(255),
            state VARCHAR(2),
            zip_code VARCHAR(5),
            crisis_name VARCHAR(100),
            crisis_phone VARCHAR(20),   # in format ###-###-####
        )
        """
        
        self.cursor.execute(create_query)
        self.conn.commit()
        
    def set_pw(self, id, password):     # user will set the pw; other fields will be set by admin
        """
        User sets password.
        """
        update_query = "UPDATE user_data SET password = %s WHERE id = %s"
        self.cursor.execute(update_query, (password, id))
        self.conn.commit()
        self.ID = id

    def lost_pw_email(self, id):     # find user that has id -> return email
        """
        Reset pw when lost.
        """
        select_query = "SELECT email FROM user_data WHERE id = (%s)"
        self.cursor.execute(select_query, (id,))
        
        return self.cursor.fetchall(), id

    def reset_pw(self, password):
        update_query = "UPDATE user_data SET password = %s WHERE id = %s"
        self.cursor.execute(update_query, (password, self.ID))
        self.conn.commit()

    def get_all_user_data(self):
        """
        Fetch all data from table.
        """
        select_query = "SELECT * FROM user_data WHERE id = (self.ID)"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()
    
    ## emotion data table
    ## unique table for each user
    def create_emotion_table(self):
        """
        Creates a table to store transcripts and emotion scores.
        """
        table_name = f"emotion_data_{self.ID}"

        create_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp TIMESTAMP,
            transcript TEXT,
            anger FLOAT,
            sadness FLOAT,
            fear FLOAT,
            shame FLOAT,
            guilt FLOAT,
            jealousy FLOAT,
            envy FLOAT,
            joy FLOAT,
            love FLOAT,
            top3 JSON,
            correct BOOLEAN,
            adjusted_top3 JSON
        )
        """
        self.cursor.execute(create_query)
        self.conn.commit()
        self.entry = 0

    def insert_emotion_data(self, transcript, anger, sadness, fear, shame, guilt,
                            jealousy, envy, joy, love):
        """
        Insert a row into the emotion_data table.
        """
        self.entry = self.entry + 1

        table_name = f"emotion_data_{self.ID}"
        select_query = "SELECT NOW()"
        self.cursor.execute(select_query)
        timestamp = self.cursor.fetchall()
        correct = True if correct else False

        insert_query = f"""
        INSERT INTO {table_name} ({timestamp}, transcript, anger, sadness, fear, shame, guilt, jealousy, envy, joy, love, top3, correct, adjusted_top3)
        VALUES
            ({timestamp}, transcript, anger, sadness, fear, shame, guilt, jealousy, envy, joy, love, NULL, correct, NULL)
        """
        data = (transcript, anger, sadness, fear, shame, guilt, jealousy, envy, joy, love)
        self.cursor.execute(insert_query, data)
        self.conn.commit()

    def get_top3_emotion_data(self):
        """
        Fetch the top 3 emotions from the latest entry in the emotion_data table.
        """
        table_name = f"emotion_data_{self.ID}"

        # Fetch all rows from emotion_data.
        select_query = f"""
            SELECT anger, sadness, fear, shame, guilt, jealousy, envy, joy, love 
            FROM {table_name}
            WHERE id = {self.entry}
            """
        self.cursor.execute(select_query)
        full_data = self.cursor.fetchall()[-1]  # list of tuples (each tuple=row); last entry

        # retrieve top 3 emotions as list of ([name],[score])
        emotion_order = ['anger', 'sadness', 'fear', 'shame', 'guilt', 'jealousy', 'envy', 'joy', 'love']
        sorted_emotions = sorted(enumerate(full_data), key=lambda x: x[1], reverse=True)[:3]
        top3_emotions = [(emotion_order[i], score) for i, score in sorted_emotions]

        top3_json = json.dumps(top3_emotions)

        update_query = f"""
            UPDATE {table_name}
            SET top3 = %s
            WHERE id = {self.entry}
            """
        self.cursor.execute(update_query, (top3_json,))
        self.conn.commit()

        return top3_emotions

    def adjust_emotion(self, feedback, adjustment):
        """
        Update emotion scores based on user feedback.
        """
        table_name = f"emotion_data_{self.ID}"

        if feedback == "correct":
            correct = True
        else:
            correct = False
            adjustment_json = json.dumps(adjustment)
            update_query = f"""
                UPDATE {table_name}
                SET correct = %s, adjusted_top3 = %s
                WHERE id = {self.entry}
                """
            self.cursor.execute(update_query, (correct, adjustment_json,))
            self.conn.commit()

        return adjustment
    
    ## check-in data table
    ## unique table for each user
    def create_checkin_table(self):
        """
        Creates a table to store check-in data.
        """
        table_name = f"checkin_data_{self.ID}"

        create_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
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
        self.cursor.execute(create_query)
        self.conn.commit()
    
    def insert_checkin_data(self, mindfulness, diary, ABC_A, ABC_B, ABC_C, 
                            PLEASE_Physical_iLlness, PLEASE_balanced_Eating, 
                            PLEASE_mood_Altering_substances, PLEASE_Sleep, PLEASE_Exercise):
        """
        Insert a row into the checkin_data table.
        """
        table_name = f"checkin_data_{self.ID}"

        select_query = "SELECT NOW()"
        self.cursor.execute(select_query)
        timestamp = self.cursor.fetchall()

        insert_query = f"""
        INSERT INTO {table_name} ({timestamp}, mindfulness, diary, ABC_A, ABC_B, ABC_C, 
                            PLEASE_Physical_iLlness, PLEASE_balanced_Eating, 
                            PLEASE_mood_Altering_substances, PLEASE_Sleep, PLEASE_Exercise)
        VALUES ({timestamp}, mindfulness, diary, ABC_A, ABC_B, ABC_C, 
                            PLEASE_Physical_iLlness, PLEASE_balanced_Eating, 
                            PLEASE_mood_Altering_substances, PLEASE_Sleep, PLEASE_Exercise)
        """
        data = (mindfulness, diary, ABC_A, ABC_B, ABC_C, 
                            PLEASE_Physical_iLlness, PLEASE_balanced_Eating, 
                            PLEASE_mood_Altering_substances, PLEASE_Sleep, PLEASE_Exercise)
        self.cursor.execute(insert_query, data)
        self.conn.commit()

    def get_all_checkin_data(self):
        """
        Fetch all rows from checkin_data.
        """
        table_name = f"checkin_data_{self.ID}"

        # Fetch all rows from checkin_data.
        select_query = f"SELECT * FROM {table_name}"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()

    ## store user interactions
    ## unique table for each user
    def create_log_table(self):
        """
        Creates a table to store user interactions.
        """
        table_name = f"log_data_{self.ID}"
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            action VARCHAR(255),
            details TEXT
        )
        """
        self.cursor.execute(create_query)
        self.conn.commit()

    def insert_log_data(self, action, details):
        """
        Insert a row into the log_data table.
        """
        table_name = f"log_data_{self.ID}"

        insert_query = f"""
        INSERT INTO {table_name} (action, details)
        VALUES (%s, %s)
        """
        data = (action, details)
        self.cursor.execute(insert_query, data)
        self.conn.commit()

    def close(self):
        """
        Close the connection.
        """
        self.cursor.close()
        self.conn.close()