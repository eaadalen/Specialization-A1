import pickle

def take_recipe():
    name = input("enter recipe name: ")
    cooking_time = input("enter cooking time (in minutes): ")

    done = False
    ingredients = []
    while done == False:
        item = input("enter ingredient: ")
        ingredients.append(item)
        response = input("add another ingredient (y/n)?: ")
        if response == "n":
            done = True
    
    print()
    recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}
    recipe_with_DL = calc_difficulty(recipe)   #add difficulty level (DL) to recipe
    return(recipe_with_DL)

def calc_difficulty(recipe):
    if int(recipe["cooking_time"]) < 10 and len(recipe["ingredients"]) < 4:
        difficulty = "easy"
    elif int(recipe["cooking_time"]) < 10 and len(recipe["ingredients"]) >= 4:
        difficulty = "medium"
    elif int(recipe["cooking_time"]) >= 10 and len(recipe["ingredients"]) < 4:
        difficulty = "intermediate"
    elif int(recipe["cooking_time"]) >= 10 and len(recipe["ingredients"]) >= 4:
        difficulty = "hard"
    print("Recipe: " + recipe["name"])
    print("Cooking Time (min): " + recipe["cooking_time"])
    print("Ingredients: ")
    for a in recipe["ingredients"]:
        print(a)
    print("Difficulty Level: " + difficulty)
    print()
    
    recipe["difficulty"] = difficulty
    return recipe

filename = input("Enter a filename: ")

recipes_list = []
all_ingredients = []

with open(filename, "rb") as file:
    file.seek(0)
    data = pickle.load(file)

'''
try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found")
except:
    print("Failed reading file")
else:
    file.close()
'''

n = input("How many recipes would you like to enter? ")

for i in range(int(n)):
    recipe = take_recipe()
    recipes_list.append(recipe)
    for item in recipe["ingredients"]:
        if not(item in all_ingredients):
            all_ingredients.append(item)

export_data = {"recipes_list" : recipes_list, "all_ingredients" : all_ingredients}

try:
    with open(filename, '2b') as file:
        pickle.dump(export_data, file)
except FileNotFoundError:
    print("File not found")
except:
    print("Failed writing file")
else:
    file.close()