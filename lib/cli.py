from models.recipe import Recipe
from models.ingredient import Ingredient
from helpers import (
    exit_application,
    list_all_recipes,
    find_recipe_by_id,
    find_recipe_by_name,
    show_ingredients_by_id,
    create_recipe,
    update_recipe,
    delete_recipe,
    create_ingredient_for_recipe,
    delete_ingredient,
    reset_tables
)

from colorama import Fore, Style, init
import time
import os

init(autoreset=True)

Recipe.create_table()
Ingredient.create_table()

def styled_title():
    os.system('cls' if os.name == 'nt' else 'clear')
    title = "🍽️  RECIPE MANAGER  🍽️"
    border = "=" * len(title)
    print(Fore.YELLOW + Style.BRIGHT + border)
    print(Fore.MAGENTA + Style.BRIGHT + title)
    print(Fore.YELLOW + Style.BRIGHT + border)

def menu():
    styled_title()
    print(Fore.CYAN + "Select an option:\n")
    options = [
        "0. Exit application",
        "1. List all recipes",
        "2. Find recipe by ID",
        "3. Find recipe by name",
        "4. Show ingredients for a recipe",
        "5. Create a new recipe",
        "6. Update an existing recipe",
        "7. Delete a recipe",
        "8. Create ingredient for a recipe",
        "9. Delete an ingredient",
        "10. Reset all tables (DANGER)"
    ]

    for opt in options:
        print(Fore.GREEN + f" {opt}")
        time.sleep(0.03)  

def main():
    while True:
        menu()
        choice = input(Fore.CYAN + Style.BRIGHT + "\nEnter your choice: " + Fore.RESET)
        if choice == "0":
            exit_application()
        elif choice == "1":
            list_all_recipes()
        elif choice == "2":
            find_recipe_by_id()
        elif choice == "3":
            find_recipe_by_name()
        elif choice == "4":
            show_ingredients_by_id()
        elif choice == "5":
            create_recipe()
        elif choice == "6":
            update_recipe()
        elif choice == "7":
            delete_recipe()
        elif choice == "8":
            create_ingredient_for_recipe()
        elif choice == "9":
            delete_ingredient()
        elif choice == "10":
            reset_tables()
        else:
            print(Fore.RED + "❌ Invalid choice: Try again")

        input(Fore.YELLOW + "\nPress Enter to continue...")

if __name__ == "__main__":
    main()
