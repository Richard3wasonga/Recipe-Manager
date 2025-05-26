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

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY,
            name TEXT,
            quantity REAL,
            unit TEXT,
            recipe_id INTEGER,
            FOREIGN KEY(recipe_id) REFERENCES recepies(id))

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
    
