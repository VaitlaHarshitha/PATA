import sqlite3


def create_database():

    conn = sqlite3.connect("pata.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_address TEXT,
        landmark TEXT,
        locality TEXT,
        city TEXT,
        latitude TEXT,
        longitude TEXT
    )
    """)

    conn.commit()
    conn.close()



def save_location(address, parsed, location):

    conn = sqlite3.connect("pata.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO locations
    (original_address, landmark, locality, city, latitude, longitude)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        address,
        ", ".join(parsed["landmark"]),
        parsed["locality"],
        parsed["city"],
        location["latitude"],
        location["longitude"]
    ))

    conn.commit()
    conn.close()



def get_locations():

    conn = sqlite3.connect("pata.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM locations")

    data = cursor.fetchall()

    conn.close()

    return data