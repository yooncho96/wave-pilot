# data/db_helper.py

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

        global emotion_list 
        emotion_list = ['anger', 'sadness', 'fear', 'shame', 'guilt', 'jealousy', 'envy', 'joy', 'love']
            
    ## emotion data table
    ## unique table for each user
    def create_emotion_table(self):
        """
        Creates a table to store transcripts and emotion scores.
        """
        table_name = f"emotion_data_{ID}"

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
            sorted JSON,
            correct BOOLEAN,
            adjusted_main JSON
        )
        """
        self.cursor.execute(create_query)
        self.conn.commit()

    def insert_emotion_data(self, transcript, anger, sadness, fear, shame, guilt,
                            jealousy, envy, joy, love):
        """
        Insert a row into the emotion_data table.
        """
        select_query = "SELECT NOW()"
        self.cursor.execute(select_query)
        timestamp = self.cursor.fetchall()

        insert_query = """
            INSERT INTO %s (
                timestamp,
                transcript,
                anger,
                sadness,
                fear,
                shame,
                guilt,
                jealousy,
                envy,
                joy,
                love,
                sorted,
                correct,
                adjusted_main
            )
            VALUES (
                %s,   -- timestamp
                %s,   -- transcript
                %s,   -- anger
                %s,   -- sadness
                %s,   -- fear
                %s,   -- shame
                %s,   -- guilt
                %s,   -- jealousy
                %s,   -- envy
                %s,   -- joy
                %s,   -- love
                %s, -- sorted
                NULL, -- correct (forcing NULL)
                NULL  -- adjusted_top3 (forcing NULL)
            )
        """
        data = (timestamp, transcript, anger, sadness, fear, shame, guilt, jealousy, envy, joy, love)
        sorted_emotions = sorted(enumerate(data[2:]), key=lambda x: x[1], reverse=True)
        sorted_dict = {emotion_list[i]: data[1:][i] for i, _ in sorted_emotions}
        sorted_json = json.dumps(sorted_dict)

        data = data + (sorted_json,)

        self.cursor.execute(insert_query % f"emotion_data_{ID}", (data,))
        self.conn.commit()

    def get_current_idx(self):
        select_query = "SELECT id FROM %s ORDER BY id DESC LIMIT 1"
        self.cursor.execute(select_query, (f"emotion_data_{ID}",))
        idx = self.cursor.fetchall()[0][0]
        return idx

    def get_emotion_data(self):
        """
        Fetch the all emotions (SORTED) from the latest entry in the emotion_data table.
        """
        idx=self.get_current_idx()
        select_query = "SELECT sorted FROM %s WHERE id = %s"
        self.cursor.execute(select_query % f"emotion_data_{ID}", (idx,))
        sorted_json = self.cursor.fetchall()[0][0]
        sorted_dict = json.loads(sorted_json)

        return sorted_dict
    
    def get_all_emotion_data(self):
        """
        Fetch all rows from emotion_data.
        """
        # Fetch all rows from emotion_data.
        select_query = "SELECT * FROM %s"
        self.cursor.execute(select_query, (f"emotion_data_{ID}",))

        return self.cursor.fetchall()

    def save_feedback(self, correct):
        """
        Save user feedback on emotion scores.
        """
        idx=self.get_current_idx()
        update_query = """
            UPDATE %s
            SET correct = %s
            WHERE id = %s
            """
        self.cursor.execute(update_query % f"emotion_data_{ID}"(correct, idx))
        self.conn.commit()

    def adjust_emotion(self, adjustment):   
        """
        Update emotion scores based on user feedback.
        `adjustment` is a tuple of (name, value)
        """
        idx=self.get_current_idx()
        self.save_feedback(False)
        adjustment_json = json.dumps(adjustment)

        update_query = """
            UPDATE %s
            SET adjusted_main = %s
            WHERE id = %s
            """
        self.cursor.execute(update_query % f"emotion_data_{ID}", (adjustment_json, idx))
        self.conn.commit()

        return adjustment
    
    def get_adjusted_main(self):
        """
        Fetch the adjusted emotion scores from the latest entry in the emotion_data table.
        """
        idx=self.get_current_idx()
        select_query = "SELECT adjusted_main FROM %s WHERE id = %s"
        self.cursor.execute(select_query % f"emotion_data_{ID}", (idx,))
        adjusted_main_json = self.cursor.fetchall()[0][0]
        adjusted_main = json.loads(adjusted_main_json)
        return adjusted_main
    
    def get_final_key_emotion(self):
        emotions = self.get_emotion_data()
        if emotions[12]:
            emotion, score = emotions[11].items()[0]
        else:
            adjusted = self.get_adjusted_main()
            emotion, score = adjusted.items()[0]
        return emotion, score
    
    ## store selected skills data table
    ## unique table for each user
    def create_mindfulness_table(self):
        """
        Creates a table to store selected mindfulness skills data.
        """
        create_query = """
        CREATE TABLE IF NOT EXISTS %s (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp TIMESTAMP,
            Paced_breathing BOOLEAN,
            Box_breathing BOOLEAN,
            Focusing_on_exhales BOOLEAN,
            Counting_down_from_10 BOOLEAN,
            Narrate_a_task BOOLEAN,
            Blindfolded_movement_taste BOOLEAN,
            Mindful_eating BOOLEAN,
            Search_for_that_color BOOLEAN,
            Search_for_that_shape BOOLEAN,
            Learning_from_an_animal_friend BOOLEAN,
            5_4_3_2_1 BOOLEAN,
            Coloring BOOLEAN,
            Doodling BOOLEAN,
            Taking_a_walk BOOLEAN,
            Cooking BOOLEAN,
            Dancing BOOLEAN,
            Puzzles BOOLEAN,
            Light_a_candle BOOLEAN,
            Body_Scan BOOLEAN,
            Set_up_mantras BOOLEAN,
            Journaling BOOLEAN,
            List_of_Gratitude BOOLEAN
        )
        """
        self.cursor.execute(create_query, (f"mindfulness_skills_{ID}",))
        self.conn.commit()

    def set_preferred_mindfulness(self, skill_list):
        """
        Add selected skill to list of preferred skills saved in mindfulness.
        """
        table_name = f"mindfulness_skills_{ID}"

        select_query = "SELECT NOW()"
        self.cursor.execute(select_query)
        timestamp = self.cursor.fetchall()

        for skill in skill_list:
            if skill not in self.cursor.column_names:
                alter_query = "ALTER TABLE %s ADD COLUMN %s BOOLEAN"
                skill = f"Other_{skill}"
                self.cursor.execute(alter_query % {table_name}, (skill,))
        
        columns = self.cursor.column_names
        values = [True if col in skill_list else False for col in columns]
        insert_query = f"INSERT INTO %s (timestamp, {', '.join(columns)}) VALUES (%s, {', '.join(['%s'] * len(columns))}))"
        self.cursor.execute(insert_query % {table_name}, ((timestamp,) + values,))
        self.conn.commit()

    def get_mindfulness(self):
        """
        Get latest entry of `mindfulness`
        """
        table_name = f"mindfulness_skills_{ID}"
        select_query = "SELECT * FROM %s ORDER BY id DESC LIMIT 1"
        self.cursor.execute(select_query % {table_name})
        columns = [desc[0] for desc in self.cursor.description]
        row = self.cursor.fetchone()
        result = dict(zip(columns, row))
        return result
    
    def create_distress_tolerance_table(self):
        """
        Creates a table to store selected distress tolerance skills data.
        """
        create_query = """
        CREATE TABLE IF NOT EXISTS %s (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp TIMESTAMP,
            TIPP_skills_Temperature_Ice_diving BOOLEAN, 
            TIPP_skills_Intense_exercise BOOLEAN, 
            TIPP_skills_Paced_breathing BOOLEAN,
            TIPP_skills_Progressive_muscle_relaxation BOOLEAN,
            STOP BOOLEAN,
            SelfSoothing_Sight TEXT,
            SelfSoothing_Sound TEXT,
            SelfSoothing_Touch TEXT,
            SelfSoothing_Smell TEXT,
            SelfSoothing_Taste TEXT,
            Pros_and_Cons BOOLEAN
        )
        """
        self.cursor.execute(create_query, (f"distress_tolerance_{ID}",))
        self.conn.commit()

    def set_preferred_distress_tolerance(self, skill_list):
        """
        Add selected skill to list of preferred skills saved in distress_tolerance.
        """
        table_name = f"distress_tolerance_{ID}"

        select_query = "SELECT NOW()"
        self.cursor.execute(select_query)
        timestamp = self.cursor.fetchall()

        columns = self.cursor.column_names
        for skill in skill_list:
            if skill not in columns:
                alter_query = "ALTER TABLE %s ADD COLUMN %s BOOLEAN"
                self.cursor.execute(alter_query % {table_name}, (skill,))
        
        values = [True if col in skill_list else False for col in columns]
        insert_query = f"INSERT INTO %s (timestamp, {', '.join(columns)}) VALUES (%s, {', '.join(['%s'] * len(columns))}))"
        self.cursor.execute(insert_query % {table_name}, ((timestamp,) + values,))
        self.conn.commit()

    def get_distress_tolerance(self):
        """
        Get latest entry of `distress_tolerance`
        """
        table_name = f"distress_tolerance_{ID}"
        select_query = "SELECT * FROM %s ORDER BY id DESC LIMIT 1"
        self.cursor.execute(select_query % {table_name})
        columns = [desc[0] for desc in self.cursor.description]
        row = self.cursor.fetchone()
        result = dict(zip(columns, row))
        return result

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
        self.cursor.execute(create_query, (f"checkin_data_{ID}",))
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
            f"checkin_data_{ID}",
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
        self.cursor.execute(select_query, (f"checkin_data_{ID}",))
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
        self.cursor.execute(create_query, (f"log_data_{ID}",))
        self.conn.commit()

    def insert_log_data(self, action, details):
        """
        Insert a row into the log_data table.
        """
        insert_query = """
        INSERT INTO %s (action, details)
            VALUES (%s, %s)
        """
        data = (f"log_data_{ID}",action, details)
        self.cursor.execute(insert_query, data)
        self.conn.commit()

    def close(self):
        """
        Close the connection.
        """
        self.cursor.close()
        self.conn.close()