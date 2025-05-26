from __init__ import CURSOR, CONN
from article import Article  

class Author:
    all = {}

    def __init__(self, name, id=None):
        self.id = id
        self.name = name  

    def __repr__(self):
        return f"<Author {self.id}: {self.name}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 1 <= len(value) <= 255:
            self._name = value
        else:
            raise ValueError("Author name must be a non-empty string under 255 characters.")

    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
        """)
        CONN.commit()

    def save(self):
        if self.id:
            self.update()
        else:
            CURSOR.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            CONN.commit()
            self.id = CURSOR.lastrowid
            type(self).all[self.id] = self

    def update(self):
        CURSOR.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
        CONN.commit()

    @classmethod
    def find_by_id(cls, id):
        row = CURSOR.execute("SELECT * FROM authors WHERE id = ?", (id,)).fetchone()
        return cls(row[1], row[0]) if row else None

    @classmethod
    def find_by_name(cls, name):
        row = CURSOR.execute("SELECT * FROM authors WHERE name = ?", (name,)).fetchone()
        return cls(row[1], row[0]) if row else None

    def articles(self):
        from article import Article
        return Article.find_by_author(self.id)

    def magazines(self):
        return list({article.magazine() for article in self.articles()})
