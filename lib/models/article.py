from __init__ import CURSOR, CONN
from author import Author
from magazine import Magazine

class Article:
    all = {}

    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f"<Article {self.id}: {self.title}>"

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, str) and 1 <= len(value) <= 255:
            self._title = value
        else:
            raise ValueError("Title must be a non-empty string under 255 characters.")

    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author_id INTEGER,
                magazine_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES authors(id),
                FOREIGN KEY (magazine_id) REFERENCES magazines(id)
            );
        """)
        CONN.commit()

    def save(self):
        if self.id:
            self.update()
        else:
            CURSOR.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (self.title, self.author_id, self.magazine_id)
            )
            CONN.commit()
            self.id = CURSOR.lastrowid
            type(self).all[self.id] = self

    def update(self):
        CURSOR.execute(
            "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
            (self.title, self.author_id, self.magazine_id, self.id)
        )
        CONN.commit()

    @classmethod
    def find_by_id(cls, id):
        row = CURSOR.execute("SELECT * FROM articles WHERE id = ?", (id,)).fetchone()
        return cls(row[1], row[2], row[3], row[0]) if row else None

    @classmethod
    def find_by_title(cls, title):
        row = CURSOR.execute("SELECT * FROM articles WHERE title = ?", (title,)).fetchone()
        return cls(row[1], row[2], row[3], row[0]) if row else None

    @classmethod
    def find_by_author(cls, author_id):
        rows = CURSOR.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,)).fetchall()
        return [cls(row[1], row[2], row[3], row[0]) for row in rows]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        rows = CURSOR.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,)).fetchall()
        return [cls(row[1], row[2], row[3], row[0]) for row in rows]

    def author(self):
        return Author.find_by_id(self.author_id)

    def magazine(self):
        return Magazine.find_by_id(self.magazine_id)
