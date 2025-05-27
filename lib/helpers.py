from models.__init__ import CONN, CURSOR
from models.recipe import Recipe
from models.ingredient import Ingredient
from tabulate import tabulate
from colorama import init, Fore, Style
import time
import sys

init(autoreset=True)

Recipe.drop_table()
Recipe.create_table()
Ingredient.drop_table()
Ingredient.create_table()

def exit_application():
    message = "Goodbye! Thanks for using Recipe Manager 🍽️"
    print("\n" + Fore.YELLOW +  "=" * len(message))
    for char in message:
        sys.stdout.write(Fore.MAGENTA + char)
        sys.stdout.flush()
        time.sleep(0.03)
    print("\n" + Fore.YELLOW + "=" * len(message))
    exit()
    
def list_all_recipes():
    sql = "SELECT id, name, cuisine, time_to_prepare, food_quantity FROM recipes"
    CURSOR.execute(sql)
    recipes = CURSOR.fetchall()
    if recipes:
        print(tabulate(recipes, headers=["ID", "Name", "Cuisine", "Time to Prepare", "Food Quantity"], tablefmt="heavy_grid"))
    else:
        print("No recipes found.")

def find_recipe_by_id():
    try:
        recipe_id = int(input("Enter recipe ID: ").strip())  
        recipe = Recipe.find_by_id(recipe_id)
        if recipe:
            headers = ["ID", "Name", "Cuisine", "Time to Prepare", "Food Quantity"]
            data = [[recipe.id, recipe.name, recipe.cuisine, recipe.time_to_prepare, recipe.food_quantity]]
            print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
        else:
            print(f"Recipe with id {recipe_id} not found.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def find_recipe_by_name():
    name = input("Enter recipe name: ").strip()
    recipe = Recipe.find_by_name(name)
    if recipe:
        headers = ["ID", "Name", "Cuisine", "Time to Prepare", "Food Quantity"]
        data = [[recipe.id, recipe.name, recipe.cuisine, recipe.time_to_prepare, recipe.food_quantity]]
        print(tabulate(data, headers=headers, tablefmt="rounded_grid"))
    else:
        print(f"Recipe with name '{name}' not found.")

def show_ingredients_by_id():
    try:
        recipe_id = int(input("Enter recipe ID to show ingredients: ").strip())
        recipe = Recipe.find_by_id(recipe_id)
        if recipe:
            ingredients = recipe.get_ingredients()
            print(f"\nIngredients for: {recipe.name}")
            if not ingredients:
                print("No ingredients found.")
                return

            headers = ["Name", "Quantity", "Unit"]
            print(tabulate(ingredients, headers=headers, tablefmt="double_grid"))
        else:
            print(f"Recipe with id {recipe_id} not found.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def create_recipe():
    f_name = str(input("Enter name of recipe: ").strip())
    cuisine_origin = str(input("Enter cuisine of recipe: ").strip())
    time_prepared = int(input("Enter time taken to prepare the recipe: ").strip())
    f_quantity = int(input("Enter food quantity: ").strip())
    recipe = Recipe(name=f_name, cuisine=cuisine_origin, time_to_prepare=time_prepared, food_quantity=f_quantity)
    recipe.save()