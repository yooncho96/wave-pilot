# data/db_helper.py

import mysql.connector
import os

# If you need to handle environment variables or load .env, do so here.
# from dotenv import load_dotenv
# load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'YOUR_CLOUD_SQL_HOST')
DB_USER = os.getenv('DB_USER', 'YOUR_DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'YOUR_DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME', 'YOUR_DB_NAME')
DB_PORT = int(os.getenv('DB_PORT', '3306'))

# SSL certificate paths
SSL_CA_PATH   = os.getenv('SSL_CA_PATH', 'ssl/server-ca.pem')
SSL_CERT_PATH = os.getenv('SSL_CERT_PATH', 'ssl/client-cert.pem')
SSL_KEY_PATH  = os.getenv('SSL_KEY_PATH', 'ssl/client-key.pem')


class DBHelper:
    """
    Manages database connection and queries using SSL.
    """

    def __init__(self):
        self.conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            ssl_ca=SSL_CA_PATH,
            ssl_cert=SSL_CERT_PATH,
            ssl_key=SSL_KEY_PATH
        )
        self.cursor = self.conn.cursor()

    def create_emotion_table(self):
        """
        Creates a table to store transcripts and emotion scores.
        """
        create_query = """
        CREATE TABLE IF NOT EXISTS emotion_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            transcript TEXT,
            anger FLOAT,
            sadness FLOAT,
            fear FLOAT,
            shame FLOAT,
            guilt FLOAT,
            jealousy FLOAT,
            envy FLOAT,
            joy FLOAT,
            love FLOAT
        )
        """
        self.cursor.execute(create_query)
        self.conn.commit()

    def insert_emotion_data(self, transcript, anger, sadness, fear, shame, guilt,
                            jealousy, envy, joy, love):
        """
        Insert a row into the emotion_data table.
        """
        insert_query = """
        INSERT INTO emotion_data
            (transcript, anger, sadness, fear, shame, guilt, jealousy, envy, joy, love)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (transcript, anger, sadness, fear, shame, guilt, jealousy, envy, joy, love)
        self.cursor.execute(insert_query, data)
        self.conn.commit()

    def get_all_emotion_data(self):
        """
        Fetch all rows from emotion_data.
        """
        select_query = "SELECT * FROM emotion_data"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()

    def close(self):
        """
        Close the database connection.
        """
        self.cursor.close()
        self.conn.close()
