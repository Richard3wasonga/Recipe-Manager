from models.__init__ import CONN, CURSOR
from models.recipe import Recipe
from models.ingredient import Ingredient
from tabulate import tabulate
from colorama import init, Fore, Style
import time
import sys

init(autoreset=True)

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
    f_name = input("Enter name of recipe: ").strip()
    cuisine_origin = input("Enter cuisine of recipe: ").strip()
    
    if not f_name or not cuisine_origin:
        print("Recipe name and cuisine cannot be empty.")
        return

    try:
        time_prepared = int(input("Enter time taken to prepare the recipe (in minutes): ").strip())
        f_quantity = int(input("Enter food quantity: ").strip())
    except ValueError:
        print("Please enter valid numbers for time and food quantity.")
        return

    recipe = Recipe.create(f_name, cuisine_origin, time_prepared, f_quantity)
    print(f"Recipe '{recipe.name}' created successfully with ID {recipe.id}.")

def update_recipe():
    try:
        recipe_id = int(input("Enter the ID of the recipe to update: ").strip())
    except ValueError:
        print("Invalid input. please enter a valid recipe ID")
        return
    recipe = Recipe.find_by_id(recipe_id)
    if not recipe:
        print(f"No recipe found with ID {recipe_id}.")
        return
    print(f"Current recipe info: {recipe}")

    new_name = input(f"Enter new name of [{recipe.name}]: ").strip()
    new_cuisine = input(f"Enter new cuisine of [{recipe.cuisine}]: ").strip()

    if not new_name or not new_cuisine:
        print("New recipe name and new cuisine cannot be empty.")
        return

    try:
        new_time = input(f"Enter new preparation time in minutes [{recipe.time_to_prepare}]: ").strip()
        new_time = int(new_time) if new_time else recipe.time_to_prepare

        new_quantity = input(f"Enter new food quantity [{recipe.food_quantity}]: ").strip()
        new_quantity = int(new_quantity) if new_quantity else  recipe.food_quantity
    except ValueError:
        print("Invalid input. Time and quantity must be numbers.")
        return

    recipe.name = new_name if new_name else recipe.name
    recipe.cuisine = new_cuisine if new_cuisine else recipe.cuisine
    recipe.time_to_prepare = new_time
    recipe.food_quantity = new_quantity

    recipe.update()
    print(f"Recipe '{recipe.name}' updated successfully.")

def reset_tables():
    confrimation = input("This will DELETE ALL datain the database. Type 'yes' to continue and 'no' to cancle: ").strip().lower()
    if confrimation == "yes":
        Recipe.drop_table()
        Recipe.create_table()
        Ingredient.drop_table()
        Ingredient.create_table()
        print("Tables have been reset successfully.")
    else:
        print("Reset cancelled.")
    
        
