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
    headers = ["ID", "Name", "Cuisine", "Time to Prepare", "Food Quantity"]
    data = [[recipe.id, recipe.name, recipe.cuisine, recipe.time_to_prepare, recipe.food_quantity]]
    print("\nCurrent recipe info:")
    print(tabulate(data, headers=headers, tablefmt="simple"))

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

def delete_recipe():
    try:
        recipe_id = int(input("Enter the ID of the recipe to delete: ").strip())
    except ValueError:
        print("Invalid input. Please enter a valid recipe ID.")
        return

    recipe = Recipe.find_by_id(recipe_id)
    if not recipe:
        print(f"No recipe found with ID {recipe_id}.")
        return

    confirm = input(f"Are you sure you want to delete recipe '{recipe.name}' and all its ingredients? (yes/no): ").strip().lower()
    if confirm == "yes":
        Ingredient.delete_by_recipe_id(recipe.id)
        recipe.delete()
        print(f"Recipe '{recipe.name}' and its ingredients deleted successfully")
    else:
        print("Delete operation cancelled.")

def create_ingredient_for_recipe():
    try:
        recipe_id = int(input("Enter the ID of the recipe to add ingredients to: ").strip())
    except ValueError:
        print("Invalid input. Please enter a valid recipe ID.")
        return

    recipe = Recipe.find_by_id(recipe_id)
    if not recipe:
        print(f"No recipe found with ID {recipe_id}.")
        return

    while True:
        name = input("Enter ingredient name (or 'done' to finish): ").strip()
        if name.lower() == "done":
            break

        try:
            quantity = float(input("Enter quantity: ").strip())
        except ValueError:
            print("Invalid quantity. Please enter a number.")
            continue

        unit = input("Enter unit (e.g., grams, cups): ").strip()

        if not unit:
            print("Unit cannot be empty.")
            continue

        ingredient = Ingredient.create(name, quantity, unit, recipe_id)
        print(f"Ingredient '{ingredient.name}' added to recipe '{recipe.name}'.")

    print(f"Finished adding ingredients to '{recipe.name}'.")

def delete_ingredient():
    try:
        ingredient_id = int(input("Enter the ID of the ingredient to delete: ").strip())
    except ValueError:
        print("Invalid input. Please enter a valid ingredient ID.")
        return

    ingredient = Ingredient.find_by_id(ingredient_id)
    if not ingredient:
        print(f"No ingredient found with ID {ingredient_id}.")
        return

    confirm = input(f"Are you sure you want to delete ingredient '{ingredient.name}'? (yes/no): ").strip().lower()
    if confirm == "yes":
        ingredient.delete()
        print(f"Ingredient {ingredient.name} deleted successfully.")
    else:
        print("Delete operation cancelled.")

def adjust_ingredients_by_quantity():
    try:
        recipe_id = int(input("Enter the recipe ID to scale ingredients: ").strip())
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a valid number.")
        return

    recipe = Recipe.find_by_id(recipe_id)
    if not recipe:
        print(Fore.RED + f"No recipe found with ID {recipe_id}.")
        return

    ingredients = recipe.get_ingredients()
    if not ingredients:
        print(Fore.YELLOW + f"No ingredients found for recipe '{recipe.name}'.")
        return

    print(Fore.CYAN + f"\nRecipe: {recipe.name}")
    print(Fore.CYAN + f"Default serves: {recipe.food_quantity}")

    try:
        desired_quantity = int(input("Enter desired food quantity: ").strip())
        if desired_quantity <= 0:
            print(Fore.RED + "Desired quantity must be greater than 0.")
            return
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a number.")
        return

    factor = desired_quantity / recipe.food_quantity

    adjusted_ingredients = [
        (name, round(quantity * factor, 2), unit)
        for name, quantity, unit in ingredients
    ]

    print(Fore.GREEN + f"\nAdjusted ingredients for {desired_quantity} servings:\n")
    headers = ["Ingredient", "Quantity", "Unit"]
    print(tabulate(adjusted_ingredients, headers=headers, tablefmt="fancy_grid"))
