import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        # if not, add new user to the database
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "firstname": request.form.get("firstname").lower(),
            "lastname": request.form.get("lastname").lower()
        }

        mongo.db.users.insert_one(register)
        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {} let's get cooking!".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "index", username=session["user"]))
            else:
                # passord isn't correct
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username isn't correct
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("index"))


@app.route("/search_page")
def search_page():
    return render_template("search_page.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("search_page.html", recipes=recipes)


@app.route("/categories/<category_name>")
def category(category_name):
    name = category_name
    category = mongo.db.categories.find_one({"category_name": category_name})
    recipes = list(mongo.db.recipes.find({"category_name": category_name}))
    return render_template(
        "category.html", recipes=recipes, name=name, category=category)


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
            "steps": request.form.getlist("steps"),
            "added_by": session["user"]
        }

        mongo.db.recipes.insert_one(recipe)
        flash("Your recipe was successfully added!")
        return redirect(url_for("add_recipe"))

    categories = list(mongo.db.categories.find())
    levels = list(mongo.db.levels.find())
    return render_template(
        "add_recipe.html", categories=categories,
        levels=levels)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name"),
            "recipe_title": request.form.get("title"),
            "description": request.form.get("description"),
            "difficulty_level": request.form.get("level"),
            "total_time": int(request.form.get("time")),
            "servings": int(request.form.get("servings")),
            "ingredients": request.form.getlist("ingredients"),
            "steps": request.form.getlist("steps"),
            "added_by": session["user"]
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, submit)
        flash("Recipe successfully updated !")

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    steps = recipe["steps"]
    ingredients = recipe["ingredients"]
    levels = list(mongo.db.levels.find())
    categories = list(mongo.db.categories.find())
    return render_template(
        "edit_recipe.html", recipe=recipe, categories=categories,
        steps=steps, ingredients=ingredients, levels=levels)


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe successfully deleted")
    return redirect(url_for("index"))


@app.route("/my_recipes/<username>")
def my_recipes(username):
    # grab the session user's username from db
    firstname = mongo.db.users.find_one(
        {"username": session["user"]})["firstname"]
    user_recipes = list(mongo.db.recipes.find({"added_by": username}))
    return render_template(
        "my_recipes.html", firstname=firstname,
        user_recipes=user_recipes)


@app.route("/categories/<category>/<recipe_url>/<recipe_id>")
def recipe(category, recipe_url, recipe_id):
    recipe = mongo.db.recipes.find_one(
        {"_id": ObjectId(recipe_id)})
    steps = recipe["steps"]
    ingredients = recipe["ingredients"]
    return render_template(
        "recipe.html", recipe=recipe, steps=steps,
        ingredients=ingredients)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)