from models.__init__ import CONN, CURSOR
from models.recipe import Recipe
from models.ingredient import Ingredient

def seed_data():
    # Reset tables
    Recipe.drop_table()
    Recipe.create_table()
    Ingredient.drop_table()
    Ingredient.create_table()

    ### Recipe 1: Spaghetti Carbonara
    carbonara = Recipe(name="Spaghetti Carbonara", cuisine="Italian", time_to_prepare=25, food_quantity=2)
    carbonara.save()

    Ingredient(name="Spaghetti", quantity=200, unit="grams", recipe_id=carbonara.id).save()
    Ingredient(name="Eggs", quantity=3, unit="pcs", recipe_id=carbonara.id).save()
    Ingredient(name="Pancetta", quantity=100, unit="grams", recipe_id=carbonara.id).save()
    Ingredient(name="Parmesan cheese", quantity=50, unit="grams", recipe_id=carbonara.id).save()
    Ingredient(name="Black pepper", quantity=1, unit="tsp", recipe_id=carbonara.id).save()
    Ingredient(name="Salt", quantity=0.5, unit="tsp", recipe_id=carbonara.id).save()

    ### Recipe 2: Classic French Omelette
    omelette = Recipe(name="Classic French Omelette", cuisine="French", time_to_prepare=10, food_quantity=1)
    omelette.save()

    Ingredient(name="Eggs", quantity=3, unit="pcs", recipe_id=omelette.id).save()
    Ingredient(name="Butter", quantity=20, unit="grams", recipe_id=omelette.id).save()
    Ingredient(name="Salt", quantity=0.25, unit="tsp", recipe_id=omelette.id).save()
    Ingredient(name="Black pepper", quantity=0.25, unit="tsp", recipe_id=omelette.id).save()
    Ingredient(name="Chives", quantity=1, unit="tbsp", recipe_id=omelette.id).save()

    ### Recipe 3: Chicken Stir Fry
    stir_fry = Recipe(name="Chicken Stir Fry", cuisine="Chinese", time_to_prepare=20, food_quantity=3)
    stir_fry.save()

    Ingredient(name="Chicken breast", quantity=300, unit="grams", recipe_id=stir_fry.id).save()
    Ingredient(name="Soy sauce", quantity=2, unit="tbsp", recipe_id=stir_fry.id).save()
    Ingredient(name="Garlic", quantity=3, unit="cloves", recipe_id=stir_fry.id).save()
    Ingredient(name="Bell pepper", quantity=1, unit="pcs", recipe_id=stir_fry.id).save()
    Ingredient(name="Onion", quantity=1, unit="pcs", recipe_id=stir_fry.id).save()
    Ingredient(name="Olive oil", quantity=1, unit="tbsp", recipe_id=stir_fry.id).save()

    ### Recipe 4: Guacamole
    guacamole = Recipe(name="Guacamole", cuisine="Mexican", time_to_prepare=10, food_quantity=2)
    guacamole.save()

    Ingredient(name="Avocados", quantity=2, unit="pcs", recipe_id=guacamole.id).save()
    Ingredient(name="Lime juice", quantity=2, unit="tbsp", recipe_id=guacamole.id).save()
    Ingredient(name="Red onion", quantity=0.25, unit="pcs", recipe_id=guacamole.id).save()
    Ingredient(name="Tomato", quantity=1, unit="pcs", recipe_id=guacamole.id).save()
    Ingredient(name="Cilantro", quantity=1, unit="tbsp", recipe_id=guacamole.id).save()
    Ingredient(name="Salt", quantity=0.5, unit="tsp", recipe_id=guacamole.id).save()

    ### Recipe 5: Banana Pancakes
    pancakes = Recipe(name="Banana Pancakes", cuisine="American", time_to_prepare=15, food_quantity=2)
    pancakes.save()

    Ingredient(name="Bananas", quantity=2, unit="pcs", recipe_id=pancakes.id).save()
    Ingredient(name="Eggs", quantity=2, unit="pcs", recipe_id=pancakes.id).save()
    Ingredient(name="Flour", quantity=100, unit="grams", recipe_id=pancakes.id).save()
    Ingredient(name="Milk", quantity=100, unit="ml", recipe_id=pancakes.id).save()
    Ingredient(name="Baking powder", quantity=1, unit="tsp", recipe_id=pancakes.id).save()
    Ingredient(name="Maple syrup", quantity=2, unit="tbsp", recipe_id=pancakes.id).save()

    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_data()
