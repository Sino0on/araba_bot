import sqlite3
from typing import Optional, List, Tuple

DB_PATH = "evacuation.db"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# Создание таблиц
cursor.execute('''
CREATE TABLE IF NOT EXISTS evacuations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate TEXT,
    brand TEXT,
    reason TEXT,
    from_location TEXT,
    to_location TEXT,
    media_file_id TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS watchers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    plate TEXT
)
''')

conn.commit()

# --- ФУНКЦИИ РАБОТЫ С ЭВАКУАЦИЯМИ --- #
def add_evacuation(plate: str, brand: str, reason: str, from_loc: str, to_loc: str, media_id: str):
    cursor.execute('''
        INSERT INTO evacuations (plate, brand, reason, from_location, to_location, media_file_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (plate, brand, reason, from_loc, to_loc, media_id))
    conn.commit()

def get_evacuation_by_plate(plate: str) -> List[Tuple]:
    cursor.execute('''
        SELECT id, plate, brand, reason, from_location, to_location, media_file_id, timestamp
        FROM evacuations
        WHERE plate = ?
        ORDER BY timestamp DESC
    ''', (plate,))
    return cursor.fetchall()

def get_all_unique_brands_by_plate(plate: str) -> List[str]:
    cursor.execute('''
        SELECT DISTINCT brand FROM evacuations WHERE plate = ?
    ''', (plate,))
    return [row[0] for row in cursor.fetchall()]

# --- ФУНКЦИИ РАБОТЫ С ПОДПИСЧИКАМИ --- #
def add_watcher(user_id: int, plate: str):
    cursor.execute('''
        INSERT INTO watchers (user_id, plate) VALUES (?, ?)
    ''', (user_id, plate))
    conn.commit()

def get_watchers_by_plate(plate: str) -> List[int]:
    cursor.execute('''
        SELECT user_id FROM watchers WHERE plate = ?
    ''', (plate,))
    return [row[0] for row in cursor.fetchall()]
