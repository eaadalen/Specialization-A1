from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql.expression import or_

# Database Configuration: Set up connection parameters for the MySQL database.
USERNAME = "cf-python"
PASSWORD = "password"
HOST = "localhost"
DATABASE = "task_database"

# SQLAlchemy Engine: Create the engine to manage connections to the database.
engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}")

# Base Class: All model classes will inherit from this class.
Base = declarative_base()

# Session: Set up the mechanism to talk to the database. 
# The session will be used to query and commit transactions.
Session = sessionmaker(bind=engine)
session = Session()

class Recipe(Base):
    # Table Name: Define the name of the table in the database.
    __tablename__ = "final_recipes"

    # Schema:
    #|-----------------------------------------------------------------------------------|
    #| Field        | Type         | Null     | Key         | Default   | Extra          |
    #|--------------|--------------|----------|-------------|-----------|----------------|
    #| id           | int          | NOT NULL | PRIMARY KEY | NULL      | AUTO_INCREMENT |
    #| name         | varchar(50)  | NULLABLE |             | NULL      |                |
    #| ingredients  | varchar(255) | NULLABLE |             | NULL      |                |
    #| cooking_time | int          | NULLABLE |             | NULL      |                |
    #| difficulty   | varchar(20)  | NULLABLE |             | NULL      |                |
    #|-----------------------------------------------------------------------------------|

    # Columns: Define the structure of the table.
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        # Representation: Used for debugging purposes, showing a quick string representation of the object.
        return f"<Recipe(id={self.id}, name={self.name}, difficulty={self.difficulty})>"
    
    def __str__(self):
        # String Representation: Formats recipe details in a user-friendly way for printing.
        ingredients_list = self.ingredients.split(", ")
        formatted_ingredients = "\n ".join(f"  - {ingredient.title()}" for ingredient in ingredients_list)

        return (f"Recipe ID: {self.id}\n"
                f"  Name: {self.name.title()}\n"
                f"  Ingredients:\n {formatted_ingredients}\n"
                f"  Cooking Time: {self.cooking_time} minutes\n"
                f"  Difficulty: {self.difficulty}\n")
    
    def calculate_difficulty(self):
        # Calculate Difficulty: Determines the recipe's difficulty based on cooking time and number of ingredients.
        num_ingredients = len(self.return_ingredients_as_list())
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_ingredients >= 4:
            self.difficulty = "Hard"

    def return_ingredients_as_list(self):
        # Convert Ingredients to List: Splits the ingredients string into a list for easier manipulation.
        if not self.ingredients:
            return []
        return self.ingredients.split(", ")

# Create Tables: Execute the creation of tables in the database based on the models defined.   
Base.metadata.create_all(engine)


def create_recipe():
    # Display the header for the create recipe function.
    print()
    print("==================================================")
    print("           *** Create New Recipes ***             ")
    print("==================================================")
    print("Please follow the steps below to add new recipes!\n")
    
    # Loop to get the number of recipes the user wants to enter.
    # Validates that the input is a positive integer.
    while True:
        try:
            number_of_recipes = int(input("How many recipes would you like to enter? "))
            if number_of_recipes < 1:
                print("Please enter a positive number.\n")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.\n")
    
    # Loop over the number of recipes to be created.
    for i in range(number_of_recipes):
        print(f"\nEnter recipe #{i + 1}")
        print("---------------------")

        # Input validation for recipe name, ensuring it's within the character limit.
        while True:
            name = input("  Enter the recipe name: ").strip()
            if 0 < len(name) <= 50:
                break
            else:
                print("Please enter a valid recipe name (1-50 characters).\n")

        # Input validation for cooking time, ensuring it's a positive integer.
        while True:
            try:
                cooking_time = int(input("  Enter the cooking time in minutes: "))
                if cooking_time > 0:
                    break
                else:
                    print("Please enter a positive number for cooking time.\n")
            except ValueError:
                print("Invalid input. Please enter a positive number for cooking time.\n")

        # Input validation for ingredients, ensuring the input is not empty.
        while True:
                ingredients_input = input("  Enter the recipe's ingredients, separated by a comma: ").strip()
                if ingredients_input:
                    break
                else:
                    print("Please enter at least one ingredient.\n")

        # Create a new recipe instance and add it to the session.
        new_recipe = Recipe(name=name, ingredients=ingredients_input, cooking_time=cooking_time)
        new_recipe.calculate_difficulty()

        # Add the new recipe to the session and attempt to commit it to the database.
        session.add(new_recipe)
        try:
            session.commit()
            print("  ** Recipe successfully added! **")

        except Exception as err:
            # Rollback in case of error during commit.
            session.rollback()
            print("Error occurred: ", err)

    # Display a final message after adding recipes.    
    final_message = "Recipe successfully added!" if number_of_recipes == 1 else "All recipes successfully added!"
    print()
    print("--------------------------------------------------")
    print(f"            {final_message}            ")
    print("--------------------------------------------------\n")
    
    # Pause the execution and wait for the user to press enter.
    pause()


