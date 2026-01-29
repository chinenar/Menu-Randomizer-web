from flask import Flask, request, render_template
from asgiref.wsgi import WsgiToAsgi
import requests
import random
import string

app = Flask(__name__)

# Function to fetch meals from TheMealDB API
def fetch_meals():
    while True:  # ลูปสุ่มไปเรื่อยๆ จนกว่าจะเจอข้อมูล
        try:
            random_letter = random.choice(string.ascii_lowercase)  # สุ่มตัวอักษร a-z
            url = f"https://www.themealdb.com/api/json/v1/1/search.php?f={random_letter}"
            response = requests.get(url, timeout=5)  # เพิ่ม timeout
            response.raise_for_status()  # Raise exception if HTTP status is not 200
            
            data = response.json()
            meals = data.get("meals", [])

            if meals:  # ถ้าเจอเมนูอาหาร
                print(f"Fetched {len(meals)} meals for letter '{random_letter}'")
                return meals  # ส่งข้อมูลเมนูกลับไปใช้

        except requests.RequestException as e:
            print(f"Error fetching meals: {e}, retrying...")

# Function to filter meals based on user input
def filter_meals(allergy, cuisine, main_ingredient):
    while True:  # ลูปสุ่มและกรองจนกว่าจะเจอเมนูอาหารที่ตรง
        meals = fetch_meals()
        filtered_meals = []
        
        # คำนวณจำนวนส่วนผสมสูงสุดในทุกเมนู
        max_ingredients = max(
            sum(1 for i in range(1, 21) if meal.get(f"strIngredient{i}", "")) for meal in meals
        )

        for meal in meals:
            # Extract ingredients ตามจำนวนที่คำนวณได้
            ingredients = [
                meal.get(f"strIngredient{i}", "").lower()
                for i in range(1, max_ingredients + 1)
                if meal.get(f"strIngredient{i}", "")
            ]

            # Check conditions
            if (
                (not allergy or allergy not in ingredients) and
                (not cuisine or cuisine.lower() in meal.get("strArea", "").lower()) and
                (not main_ingredient or main_ingredient in ingredients)
            ):
                filtered_meals.append(meal)

        if filtered_meals:  # ถ้าเจอเมนูที่ตรง
            return filtered_meals

@app.route("/", methods=["GET", "POST"])
def home():
    try:
        if request.method == "POST":
            # Get user inputs
            allergy = request.form.get("allergy", "").lower()
            cuisine = request.form.get("cuisine", "").lower()
            main_ingredient = request.form.get("main_ingredient", "").lower()

            # Filter meals until a valid meal is found
            filtered_meals = filter_meals(allergy, cuisine, main_ingredient)

            # Randomly select a meal from the filtered list
            meal = random.choice(filtered_meals)
            ingredients = [
                (meal.get(f"strIngredient{i}", ""), meal.get(f"strMeasure{i}", ""))
                for i in range(1, 21)
                if meal.get(f"strIngredient{i}", "")
            ]
            return render_template("index.html", meal=meal, ingredients=ingredients)

        # For GET requests, fetch and display a random meal
        meals = fetch_meals()
        meal = random.choice(meals)
        ingredients = [
            (meal.get(f"strIngredient{i}", ""), meal.get(f"strMeasure{i}", ""))
            for i in range(1, 21)
            if meal.get(f"strIngredient{i}", "")
        ]
        return render_template("index.html", meal=meal, ingredients=ingredients)

    except Exception as e:
        print(f"Unhandled error: {e}")
        return render_template("index.html", error="An unexpected error occurred. Please try again later.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
