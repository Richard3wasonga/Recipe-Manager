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
        return f"<Recipe id={self.id} name='{self.name}' cuisine='{self.cuisine}' time_to_prepare='{self.time_to_prepare} Min' food_quantity='{self.food_quantity}'>"

    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string.")
        self._name = value.strip()

    
    @property
    def cuisine(self):
        return self._cuisine

    @cuisine.setter
    def cuisine(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Cuisine must be a non-empty string.")
        self._cuisine = value.strip()

    
    @property
    def time_to_prepare(self):
        return self._time_to_prepare

    @time_to_prepare.setter
    def time_to_prepare(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Time to prepare must be a non-negative integer.")
        self._time_to_prepare = value

    
    @property
    def food_quantity(self):
        return self._food_quantity

    @food_quantity.setter
    def food_quantity(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Food quantity must be a positive integer.")
        self._food_quantity = value


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
        CURSOR.execute(sql, (self.name, self.cuisine, self.time_to_prepare, self.food_quantity, self.id))
        CONN.commit()

    def delete(self):
        if not self.id:
            print("Recipe not saved or already deleted.")
            return

        sql = """
            DELETE FROM recipes
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        if hasattr(type(self), "all") and self.id in type(self).all:
            del type(self).all[self.id]

        self.id = None
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM recipes
            WHERE id = ?
        """
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        return cls(id=row[0], name=row[1], cuisine=row[2], time_to_prepare=row[3], food_quantity=row[4]) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM recipes
            WHERE LOWER(name) = LOWER(?)
        """
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        return cls(id=row[0], name=row[1], cuisine=row[2], time_to_prepare=row[3], food_quantity=row[4]) if row else None

    def get_ingredients(self):
        sql = """
            SELECT name, quantity, unit
            FROM ingredients
            WHERE recipe_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        return CURSOR.fetchall()

    
