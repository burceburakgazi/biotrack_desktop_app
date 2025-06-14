import sqlite3
from datetime import datetime
from typing import List, Optional
from data.models import BiometricReading

class DatabaseManager:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                glucose REAL NOT NULL,
                ph REAL NOT NULL,
                oxygen REAL NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id TEXT PRIMARY KEY,
                esp32_ip TEXT DEFAULT '192.168.4.1',
                language TEXT DEFAULT 'EN',
                theme TEXT DEFAULT 'light',
                glucose_threshold_min REAL DEFAULT 70,
                glucose_threshold_max REAL DEFAULT 140,
                ph_threshold_min REAL DEFAULT 6.5,
                ph_threshold_max REAL DEFAULT 7.5,
                oxygen_threshold_min REAL DEFAULT 90
            )
        ''')

        conn.commit()
        conn.close()

    def save_reading(self, user_id: str, reading: BiometricReading):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO readings (user_id, timestamp, glucose, ph, oxygen)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, reading.timestamp.isoformat(), reading.glucose, reading.ph, reading.oxygen))

        conn.commit()
        conn.close()

    def get_readings(self, user_id: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[BiometricReading]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        query = "SELECT timestamp, glucose, ph, oxygen FROM readings WHERE user_id = ?"
        params = [user_id]

        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date.isoformat())

        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date.isoformat())

        query += " ORDER BY timestamp DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [BiometricReading(row[0], row[1], row[2], row[3]) for row in rows]

    def export_to_csv(self, user_id: str, filename: str):
        readings = self.get_readings(user_id)

        with open(filename, 'w', newline='') as csvfile:
            csvfile.write("Timestamp,Glucose,pH,Oxygen\n")
            for reading in readings:
                csvfile.write(f"{reading.timestamp},{reading.glucose},{reading.ph},{reading.oxygen}\n")
