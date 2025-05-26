from __init__ import CURSOR, CONN
from article import Article

class Magazine:
    all = {}

    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Magazine {self.id}: {self.name}, {self.category}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 1 <= len(value) <= 255:
            self._name = value
        else:
            raise ValueError("Magazine name must be a non-empty string under 255 characters.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and 1 <= len(value) <= 255:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string under 255 characters.")

    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL
            );
        """)
        CONN.commit()

    def save(self):
        if self.id:
            self.update()
        else:
            CURSOR.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
            CONN.commit()
            self.id = CURSOR.lastrowid
            type(self).all[self.id] = self

    def update(self):
        CURSOR.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", (self.name, self.category, self.id))
        CONN.commit()

    @classmethod
    def find_by_id(cls, id):
        row = CURSOR.execute("SELECT * FROM magazines WHERE id = ?", (id,)).fetchone()
        return cls(row[1], row[2], row[0]) if row else None

    @classmethod
    def find_by_name(cls, name):
        row = CURSOR.execute("SELECT * FROM magazines WHERE name = ?", (name,)).fetchone()
        return cls(row[1], row[2], row[0]) if row else None

    @classmethod
    def find_by_category(cls, category):
        rows = CURSOR.execute("SELECT * FROM magazines WHERE category = ?", (category,)).fetchall()
        return [cls(row[1], row[2], row[0]) for row in rows]

    def articles(self):
        return Article.find_by_magazine(self.id)

    def contributors(self):
        return list({article.author() for article in self.articles()})
