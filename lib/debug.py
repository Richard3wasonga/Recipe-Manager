from models.__init__ import CONN, CURSOR
from models.recipe import Recipe
from models.ingredient import Ingredient
import ipdb

def testing():
    Recipe.drop_table()
    Recipe.create_table()
    Ingredient.drop_table()
    Ingredient.create_table()


    recipe1 = Recipe(name="Pasta", cuisine="Italian", time_to_prepare=30, food_quantity=1 )
    recipe1.save()
    print(recipe1)


    ingredient1_1 = Ingredient(name="Tomato", quantity=4, unit="pcs", recipe_id=recipe1.id)
    ingredient1_1.save()

    ingredient1_2 = Ingredient(name="Onion", quantity=2, unit="pcs", recipe_id=recipe1.id)
    ingredient1_2.save()


    recipe2 = Recipe(name="Omelette", cuisine="French", time_to_prepare=10, food_quantity=3)
    recipe2.save()
    print(recipe2)


    ingredient2_1 = Ingredient(name="Eggs", quantity=3, unit="pcs", recipe_id=recipe2.id)
    ingredient2_1.save()

    ingredient2_2 = Ingredient(name="Salt", quantity=0.5, unit="tsp", recipe_id=recipe2.id)
    ingredient2_2.save()
    print(ingredient1_1)
    print(ingredient1_2)
    print(ingredient2_1)
    print(ingredient2_2)

    print("\nIngredients for:", recipe1.name)
    for name, quantity, unit in recipe1.get_ingredients():
        print(f"{name:<12} {quantity:<8} {unit}")

    # Example: print ingredients for recipe2
    print("\nIngredients for:", recipe2.name)
    for name, quantity, unit in recipe2.get_ingredients():
        print(f"{name:<12} {quantity:<8} {unit}")

    ipdb.set_trace()

testing()

