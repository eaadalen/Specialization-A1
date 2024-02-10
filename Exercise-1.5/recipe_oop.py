class Recipe:
    all_ingredients = set()

    def __init__(self, name, ingredients, cooking_time):
        self.name = name
        self.ingredients = ingredients
        self.cooking_time = cooking_time
        self.difficulty = None

    def calculate_difficulty(self):
        if int(self.cooking_time) < 10 and len(self.ingredients) < 4:
            self.difficulty = "easy"
        elif int(self.cooking_time) < 10 and len(self.ingredients) >= 4:
            self.difficulty = "medium"
        elif int(self.cooking_time) >= 10 and len(self.ingredients) < 4:
            self.difficulty = "intermediate"
        elif int(self.cooking_time) >= 10 and len(self.ingredients) >= 4:
            self.difficulty = "hard"

    def add_ingredients(self, *args):
        for item in args:
            self.ingredients.append(item)
        self.update_all_ingredients()

    def get_ingredients(self):
        return self.ingredients
    
    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty
    
    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients
    
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            Recipe.all_ingredients.add(ingredient)

    def __str__(self): # String representation of the recipe
        self.calculate_difficulty()
        return f"Recipe Name: {self.name}\nIngredients: {', '.join(self.ingredients)}\nCooking Time: {self.cooking_time} minutes\nDifficulty: {self.difficulty}"
    

def recipe_search(data, search_term):
    print(f"Recipes that contain '{search_term}':\n")
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)


tea = Recipe("Tea", ["Tea Leaves", "Sugar", "Water"], 5)
coffee = Recipe("Coffee", ["Coffee Powder", "Sugar", "Water"], 5)
cake = Recipe("Cake", ["Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"], 50)
smoothie = Recipe("Banana Smoothie", ["Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"], 5)

recipes_list = [tea, coffee, cake, smoothie]

for ingredient in ["Water", "Sugar", "Bananas"]:
    print()
    recipe_search(recipes_list, ingredient)