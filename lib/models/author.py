from __init__ import CURSOR, CONN

class Author:
    all = {}

    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author {self.id}: {self.name}>"

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS authors")
        CONN.commit()

    def save(self):
        sql = "INSERT INTO authors (name) VALUES (?)"
        CURSOR.execute(sql, (self.name,))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name):
        author = cls(name)
        author.save()
        return author

    def update(self):
        sql = "UPDATE authors SET name = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM authors WHERE id = ?", (self.id,))
        CONN.commit()
        if self.id in Author.all:
            del Author.all[self.id]

    @classmethod
    def instance_from_db(cls, row):
        author = cls.all.get(row[0])
        if author:
            author.name = row[1]
        else:
            author = cls(row[1], row[0])
            cls.all[author.id] = author
        return author

    @classmethod
    def get_all(cls):
        rows = CURSOR.execute("SELECT * FROM authors").fetchall()
        return [cls.instance_from_db(row) for row in rows]
