from flask import Flask, render_template, request
import random
from datetime import datetime

app = Flask(__name__)

class RecipeGenerator:
    def __init__(self):
        self.cuisines = {
            'italian': ['Pasta Carbonara', 'Margherita Pizza', 'Risotto', 'Bruschetta', 'Tiramisu'],
            'mexican': ['Tacos', 'Enchiladas', 'Burritos', 'Quesadillas', 'Churros'],
            'indian': ['Chicken Curry', 'Vegetable Biryani', 'Samosas', 'Naan Bread', 'Gulab Jamun'],
            'chinese': ['Fried Rice', 'Dumplings', 'Chow Mein', 'Spring Rolls', 'Moon Cakes'],
            'american': ['Cheeseburger', 'Hot Dog', 'Apple Pie', 'Fried Chicken', 'Brownies'],
            'japanese': ['Sushi Rolls', 'Ramen', 'Tempura', 'Miso Soup', 'Matcha Ice Cream'],
            'mediterranean': ['Hummus', 'Falafel', 'Greek Salad', 'Baklava', 'Shawarma']
        }
        
        self.ingredients = {
            'vegetarian': ['tofu', 'beans', 'lentils', 'vegetables', 'cheese', 'eggs'],
            'non-vegetarian': ['chicken', 'beef', 'pork', 'fish', 'shrimp'],
            'vegan': ['tofu', 'tempeh', 'beans', 'lentils', 'vegetables', 'nuts']
        }
        
        self.cooking_methods = ['Grilled', 'Baked', 'Fried', 'Steamed', 'Roasted', 'Stir-fried']
        self.spices = ['salt', 'pepper', 'cumin', 'coriander', 'paprika', 'turmeric', 'garlic powder']
        
    def generate_recipe(self, cuisine=None, diet=None, cooking_time=None):
        if cuisine is None:
            cuisine = random.choice(list(self.cuisines.keys()))
        if diet is None:
            diet = random.choice(list(self.ingredients.keys()))
        
        dish = random.choice(self.cuisines[cuisine])
        main_ingredient = random.choice(self.ingredients[diet])
        method = random.choice(self.cooking_methods)
        
        if cooking_time is None:
            cooking_time = random.randint(10, 120)
        
        num_spices = random.randint(2, 5)
        spice_list = random.sample(self.spices, num_spices)
        
        instructions = [
            f"Prepare all ingredients by cleaning and chopping as needed.",
            f"Marinate the {main_ingredient} with {', '.join(spice_list[:-1])} and {spice_list[-1]}.",
            f"{method} the {main_ingredient} for about {cooking_time//2} minutes.",
            f"Combine with other ingredients to make {dish}.",
            f"Cook for another {cooking_time//2} minutes until done.",
            "Serve hot and enjoy!"
        ]
        
        recipe = {
            "title": f"{method} {main_ingredient} {dish}",
            "cuisine": cuisine.capitalize(),
            "diet": diet.capitalize(),
            "cooking_time": f"{cooking_time} minutes",
            "servings": random.randint(1, 8),
            "ingredients": {
                "main": main_ingredient,
                "spices": spice_list,
                "other": ["olive oil", "water", random.choice(['fresh herbs', 'lemon juice', 'yogurt'])]
            },
            "instructions": instructions,
            "date_generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return recipe

@app.route('/', methods=['GET', 'POST'])
def home():
    generator = RecipeGenerator()
    recipe = None
    now = datetime.now()
    
    if request.method == 'POST':
        cuisine = request.form.get('cuisine')
        diet = request.form.get('diet')
        cooking_time = request.form.get('cooking_time')
        
        if cooking_time:
            try:
                cooking_time = int(cooking_time)
            except ValueError:
                cooking_time = None
        
        recipe = generator.generate_recipe(
            cuisine if cuisine != 'any' else None,
            diet if diet != 'any' else None,
            cooking_time
        )
    
    return render_template('index.html', 
                         recipe=recipe, 
                         cuisines=generator.cuisines.keys(),
                         now=now)

if __name__ == '__main__':
    app.run(debug=True)