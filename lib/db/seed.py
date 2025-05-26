from lib.db.connection import get_connection

def seed():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript(open("lib/db/schema.sql").read())

    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Rio",))
    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Alice",))

    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Tech Weekly", "Technology"))
    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Health Digest", "Health"))

    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                   ("The Rise of AI", 1, 1))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                   ("Staying Fit", 2, 2))

    conn.commit()
    conn.close()
