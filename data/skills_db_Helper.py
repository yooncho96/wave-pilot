# data/skills_db_helper.py

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
        self.cursor.execute(create_query, (f"mindfulness_skills_{self.ID}",))
        self.conn.commit()

    def set_preferred_mindfulness(self, skill_list):
        """
        Add selected skill to list of preferred skills saved in mindfulness.
        """
        table_name = f"mindfulness_skills_{self.ID}"

        select_query = "SELECT NOW()"
        self.cursor.execute(select_query)
        timestamp = self.cursor.fetchall()

        for skill in skill_list:
            if skill not in self.cursor.column_names:
                alter_query = "ALTER TABLE %s ADD COLUMN %s BOOLEAN"
                skill = f"Other_{skill}"
                self.cursor.execute(alter_query % table_name, (skill,))
        
        columns = self.cursor.column_names
        values = [True if col in skill_list else False for col in columns]
        insert_query = f"INSERT INTO %s (timestamp, {', '.join(columns)}) VALUES (%s, {', '.join(['%s'] * len(columns))}))"
        self.cursor.execute(insert_query % table_name, ((timestamp,) + values,))
        self.conn.commit()

    def get_mindfulness(self):
        """
        Get latest entry of `mindfulness`
        """
        table_name = f"mindfulness_skills_{self.ID}"
        select_query = "SELECT * FROM %s ORDER BY id DESC LIMIT 1"
        self.cursor.execute(select_query % table_name)
        columns = [desc[0] for desc in self.cursor.description]
        row = self.cursor.fetchone()
        result = dict(zip(columns, row))
        return result
    
    def create_distress_tolerance_table(self):
        """
        Creates a table to store selected distress tolerance skills data
        Creates a second table to store assigned probabilities
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
            SelfSoothing_Sight BOOLEAN,
            SelfSoothing_Sound BOOLEAN,
            SelfSoothing_Touch BOOLEAN,
            SelfSoothing_Smell BOOLEAN,
            SelfSoothing_Taste BOOLEAN,
            Detail_SelfSoothing_Sight TEXT,
            Detail_SelfSoothing_Sound TEXT,
            Detail_SelfSoothing_Touch TEXT,
            Detail_SelfSoothing_Smell TEXT,
            Detail_SelfSoothing_Taste TEXT,
            Pros_and_Cons BOOLEAN
        )
        """
        self.cursor.execute(create_query, (f"distress_tolerance_{self.ID}",))
        self.conn.commit()

    def set_preferred_distress_tolerance(self, skill_list: list, details_list: list):
        """
        Add selected skill to list of preferred skills saved in distress_tolerance.
        """
        table_name = f"distress_tolerance_{self.ID}"

        select_query = "SELECT NOW()"
        self.cursor.execute(select_query)
        timestamp = self.cursor.fetchall()

        columns = self.cursor.column_names
        for skill in skill_list:
            if skill not in columns:
                alter_query = "ALTER TABLE %s ADD COLUMN %s BOOLEAN"
                self.cursor.execute(alter_query % table_name, (skill,))
        
        values = [True if col in skill_list else False for col in columns]
        insert_query = f"INSERT INTO %s (timestamp, {', '.join(columns)}) VALUES (%s, {', '.join(['%s'] * len(columns))}))"
        self.cursor.execute(insert_query % table_name, ((timestamp, *values,)))
        self.conn.commit()

        # details for self-soothing
        idx = self.get_current_idx("disstress_tolerance")
        update_query = """
            UPDATE %s
            SET (
                Detail_SelfSoothing_Sight,
                Detail_SelfSoothing_Sound,
                Detail_SelfSoothing_Touch,
                Detail_SelfSoothing_Smell,
                Detail_SelfSoothing_Taste
                ) = (*%s,)
            WHERE id = %s
            """
        self.cursor.execute(update_query % table_name, (*details_list, idx))
        self.conn.commit()

    def get_distress_tolerance(self):
        """
        Get latest entry of `distress_tolerance`
        includes "Details_"
        """
        table_name = f"distress_tolerance_{self.ID}"
        select_query = "SELECT * FROM %s ORDER BY id DESC LIMIT 1"
        self.cursor.execute(select_query % table_name)
        columns = [desc[0] for desc in self.cursor.description]
        row = self.cursor.fetchone()
        result = dict(zip(columns, row))
        return result
    
    def create_DistTol_prob_table(self):
        """
        Creates a table to store probabilities for distress tolerance skills.
        Called when DT skills are first selected and every time probabilities are updated.
        """

        select_query = "SELECT column_name FROM information_schema.columns WHERE table_name = %s"
        self.cursor.execute(select_query, (f"distress_tolerance_{self.ID}",))
        columns = [row[0] for row in self.cursor.fetchall()]

        row = self.get_distress_tolerance().keys()
        colnames = []
        for i in range(len(columns)):
            if isinstance(row[i], str):
                skill_values = row[i].split(',')
                for skill_value in skill_values:
                    cat = columns[i].replace("Details_","")
                    colnames.append(f"{cat}_{skill_value.strip()}")
            elif row[i]==True:
                if columns[i].startswith("SelfSoothing"): continue
                colnames.append(columns[i])

        query_col = "id INT AUTO_INCREMENT PRIMARY KEY, timestamp TIMESTAMP, reference INT"
        for col in colnames:
            query_col += f", {col} FLOAT"
        create_query = "CREATE TABLE IF NOT EXISTS %s (%s)"
        self.cursor.execute(create_query, (f"DistTol_prob_{self.ID}", query_col))
        self.conn.commit()

        # Check for new columns and alter table if necessary
        self.cursor.execute(select_query, (f"DistTol_prob_{self.ID}",))
        existing_columns = [row[0] for row in self.cursor.fetchall()]

        for col in colnames:
            if col not in existing_columns:
                alter_query = "ALTER TABLE %s ADD COLUMN %s FLOAT"
                self.cursor.execute(alter_query % (f"DistTol_prob_{self.ID}", col))
                self.conn.commit()

        table_name = f"DistTol_prob_{self.ID}"

        # Initialize probabilities for the first entry
        if self.get_current_idx("DistTol_prob") is None:
            idx = self.get_current_idx("distress_tolerance")
            select_query = "SELECT NOW()"
            self.cursor.execute(select_query)
            timestamp = self.cursor.fetchall()[0][0]

            # Calculate initial probabilities
            init_probs = []
            for col in colnames:
                if col.startswith("SelfSoothing_"):
                    sense = col.split("_")[1]
                    details_col = f"Detail_SelfSoothing_{sense}"
                    self.cursor.execute(f"SELECT {details_col} FROM distress_tolerance_{self.ID} WHERE id = {idx}")
                    details = self.cursor.fetchone()[0]
                    n = len(details.split(',')) if details else 1
                    init_probs.append((1/len(colnames)) / n)
                else:
                    init_probs.append(1 / len(colnames))

            insert_query = "INSERT INTO %s (timestamp, reference, %s) VALUES (%s, %s, %s)"
            values = [timestamp, idx] + init_probs
            self.cursor.execute(insert_query % (table_name, ', '.join(colnames), '%s, %s, ' + ', '.join(['%s'] * len(init_probs))), values)
            self.conn.commit()
        
    def get_DistTol_probs(self):
        """
        Get the last row of DistTol_probs and return a dictionary 
        with keys as column names that have non-null values and values as the cell values.
        """
        table_name = f"DistTol_prob_{self.ID}"
        select_query = f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 1"
        self.cursor.execute(select_query)
        row = self.cursor.fetchone()
        if row:
            columns = [desc[0] for desc in self.cursor.description]
            columns = [col for i, col in enumerate(columns) if row[i]]
            result = {columns[i]: row[i] for i in range(len(row)) if row[i] is not None and row[i] is True}
            return result
        return LookupError

    def update_prob(self, swipe_record: dict):
        """
        swipe_record is a dict:
        keys = skill names (True columns from distress_tolerance)
        values = str, "Dislike", "Cannot", or "Like"
        """
        prev_dict = self.get_DistTol_probs() 
        updated_dict = prev_dict.copy()

        # 1) Group skills by their "sense" (or top-level grouping)
        #    e.g. group_key = "SelfSoothing_Smell", sub_key = "ScentedCandle"
        groups = {}
        for skill_name, prob in prev_dict.items():
            if skill_name.startswith("SelfSoothing_"):
                parts = skill_name.split("_", 2)
                group_key = "_".join(parts[:2]) 
            else:
                group_key = skill_name  # skill has no sub-detail
            groups.setdefault(group_key, []).append(skill_name)

        # 2) Figure out scale factors for each group based on user swipes
        group_scale = {}
        for skill_name, swipe in swipe_record.items():
            if swipe == "Like":
                factor = 1.05
            elif swipe == "Dislike":
                factor = 0.95
            else:  # "Cannot"
                factor = 1.0
            
            # Find this skill's group
            if skill_name.startswith("SelfSoothing_"):
                parts = skill_name.split("_", 2)
                gkey = "_".join(parts[:2])
            else:
                gkey = skill_name
            
            # Combine factors if multiple sub‐skills in the same group were rated
            existing_factor = group_scale.get(gkey, 1.0)
            group_scale[gkey] = existing_factor * factor

        # 3) Apply group scaling to each sub‐skill in that group
        for gkey, subskills in groups.items():
            # The factor for the group, or 1.0 if no skill in group was updated
            factor = group_scale.get(gkey, 1.0)
            # Sum of sub‐skills for the group
            total_group_prob = sum(prev_dict[subsk] for subsk in subskills)
            
            if total_group_prob == 0.0:
                continue
            
            # Scale entire group
            for subsk in subskills:
                # preserve the ratio subsk_prob / total_group_prob
                ratio = prev_dict[subsk] / total_group_prob
                # new total for group = total_group_prob * factor
                updated_dict[subsk] = ratio * (total_group_prob * factor)
        
        # Global normalization so everything sums to 1
        total_prob = sum(updated_dict.values())
        if total_prob > 0:
            for k in updated_dict:
                updated_dict[k] = updated_dict[k] / total_prob

        return updated_dict