# Menu randomnizer

If you all can't decide what to eat,
 try this!
It will help you figure out what you should eat !!

## Features
- A random food system that will make your life easier

  • Identify foods you are allergic to, dislike, or don't have.

  • Specify the country of the food you want to eat.

  • Identify the ingredient you want to include in the meal.
  
  • RANDOM it!! 

---
### ----------DOCKER----------
## Installation for Docker
how to install for Docker?
1. Clone project:
   ```bash
    git clone https://github.com/chinenar/Menu-Randomizer-web.git
    cd Menu-Radomizer-web
   ```
2. setup virtual environment
    ```bash
    python -m venv venv
    . ./venv/Scripts/activate
    pip install -r requirements.txt
   ```
3. run docker
   ```bash
   docker compose build
   docker compose up -d
   ```
4. Open new terminal that is not git bash. 
   ```bash
   docker exec -it meal-app /bin/sh #Now you can use application through docker
   app --help #for each command detail
   ```
5. To compose down 
   ```bash
   docker compose down
   ```
---

## Credits
This project uses data provided by [TheMealDB](https://www.themealdb.com/). 

Special thanks to TheMealDB for providing an amazing free API for developers to explore food and recipes.
