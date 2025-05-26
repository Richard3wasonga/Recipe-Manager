from models.__init__ import CURSOR, CONN

class Recipe:
    
    all = {}

    def __init__(self, name, cuisine, time_to_prepare, id=None):
        self.id = id
        self.name = name
        self.cuisine = cuisine
        self.time_to_prepare = time_to_prepare
    
    def __repr__(self):
        return f"<Recipe id={self.id} food_name='{self.name}' cuisine='{self.cuisine}' time_required='{self.time_to_prepare} Min/Hr'>"

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            name TEXT,
            cuisine TEXT,
            time_to_prepare INTEGER)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS recipes;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO recipes (name, cuisine, time_to_prepare)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.name, self.cuisine, self.time_to_prepare))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, cuisine, time_to_prepare):
        recipe = cls(name, cuisine, time_to_prepare)
        recipe.save()
        return recipe

    def update(self):
        sql = """
            UPDATE recipes
            SET name = ?, cuisine = ?, time_to_prepare = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.cuisine, self.time_to_prepare))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM recipes
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None