from models.__init__ import CONN, CURSOR
from models.recipe import Recipe
from models.ingredient import Ingredient
import ipdb

def testing():
    # Reset tables
    Recipe.drop_table()
    Recipe.create_table()
    Ingredient.drop_table()
    Ingredient.create_table()

    # Recipe 1: Pasta (Italian cuisine)
    recipe1 = Recipe(name="Spaghetti Carbonara", cuisine="Italian", time_to_prepare=25, food_quantity=2)
    recipe1.save()
    print(recipe1)

    # Ingredients for recipe 1
    ingredient1_1 = Ingredient(name="Spaghetti", quantity=200, unit="grams", recipe_id=recipe1.id)
    ingredient1_1.save()
    ingredient1_2 = Ingredient(name="Eggs", quantity=3, unit="pcs", recipe_id=recipe1.id)
    ingredient1_2.save()
    ingredient1_3 = Ingredient(name="Pancetta", quantity=100, unit="grams", recipe_id=recipe1.id)
    ingredient1_3.save()
    ingredient1_4 = Ingredient(name="Parmesan cheese", quantity=50, unit="grams", recipe_id=recipe1.id)
    ingredient1_4.save()
    ingredient1_5 = Ingredient(name="Black pepper", quantity=1, unit="tsp", recipe_id=recipe1.id)
    ingredient1_5.save()
    ingredient1_6 = Ingredient(name="Salt", quantity=0.5, unit="tsp", recipe_id=recipe1.id)
    ingredient1_6.save()

    # Recipe 2: Omelette (French cuisine)
    recipe2 = Recipe(name="Classic French Omelette", cuisine="French", time_to_prepare=10, food_quantity=1)
    recipe2.save()
    print(recipe2)

    # Ingredients for recipe 2
    ingredient2_1 = Ingredient(name="Eggs", quantity=3, unit="pcs", recipe_id=recipe2.id)
    ingredient2_1.save()
    ingredient2_2 = Ingredient(name="Butter", quantity=20, unit="grams", recipe_id=recipe2.id)
    ingredient2_2.save()
    ingredient2_3 = Ingredient(name="Salt", quantity=0.25, unit="tsp", recipe_id=recipe2.id)
    ingredient2_3.save()
    ingredient2_4 = Ingredient(name="Black pepper", quantity=0.25, unit="tsp", recipe_id=recipe2.id)
    ingredient2_4.save()
    ingredient2_5 = Ingredient(name="Chives", quantity=1, unit="tbsp", recipe_id=recipe2.id)
    ingredient2_5.save()

    # Print ingredients for recipe 1
    print("\nIngredients for:", recipe1.name)
    for name, quantity, unit in recipe1.get_ingredients():
        print(f"{name:<15} {quantity:<8} {unit}")

    # Print ingredients for recipe 2
    print("\nIngredients for:", recipe2.name)
    for name, quantity, unit in recipe2.get_ingredients():
        print(f"{name:<15} {quantity:<8} {unit}")

    ipdb.set_trace()

testing()