def view_all_recipes():
    # Retrieve all recipes from the database.
    recipes = session.query(Recipe).all()

    # Check if there are any recipes in the database, and display a message if there are none.
    if not recipes:
        print("***************************************************************")
        print("         There are no recipes in the database to view.         ")
        print("                 Please create a new recipe!                   ")
        print("***************************************************************\n")
        pause()
        return None

    # Header display for viewing all recipes.
    print("=================================================================")
    print("                  *** View All Recipes ***                   ")
    print("=================================================================")

    # Display the number of recipes found.
    recipe_count = len(recipes)
    recipe_word = "recipe" if recipe_count == 1 else "recipes"
    print(f"Displaying {recipe_count} {recipe_word}\n")

    # Loop through each recipe and display its details using a formatted string.
    for i, recipe in enumerate(recipes, start=1):
        print(f"Recipe #{i}\n----------")
        print(format_recipe_for_search(recipe))
        print()
    
    # Footer display after listing all recipes.
    print("\n--------------------------------------------------")
    print("             List Display Successful!              ")
    print("--------------------------------------------------\n")
    
    # Pause the execution and wait for the user to press enter.
    pause()


def search_recipe():
    # Retrieve all ingredients from all recipes in the database.
    results = session.query(Recipe.ingredients).all()

    # If no recipes are found, display a message and return to the main menu.
    if not results:
        print("***************************************************************")
        print("       There are no recipes in the database to search.         ")
        print("                 Please create a new recipe!                   ")
        print("***************************************************************\n")
        pause()
        return

    # Initialize a set to store all unique ingredients from the database results.
    all_ingredients = set()
    for result in results:
        ingredients_list = result[0].split(", ")
        for ingredient in ingredients_list:
            all_ingredients.add(ingredient.strip())

    # Print header for search function and instructions for user.
    print()
    print("=================================================================")
    print("           *** Search for a Recipe By Ingredient ***             ")
    print("=================================================================")
    print("Please enter a number to see all recipes that use that ingredient\n")

    # Sort and display each unique ingredient with its corresponding index.
    sorted_ingredients = sorted(all_ingredients)
    for i, ingredient in enumerate(sorted_ingredients):
        print(f"{i+1}.) {ingredient.title()}")

    # Prompt user to enter one or more ingredient numbers, separated by spaces.
    print()
    while True:
        try:
            choices = input("Enter ingredient numbers (separate multiple numbers with spaces): ").split()
            selected_indices = [int(choice) for choice in choices]
            if all(1 <= choice <= len(all_ingredients) for choice in selected_indices):
                break
            else:
                print("Please enter numbers within the list range.\n")
        except ValueError:
            print("Invalid input. Please enter valid numbers.\n")

    # Convert user input into a list of selected ingredients.
    search_ingredients = [sorted_ingredients[index - 1] for index in selected_indices]

    # Build a search query using the selected ingredients.
    search_conditions = [Recipe.ingredients.ilike(f"%{ingredient}%") for ingredient in search_ingredients]
    search_results = session.query(Recipe).filter(or_(*search_conditions)).all()

    # Format the string of selected ingredients for display.
    if len(search_ingredients) > 1:
        selected_ingredients_str = ", ".join(ingredient.title() for ingredient in search_ingredients[:-1])
        selected_ingredients_str += ", or " + search_ingredients[-1].title()
    else:
        selected_ingredients_str = search_ingredients[0].title()

    # Check if there are any recipes found with the selected ingredients.
    if search_results:
        recipe_count = len(search_results)
        recipe_word = "recipe" if recipe_count == 1 else "recipes"
        print(f"\n{recipe_count} {recipe_word} found containing '{selected_ingredients_str}'\n")
        
        # Display each found recipe with its details.
        for i, recipe in enumerate(search_results, start=1):
            print(f"Recipe #{i}\n----------")
            print(format_recipe_for_search(recipe))
            print()

        # End of search result display with a success message.
        print()
        print("--------------------------------------------------")
        print("            Recipe search successful!             ")
        print("--------------------------------------------------\n")
    else:
        # Message for the user if no matching recipes are found.
        print(f"No recipes found containing '{selected_ingredients_str}'\n")

    # Pause the execution and wait for the user to press enter.
    pause()


