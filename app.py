import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    categories = list(mongo.db.categories.find())
    return render_template("index.html", categories=categories)


@app.route("/categories/<category_name>")
def category(category_name):
    name = category_name
    recipes = list(mongo.db.recipes.find({"category_name": category_name}))
    return render_template("category.html", recipes=recipes, name=name)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe = {
            "category_name": request.form.get("category_name"),
            "recipe_title": request.form.get("title"),
            "description": request.form.get("description"),
            "difficulty_level": request.form.get("level"),
            "total_time": int(request.form.get("time")),
            "servings": int(request.form.get("servings")),
            "ingredients": request.form.getlist("ingredients"),
            "steps": request.form.getlist("steps")
        }

        mongo.db.recipes.insert_one(recipe)
        flash("Your recipe was successfully added")
        return redirect(url_for("add_recipe"))

    categories = list(mongo.db.categories.find())
    levels = list(mongo.db.levels.find())
    return render_template(
        "add_recipe.html", categories=categories,
        levels=levels)


@app.route("/categories/<category>/<recipe_url>")
def recipe(category, recipe_url):
    recipe_url_formatted = recipe_url.replace("-", " ")
    recipe = list(mongo.db.recipes.find(
        {"recipe_title": recipe_url_formatted}))
    steps = recipe[0]["steps"]
    ingredients = recipe[0]["ingredients"]
    return render_template(
        "recipe.html", recipe=recipe, steps=steps,
         ingredients=ingredients)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)