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

class UserHelper:
    """
    Manages database connection and queries using SSL.
    This database stores user information to use when logging in
    Saves id to be used as a foreign key in all screens
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

    ## User data table

    def create_user_table(self):

        create_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            id INT PRIMARY KEY AUTO_INCREMENT,
            password VARCHAR(50),
            code VARCHAR(4),
            email VARCHAR(100),
            phone VARCHAR(20),  # in format ###-###-####
            street_address VARCHAR(255),
            city VARCHAR(255),
            state VARCHAR(2),
            zip_code VARCHAR(5),
            crisis_name VARCHAR(100),
            crisis_relationship VARCHAR(100),
            crisis_phone VARCHAR(20)   # in format ###-###-####
        )
        """
        self.cursor.execute(create_query)
        self.conn.commit()
        global ID 
        ID = None
        
    def set_pw(self, id, password):     # user will set the pw; other fields will be set by admin
        """
        User sets password.
        """
        update_query = "UPDATE user_data SET password = %s WHERE id = %s"
        self.cursor.execute(update_query, (password, id))
        self.conn.commit()
        ID = id

    def find_matching_user(self, id, email):
        """
        find user that has id & email, return boolean
        """
        select_query = "SELECT email FROM user_data WHERE id = (%s)"
        self.cursor.execute(select_query, (id,))
        true_email = self.cursor.fetchall()[0][0]
        if email == true_email:
            ID = id
            return True
        else:
            return False

    def reset_code(self,code):
        ID = self.lost_pw_email()[1]
        update_query = "UPDATE user_data SET code = %s WHERE id = {ID}"
        self.cursor.execute(update_query, (code, ))
        self.conn.commit()

    def login(self, code):
        select_query = "SELECT code FROM user_data WHERE id = {ID}"
        self.cursor.execute(select_query)
        true_code = self.cursor.fetchall()[0][0]
        if code == true_code:
            return True
        else:
            return False

    def set_code(self, code):
        """
        Set code for user.
        """
        update_query = "UPDATE user_data SET code = %s WHERE id = {ID}"
        self.cursor.execute(update_query, (code, ))
        self.conn.commit()

    def get_password(self):
        select_query = "SELECT password FROM user_data WHERE id = {ID}"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()[0][0]
    
    def get_user_data(self):
        """
        Fetch all data from table.
        """
        select_query = f"SELECT * FROM user_data WHERE id = {ID}"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()
    
    def set_crisis_contact(self, name, relationship, phone):
        """
        Set crisis contact for user.
        """
        update_query = "UPDATE user_data SET crisis_name = %s, crisis_relationship = %s, crisis_phone = %s WHERE id = {ID}"
        self.cursor.execute(update_query, (name, relationship, phone))
        self.conn.commit()
    
    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()

    def logout(self):
        ID = None
        self.close()