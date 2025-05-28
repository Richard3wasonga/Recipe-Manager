from models.__init__ import CURSOR, CONN

class Ingredient:

    def __init__(self, name, quantity, unit, recipe_id, id=None):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.recipe_id = recipe_id

    def __repr__(self):
        return f"<Ingrident name={self.name}  quantity={self.quantity} unit={self.unit} recipe_id={self.recipe_id} >"

     
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string.")
        self._name = value.strip()

    
    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Quantity must be a non-negative number.")
        self._quantity = value

    
    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Unit must be a non-empty string.")
        self._unit = value.strip()

    
    @property
    def recipe_id(self):
        return self._recipe_id

    @recipe_id.setter
    def recipe_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Recipe ID must be an integer.")
        self._recipe_id = value


    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY,
            name TEXT,
            quantity REAL,
            unit TEXT,
            recipe_id INTEGER,
            FOREIGN KEY(recipe_id) REFERENCES recipes(id))

        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS ingredients;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO ingredients (name, quantity, unit, recipe_id)
            VALUES(?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.name, self.quantity, self.unit,self.recipe_id))
        CONN.commit()

        self.id =CURSOR.lastrowid

    @classmethod
    def create(cls, name, quantity, unit, recipe_id):
       ingredient = cls(name, quantity, unit, recipe_id)
       ingredient.save()
       return ingredient

    def delete(self):
        if not self.id:
            print("Ingredient not saved in database.")
            return

        sql = """
            DELETE FROM ingredients
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        print(f"Ingredient '{self.name}' deleted successfully.")
        self.id = None

    @classmethod
    def delete_by_recipe_id(cls, recipe_id):
        sql = "DELETE FROM ingredients WHERE recipe_id = ?"
        CURSOR.execute(sql, (recipe_id,))
        CONN.commit()
        print(f"All ingredients for recipe ID {recipe_id} deleted.")

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * 
            FROM ingredients 
            WHERE id = ?
        """
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls(id=row[0], name=row[1], quantity=row[2], unit=row[3], recipe_id=row[4])
        return None

    
