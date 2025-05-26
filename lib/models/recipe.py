from models.__init__ import CURSOR, CONN

class Recipe:
    
    all = {}

    def __init__(self, name, cuisine, time_to_prepare,food_quantity, id=None):
        self.id = id
        self.name = name
        self.cuisine = cuisine
        self.time_to_prepare = time_to_prepare
        self.food_quantity = food_quantity
    
    def __repr__(self):
        return f"<Recipe id={self.id} name='{self.name}' cuisine='{self.cuisine}' time_to_prepare='{self.time_to_prepare} Min/Hr' food_quantity='{self.food_quantity}'>"

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            name TEXT,
            cuisine TEXT,
            time_to_prepare INTEGER,
            food_quantity INTEGER)
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
            INSERT INTO recipes (name, cuisine, time_to_prepare, food_quantity)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.name, self.cuisine, self.time_to_prepare, self.food_quantity))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, cuisine, time_to_prepare, food_quantity):
        recipe = cls(name, cuisine, time_to_prepare, food_quantity)
        recipe.save()
        return recipe

    def update(self):
        sql = """
            UPDATE recipes
            SET name = ?, cuisine = ?, time_to_prepare = ?, food_quantity = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.cuisine, self.time_to_prepare, self.food_quantity))
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

    def get_recipe_ingredient():
        sql = """
            SELECT recipes.name, ingredients.name, ingredients.quantity, ingredients.unit
            FROM recipes
            INNER JOIN ingredients
            ON recipes.id = ingredients.recipe_id
            ORDER BY resipes.name
        """
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        