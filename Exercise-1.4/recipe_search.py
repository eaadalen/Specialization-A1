import pickle

def display_recipe(recipe):
    print(recipe["name"])
    print(recipe["cooking_time"])
    print(recipe["ingredients"])
    print(recipe["difficulty"])

def search_ingredient(data):
    print(data["all_ingredients"])
    try:
        ingredient_searched = input("Enter your chosen ingredient: ")
    except:
        print("Index not valid")
    else:
        for item in data["recipes_list"]:
            if ingredient_searched in item["ingredients"]:
                print(item)
        file.close()

recipe_data = input("Enter the filename containing the recipe data: ")

try:
    with open(recipe_data, "rb") as file:
        data = pickle.load(file)
except:
    print("File not found")
else:
    search_ingredient(data)
    file.close()