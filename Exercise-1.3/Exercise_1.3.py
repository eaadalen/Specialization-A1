recipes_list = []
ingredients_list = []

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
    return(recipe)

print()
n = input("how many recipes do you want to enter? ")

print()

for i in range(int(n)):
    recipe = take_recipe()
    for item in recipe["ingredients"]:
        if not(item in ingredients_list):
            ingredients_list.append(item)
    recipes_list.append(recipe)

print()

for item in recipes_list:
    if int(item["cooking_time"]) < 10 and len(item["ingredients"]) < 4:
        difficulty = "easy"
    elif int(item["cooking_time"]) < 10 and len(item["ingredients"]) >= 4:
        difficulty = "medium"
    elif int(item["cooking_time"]) >= 10 and len(item["ingredients"]) < 4:
        difficulty = "intermediate"
    elif int(item["cooking_time"]) >= 10 and len(item["ingredients"]) <= 4:
        difficulty = "hard"
    print("Recipe: " + item["name"])
    print("Cooking Time (min): " + item["cooking_time"])
    print("Ingredients: ")
    for a in item["ingredients"]:
        print(a)
    print("Difficulty Level: " + difficulty)
    print()

ingredients_list.sort()
print("Ingredients Available Across All Recipes")
for item in ingredients_list:
    print(item)