class Article:
    all = {}

    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f"<Article {self.id}: {self.title} (Author ID: {self.author_id}, Magazine ID: {self.magazine_id})>"

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author_id INTEGER,
                magazine_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES authors(id),
                FOREIGN KEY (magazine_id) REFERENCES magazines(id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS articles")
        CONN.commit()

    def save(self):
        sql = "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)"
        CURSOR.execute(sql, (self.title, self.author_id, self.magazine_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, title, author_id, magazine_id):
        article = cls(title, author_id, magazine_id)
        article.save()
        return article

    def update(self):
        sql = "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?"
        CURSOR.execute(sql, (self.title, self.author_id, self.magazine_id, self.id))
        CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM articles WHERE id = ?", (self.id,))
        CONN.commit()
        if self.id in Article.all:
            del Article.all[self.id]

    @classmethod
    def instance_from_db(cls, row):
        article = cls.all.get(row[0])
        if article:
            article.title = row[1]
            article.author_id = row[2]
            article.magazine_id = row[3]
        else:
            article = cls(row[1], row[2], row[3], row[0])
            cls.all[article.id] = article
        return article

    @classmethod
    def get_all(cls):
        rows = CURSOR.execute("SELECT * FROM articles").fetchall()
        return [cls.instance_from_db(row) for row in rows]
