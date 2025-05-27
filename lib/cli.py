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
    reset_tables
)

Recipe.create_table()
Ingredient.create_table()

def menu():
    print("Select an option: ")
    print("0. Exit application")
    print("1. List all recipes")
    print("2. Find recipe by id")
    print("3. Find recipe by name")
    print("4. Show ingredients for a recipe")
    print("5. Create recipe")
    print("6. Update recipe")
    print("7. Reset tables")

def main():
    while True:
        menu()
        choice = input(": ")
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
            reset_tables()
        else:
            print("Invalid choice: Try again")

if __name__ == "__main__":
    main()