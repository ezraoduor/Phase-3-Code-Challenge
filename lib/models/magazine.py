class Magazine:
    all = {}

    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Magazine {self.id}: {self.name}, {self.category}>"

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS magazines")
        CONN.commit()

    def save(self):
        sql = "INSERT INTO magazines (name, category) VALUES (?, ?)"
        CURSOR.execute(sql, (self.name, self.category))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, category):
        magazine = cls(name, category)
        magazine.save()
        return magazine

    def update(self):
        sql = "UPDATE magazines SET name = ?, category = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.category, self.id))
        CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM magazines WHERE id = ?", (self.id,))
        CONN.commit()
        if self.id in Magazine.all:
            del Magazine.all[self.id]

    @classmethod
    def instance_from_db(cls, row):
        magazine = cls.all.get(row[0])
        if magazine:
            magazine.name = row[1]
            magazine.category = row[2]
        else:
            magazine = cls(row[1], row[2], row[0])
            cls.all[magazine.id] = magazine
        return magazine

    @classmethod
    def get_all(cls):
        rows = CURSOR.execute("SELECT * FROM magazines").fetchall()
        return [cls.instance_from_db(row) for row in rows]