def update_recipe():
    # Retrieve all recipes from the database.
    recipes = session.query(Recipe).all()

    # Check if there are any recipes in the database; if not, display a message.
    if not recipes:
        print("***************************************************************")
        print("       There are no recipes in the database to update.         ")
        print("                Please create a new recipe!                    ")
        print("***************************************************************\n")
        pause()
        return
    
    # Header for the update function.
    print()
    print("=================================================================")
    print("             *** Update a Recipe By ID Number ***                ")
    print("=================================================================")
    print("Please enter an ID number to update that recipe\n")

    # Display the available recipes for update.
    print("---- Avaiable Recipes ----\n")
    for recipe in recipes:
        print(format_recipe_for_update(recipe))
    print()

    # Loop to get the ID of the recipe to update.
    while True:
        try:
            recipe_id = int(input("Enter the ID of the recipe to update: "))
            recipe_to_update = session.get(Recipe, recipe_id)
            if recipe_to_update:
                break
            else:
                print("No recipe found with the entered ID. Please try again.\n")
        except ValueError:
            print("Invalid input. Please enter a numeric value.\n")

    # Prompt the user to choose which field of the recipe to update.
    print(f"\nWhich field would you like to update for '{recipe_to_update.name}'?")
    print(" - Name")
    print(" - Cooking Time")
    print(" - Ingredients\n")

    # Flag to track whether the field has been successfully updated.
    field_updated = False
    while not field_updated:
        update_field = input("Enter your choice: ").lower()

        # Update logic for each field (name, cooking time, ingredients).
        if update_field == "name":
            while True:
                new_value = input("\nEnter the new name (1-50 characters): ").strip()
                if 0 < len(new_value) <= 50:
                    recipe_to_update.name = new_value
                    field_updated = True
                    break
                else:
                    print("Invalid name. Please enter 1-50 characters.\n")
            break

        elif update_field == "cooking time":
            while True:
                try:
                    new_value = int(input("\nEnter the new cooking time (in minutes): "))
                    if new_value > 0:
                        recipe_to_update.cooking_time = new_value
                        # Recalculate the difficulty after updating the cooking time.
                        recipe_to_update.calculate_difficulty()
                        field_updated = True
                        break
                    else:
                        print("Please enter a positive number for cooking time.")
                except ValueError:
                    print("Invalid input. Please enter a numeric value for cooking time.")
            break
                    
        elif update_field == "ingredients":
            while True:
                new_value = input("\nEnter the new ingredients, separated by a comma: ").strip()
                if new_value:
                    # Update the ingredients and recalculate the difficulty.
                    recipe_to_update.ingredients = new_value
                    recipe_to_update.calculate_difficulty()
                    field_updated = True
                    break
                else:
                    print("Please enter at least one ingredient.") 
            break
        else:
            print("Invalid choice. Please choose 'name', 'cooking time', or 'ingredients'.")

    # Attempt to commit the updated recipe to the database.
    try:
        session.commit()
        print("\n--------------------------------------------------")
        print("           Recipe successfully updated!           ")
        print("--------------------------------------------------\n")
    except Exception as err:
        # Rollback in case of error during the commit.
        session.rollback()
        print(f"An error occurred: {err}")

    # Pause the execution and wait for the user to press enter.
    pause()


def delete_recipe():
    # Retrieve all recipes from the database.
    recipes = session.query(Recipe).all()

    # Check if there are any recipes in the database; if not, display a message.
    if not recipes:
        print("***************************************************************")
        print("        There are no recipes in the database to delete.        ")
        print("                  Please create a new recipe!                  ")
        print("***************************************************************\n")
        pause()
        return
    
    # Header for the delete recipe function.
    print()
    print("=================================================================")
    print("             *** Delete a Recipe By ID Number ***                ")
    print("=================================================================")
    print("Please enter the ID number of the recipe to remove")
    print("** Note: This can NOT be undone **\n")

    # Display the available recipes for deletion.
    print("---- Avaiable Recipes ----\n")
    for recipe in recipes:
        print(format_recipe_for_update(recipe))

    # Loop to get the ID of the recipe to be deleted.
    while True:
        try:
            recipe_id = int(input("\nEnter the ID of the recipe to delete: "))
            # Retrieve the recipe to be deleted from the database.
            recipe_to_delete = session.get(Recipe, recipe_id)

            # Confirm deletion from the user.
            if recipe_to_delete:
                confirm = input(f"\nAre you sure you want to delete '{recipe_to_delete.name}'? (Yes/No): ").lower()
                if confirm == "yes":
                    break
                elif confirm == "no":
                    print("Deletion cancelled.\n")
                    pause()
                    return
                else:
                    print("Please answer with 'Yes' or 'No'.")
            else:
                print("No recipe found with the entered ID. Please try again.")
                
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    # Attempt to delete the selected recipe from the database.
    try:
        session.delete(recipe_to_delete)
        session.commit()
        print()
        print("--------------------------------------------------")
        print("           Recipe successfully deleted!           ")
        print("--------------------------------------------------\n")
    except Exception as err:
        # Rollback in case of error during the deletion.
        session.rollback()
        print(f"An error occured: {err}")

    # Pause the execution and wait for the user to press enter.  
    pause()


