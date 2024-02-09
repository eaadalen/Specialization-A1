class Recipe(object):
    def __init__(self, name, ingredients, cooking_time, difficulty):
        self.name = name
        self.ingredients = ingredients
        self.cooking_time = cooking_time
        self.difficulty = difficulty

    def calculate_difficulty(self):
        if int(self.cooking_time) < 10 and len(self.ingredients) < 4:
            self.difficulty = "easy"
        elif int(self.cooking_time) < 10 and len(self.ingredients) >= 4:
            self.difficulty = "medium"
        elif int(self.cooking_time) >= 10 and len(self.ingredients) < 4:
            self.difficulty = "intermediate"
        elif int(self.cooking_time) >= 10 and len(self.ingredients) >= 4:
            self.difficulty = "hard"

