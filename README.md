
# **Recipe Manager**

![Python](https://img.shields.io/badge/python-3.10-blue)
![License](https://img.shields.io/badge/license-MIT-green)


A powerful, easy-to-use **command-line application** to organize your recipes and thier ingredients.Designed to help home cooks,chefs and food enthusiasts manage thier recipe collections effortlessly, from creating new recipes to scaling ingredient quantity based on servings.

## **Installation**

GITHUB REPOSITORY: [ recipe-management-system](https://github.com/Richard3wasonga/Recipe-Manager)

1. Clone this repository:
   ```bash
   git clone https://github.com/Richard3wasonga/Recipe-Manager 
   ```

2. Navigate to the project directory:
   ```bash
   cd recipe-manager
   ```

3. Install required python packages:
   ```bash
   pipenv install colorama tabulate
   ```

4. Make the CLI script executable:
   ```bash
   chmod +x lib/cli.py
   ```

5. Run the CLI application directly from the terminal:
   ```bash
   ./lib/cli.py
   ```

---

## **Features**

- **create,update and delete recipes** with ease.

- **Add,view and delete ingredients** linked to recipes.

- **Search recipes** by ID or name.

- **Display ingredients** for any recipe.

- **Scale ingredient quantities** dynamically based on desired food servings.

- **Reset database tables** to clear all data and start fresh.

- **Intuitive,colorful and interactive CLI interface** with helpful prompts and tables.

- **Auto-clearing terminal output**: The terminal screen **automatically clears after each operation**, ensuring a clean and clutter-free interface for better readability and focus.

## **classes: Recipe & Ingredient**

### **Recipe**

Represents a cooking recipe, storing details like:

- `id`: Unique database identifier.

- `name`: The recipe's name (e.g., "spaghetti carbonara").

- `cuisine`: The cuisine type(e.g., Italian, Mexican)

- `time_to_prepare`: Preparation time in minutes.

- `food_quantity`: Number of servings the recipe makes.

#### **Important Methods:**

- `create_table()`: Create the `recipes` table if it doesn't exist.

- `drop_table()`: Drops the `recipes` table (dangerous! delete data).

- `save`: Saves a new recipe to the database.

- `create`: Convenience method to instantiate and save a recipe.

- `update()`: Update recipe details in the database.

- `delete()`: Remove the recipe from the database.

- `find_by_id()`: Retrieve a recipe by its ID.

- `find_by_name()`: Retrieve a recipe by name (case-insensitive).

- `get_ingredients()`: Fetch all ingredients linked to this recipe.


```python


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
          

```

---

### **Ingredient**

Represents a single ingridient tied to a specific recipe:

- `id`: Unique database identifier.

- `name`: Ingredient name(e.g., "Tomato").

- `quantity`: Amount required (e.g., 2.5).

- `unit`: Unit of measurement(e.g., grams, cups)

- `recipe_id`: Foreign key linking ingredient to its recipe.

#### **Important Methods:**

- `create_table()`: Creates the `ingredients` table if not exists.

- `drop_table()`: Drop the `ingredients` table.

- `save()`: Saves a new ingredient in the database.

- `create()`: Instances and saves an ingredient.

- `delete()`: Deletes this ingredient from the database.

- `delete_by_recipe_id()`: Delete all ingedients for a particular recipe.
- `find_by_id()`: Retrieves an ingredient by its ID.


```python

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

    
```
---

## **CLI Appearance**

```css

======================
🍽️  RECIPE MANAGER  🍽️
======================
Select an option:

 0.  Exit application
 1.  List all recipes
 2.  Find recipe by ID
 3.  Find recipe by name
 4.  Show ingredients for a recipe
 5.  Create a new recipe
 6.  Update an existing recipe
 7.  Delete a recipe
 8.  Create ingredient for a recipe
 9.  Delete an ingredient
 10. Adjust ingredient quantities by food quantity
 11. Reset all tables (DANGER)

Enter your choice: :

```

---

## CLI Helper Functions

The user interface functionality is neatly organized into helper functions that simplify interaction and operations:

| Function                        | Description                                                                 |
|---------------------------------|-----------------------------------------------------------------------------|
| `exit_application()`            | Gracefully exits the program with a colorful goodbye message.               |
| `list_all_recipes()`            | Lists all recipes in a nicely formatted table.                              |
| `find_recipe_by_id()`           | Prompts the user to enter an ID and fetches the matching recipe.            |
| `find_recipe_by_name()`         | Prompts the user to enter a recipe name and fetches the matching recipe.    |
| `show_ingredients_by_id()`      | Displays all ingredients for a given recipe ID.                             |
| `create_recipe()`               | Walks the user through creating a new recipe with all necessary details.    |
| `update_recipe()`               | Lets the user update fields of an existing recipe.                          |
| `delete_recipe()`               | Deletes a recipe and all its ingredients after confirmation.                |
| `create_ingredient_for_recipe()`| Adds ingredients interactively to an existing recipe.                       |
| `delete_ingredient()`           | Deletes an ingredient by its ID with user confirmation.                     |
| `adjust_ingredients_by_quantity()` | Scales all ingredient quantities according to a new desired serving size.|
| `reset_tables()`                | Drops and recreates the recipe and ingredient tables, wiping all data.      |

---

## **Important Notes**

- **Data persistence**: Recipe and ingredients are saved in SQLite database tables.

- **Resetting tables**: The reset option will permanently erase all data, so use with caution.

- **Input validation**: The CLI checks for inputs but make sure to enter correct data types when prompted.

## **File structure**

```css

Recipe-Manager/
├── lib/
│   ├── cli.py
│   ├── helpers.py
│   └── models/
│       ├── __init__.py
│       ├── ingredient.py
│       └── recipe.py
├── Pipfile
├── Pipfile.lock
└── README.md

```

## **Technologies used**

- Python 3.10+

- SQLite3

- Colorama - for colorful CLI UI

- Tabulate - for formatting tables

## **Future Enhancements**

- Add recipe categories or tags

- Add nutrition info per ingredient

---

## **Authors**
- Richard Wasonga - [GitHub Profile](https://github.com/Richard3wasonga)

## **Contributors**
- Bob Oyier - [GitHub Profile](https://github.com/oyieroyier)

- Titus Ouko - [GitHub Profile](https://github.com/costamay)

## **Contributing**

Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

---

## **License**

This project is open-source and available under the MIT License.