def main_menu():
    # Initialize the choice variable.
    choice = ""
    
    # Main menu loop - continues until the user decides to quit the application.
    while choice != "quit":
        
        # Display the main menu header and options.
        print("  _____           _                                   ")
        print(" |  __ \         (_)                /\                ")
        print(" | |__) |___  ___ _ _ __   ___     /  \   _ __  _ __  ")
        print(" |  _  // _ \/ __| | '_ \ / _ \   / /\ \ | '_ \| '_ \ ")
        print(" | | \ \  __/ (__| | |_) |  __/  / ____ \| |_) | |_) |")
        print(" |_|  \_\___|\___|_| .__/ \___| /_/    \_\ .__/| .__/ ")
        print("                   | |                   | |   | |    ")
        print("                   |_|                   |_|   |_|    ")
        print("======================================================")
        print("   What would you like to do? Pick a choice below!    ")
        print("======================================================\n")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for a recipe by ingredient")
        print("4. Update an existing recipe")
        print("5. Delete a recipe\n")
        print("Type 'quit' to exit the program\n")
        
        # while True:
            # Get the user's choice and convert it to lower case for easier comparison.
        choice = input("Your choice: ").strip().lower()

        # Execute the appropriate function based on the user's choice.
        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_recipe()
        elif choice == "4":
            update_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "quit":
            # Display a goodbye message when the user decides to quit the application.
            print("=============================================")
            print("      Thanks for using the Recipe App!       ")
            print("             See you next time               ")
            print("=============================================")
            break # Exit the loop to terminate the program.
        else:
            # Handle invalid input and prompt the user to try again.
            print("---------------------------------------------------")
            print("Invalid choice! Please enter 1, 2, 3, 4, 5, or 'quit'.")
            print("---------------------------------------------------\n")
            
            # Pause for user acknowledgement before showing the menu again.
            pause()

    session.close()
    engine.dispose()


def format_recipe_for_search(recipe):
    # Format the recipe's ingredients for display: each ingredient is listed on a new line with a dash.
    formatted_ingredients = "\n  ".join(f"- {ingredient.title()}" for ingredient in recipe.ingredients.split(", "))
    
    # Return a formatted string representing the recipe's details (name, cooking time, ingredients, difficulty).
    return (f"Recipe Name: {recipe.name.title()}\n"
            f"  Cooking Time: {recipe.cooking_time} mins\n"
            f"  Ingredients:\n  {formatted_ingredients}\n"
            f"  Difficulty: {recipe.difficulty}")


def format_recipe_for_update(recipe):
    # Capitalize the first letter of each ingredient in the list for display.
    capitalized_ingredients = [ingredient.title() for ingredient in recipe.ingredients.split(", ")]
    
    # Capitalize the first letter of each ingredient in the list for display.
    capitalized_ingredients_str = ", ".join(capitalized_ingredients)
    
    # Return a formatted string representing the recipe's details (ID, name, ingredients, cooking time, difficulty) for update purposes.
    return (f"ID: {recipe.id} | Name: {recipe.name}\n"
            f"Ingredients: {capitalized_ingredients_str} | Cooking Time: {recipe.cooking_time} | Difficulty: {recipe.difficulty}\n")


def pause():
    # Display a message prompting the user to press ENTER, then wait for user input.
    print("Press ENTER to return to the main menu...", end="")
    input()
    
    # Add extra newline characters for better spacing in the command line interface.
    print("\n\n\n\n")


if __name__ == "__main__":
    # This is the entry point of the program. If this script is executed, run the main menu function.
    main_menu()
    