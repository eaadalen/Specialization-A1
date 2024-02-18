import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "cf-python",
    passwd = "password"
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
               id INT AUTO_INCREMENT PRIMARY KEY,
               name VARCHAR(50),
               ingredients VARCHAR(255),
               cooking_time INT,
               difficulty VARCHAR(20)
)''')

def main_menu(conn, cursor):
    choice = ""
    while(choice != "quit"):
        print()
        print("      RECIPE APP")
        print()
        print("======================")
        print("   Select an option    ")
        print("======================\n")
        print("1. Create a new recipe")
        print("2. Search for recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe\n")
        print("Type 'quit' to exit the program\n")
        choice = input("Your choice: ").strip().lower()
        print()


        if choice in ["1", "2", "3", "4"]:

            if choice == "1":
                create_recipe(conn, cursor)
            elif choice == "2":
                search_recipe(conn, cursor)
            elif choice == "3":
                update_recipe(conn, cursor)
            elif choice == "4":
                delete_recipe(conn, cursor)
        elif choice == "quit":
            print("=============================================")
            print("      Thanks for using the Recipe App!       ")
            print("             See you next time               ")
            print("=============================================")
            break
        else:
            print("---------------------------------------------------")
            print("Invalid choice! Please enter 1, 2, 3, 4, or 'quit'.")
            print("---------------------------------------------------\n")
            print("...returning to main menu\n\n")

    conn.close()


def create_recipe(conn, cursor):
    print()
    print("==================================================")
    print("           *** Create New Recipes ***             ")
    print("==================================================")
    print("Please follow the steps below to add new recipes!\n")
    
    while True:
        try:
            number_of_recipes = int(input("How many recipes would you like to enter? "))
            if number_of_recipes < 1:
                print("Please enter a positive number.\n")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.\n")
    
    for i in range(number_of_recipes):
        print(f"\nEnter recipe #{i + 1}")
        print("---------------------")

        name = input("  Enter the recipe name: ")
        cooking_time = int(input("  Enter the cooking time in minutes: "))
        ingredients_input = input("  Enter the recipe's ingredients, separated by a comma: ")
        ingredients = ingredients_input.split(", ")

        difficulty = calculate_difficulty(cooking_time, ingredients)

        ingredients_str = ", ".join(ingredients)

        try:
            insert_query = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (name, ingredients_str, cooking_time, difficulty))
            conn.commit()

            print("  ** Recipe successfully added! **")
        except mysql.connector.Error as err:
            print("Error occurred: ", err)
    
    final_message = "Recipe successfully added!" if number_of_recipes == 1 else "All recipes successfully added!"

    print()
    print("--------------------------------------------------")
    print(f"            {final_message}            ")
    print("--------------------------------------------------\n")
    print("...returning to main menu\n\n")


def calculate_difficulty(cooking_time, ingredients):
    num_ingredients = len(ingredients)
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    elif cooking_time >= 10 and num_ingredients >= 4:
        return "Hard"


def format_recipe_display(recipe):
    print(f"\nRecipe: {recipe[1].title()}")
    print(f"  Time: {recipe[3]} mins")
    print("  Ingredients:")
    for ingredient in recipe[2].split(", "):
        print(f"  - {ingredient.title()}")
    print(f"  Difficulty: {recipe[4]}")        


def search_recipe(conn, cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    if not results:
        print("***************************************************************")
        print("        There are no recipes in the database to search.        ")
        print("                  Please create a new recipe!                  ")
        print("***************************************************************\n")
        print("...returning to main menu\n\n")
        return

    all_ingredients = set()

    print()
    print("=================================================================")
    print("           *** Search for a Recipe By Ingredient ***             ")
    print("=================================================================")
    print("Please enter a number to see all recipes that use that ingredient\n")

    for result in results:
        ingredients_list = result[0].split(", ")
        for ingredient in ingredients_list:
            all_ingredients.add(ingredient.strip())

    for i, ingredient in enumerate(sorted(all_ingredients)):
        print(f"{i+1}.) {ingredient.title()}")

    print()
    while True:
        try:
            choice = int(input("Enter a number for the ingredient: "))
            if 1 <= choice <= len(all_ingredients):
                break
            else:
                print()
                print("Please enter a number within the list range.\n")
        except ValueError:
            print()
            print("Invalid input. Please enter a number.\n")

    selected_ingredient = sorted(all_ingredients)[choice - 1]

    search_query = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
    cursor.execute(search_query, ("%" + selected_ingredient + "%",))
    search_results = cursor.fetchall()

    if search_results:
        recipe_count = len(search_results)
        recipe_word = "recipe" if recipe_count == 1 else "recipes"
        print(f"\n{recipe_count} {recipe_word} found containing '{selected_ingredient.title()}'\n")
        for recipe in search_results:
            format_recipe_display(recipe)

        print()
        print("--------------------------------------------------")
        print("            Recipe search successful!             ")
        print("--------------------------------------------------\n")
        print("...returning to main menu\n")
    else:
        print(f"No recipes found containing '{selected_ingredient.title()}'\n")
    
    print("\n")

  
def update_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    if not results:
        print("***************************************************************")
        print("        There are no recipes in the database to update.        ")
        print("                  Please create a new recipe!                  ")
        print("***************************************************************\n")
        print("...returning to main menu\n\n")
        return
    
    print()
    print("=================================================================")
    print("             *** Update a Recipe By ID Number ***                ")
    print("=================================================================")
    print("Please enter an ID number to update that recipe\n")


    print("---- Avaiable Recipes ----\n")
    for result in results:
        ingredients_list = result[2].split(", ")
        capitalized_ingredients = [ingredient.title() for ingredient in ingredients_list]
        capitalized_ingredients_str = ", ".join(capitalized_ingredients)

        print(f"ID: {result[0]} | Name: {result[1]}")
        print(f"Ingredients: {capitalized_ingredients_str} | Cooking Time: {result[3]} | Difficulty: {result[4]}\n")

    while True:
        try:
            print()
            recipe_id = int(input("Enter the ID of the recipe to update: "))
            print()

            cursor.execute("SELECT COUNT(*) FROM Recipes WHERE id = %s", (recipe_id,))
            if cursor.fetchone()[0] == 0:
                print("No recipe found with the entered ID. Please try again.\n")
            else:
                break
        except ValueError:
            print()
            print("Invalid input. Please enter a numeric value.\n")

    selected_recipe = next((recipe for recipe in results if recipe[0] == recipe_id), None)
    if selected_recipe:
        print(f"Which field would you like to update for '{selected_recipe[1]}'?")
    else:
        print("Recipe not found.")
        return
    print(" - Name")
    print(" - Cooking Time")
    print(" - Ingredients\n")

    update_field = input("Enter your choice: ").lower()
    print()

    if update_field == "cooking time":
        update_field = "cooking_time"

    if update_field not in ["name", "cooking_time", "ingredients"]:
        print("Invalid field. Please enter 'name', 'cooking_time', or 'ingredients'.")
        return
    
    if update_field == "cooking_time" or update_field == "cooking time":
        while True:
            try:
                new_value = int(input("Enter the new cooking time (in minutes): "))
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value for cooking time.")
    else:
        new_value = input(f"Enter the new value for {update_field}: ")

    update_query = f"UPDATE Recipes SET {update_field} = %s WHERE id = %s"
    cursor.execute(update_query, (new_value, recipe_id))

    if update_field in ["cooking_time", "ingredients"]:
        cursor.execute("SELECT cooking_time, ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        updated_recipe = cursor.fetchone()
        new_difficulty = calculate_difficulty(int(updated_recipe[0]), updated_recipe[1].split(", "))

        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_difficulty, recipe_id))

    conn.commit()

    print()
    print("--------------------------------------------------")
    print("           Recipe successfully updated!           ")
    print("--------------------------------------------------\n")
    print("...returning to main menu\n\n")


def delete_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    if not results:
        print("***************************************************************")
        print("        There are no recipes in the database to delete.        ")
        print("                  Please create a new recipe!                  ")
        print("***************************************************************\n")
        print("...returning to main menu\n\n")
        return
    
    print()
    print("=================================================================")
    print("             *** Delete a Recipe By ID Number ***                ")
    print("=================================================================")
    print("Please enter the ID number of the recipe to remove")
    print("*Note: This can NOT be undone\n")

    
    print("---- Avaiable Recipes ----\n")
    for result in results:
        ingredients_list = result[2].split(", ")
        capitalized_ingredients = [ingredient.title() for ingredient in ingredients_list]
        capitalized_ingredients_str = ", ".join(capitalized_ingredients)

        print(f"ID: {result[0]} | Name: {result[1]}")
        print(f"Ingredients: {capitalized_ingredients_str} | Cooking Time: {result[3]} | Difficulty: {result[4]}\n")

    while True:
        try:
            recipe_id = int(input("Enter the ID of the recipe to delete: "))
            print()

            cursor.execute("SELECT COUNT(*) FROM Recipes WHERE id = %s", (recipe_id,))
            if cursor.fetchone()[0] == 0:
                print("No recipe found with the entered ID. Please try again.\n")
            else:
                
                cursor.execute("SELECT name FROM Recipes WHERE id = %s", (recipe_id,))
                recipe_name = cursor.fetchone()[0]
                confirm = input(f"Are you sure you want to delete '{recipe_name}'? (Yes/No): ").lower()
                
                if confirm == "yes":
                    break
                elif confirm == "no":
                    print()
                    print("Deletion cancelled. Returning to main menu\n\n")
                    return
                else:
                    print()
                    print("Please answer with 'Yes' or 'No'.\n")
                
        except ValueError:
            print()
            print("Invalid input. Please enter a numeric value.\n")

    cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))

    conn.commit()

    print()
    print("--------------------------------------------------")
    print("           Recipe successfully deleted!           ")
    print("--------------------------------------------------\n")
    print("...returning to main menu\n\n")
    

main_menu(conn, cursor)