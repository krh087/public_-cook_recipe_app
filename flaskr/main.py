from flaskr import app, db
from flaskr.models.database import User,Recipe,Ingredient,Step,Recipe_ingredient,Recipe_step

from flask import render_template, request, redirect, url_for, session
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user

from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

DATABASE = './flaskr/database.db'
app.secret_key = b'gqJpZCI1InFad3OizQ'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'GET':
        recipes = Recipe.query.filter_by(user_id=current_user.id).all()
        return render_template(
            'index.html', recipes=recipes, enumerate=enumerate, format=format
        )

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        input_email = request.form['email']
        input_password = request.form['password']
        user = User.query.filter_by(email=input_email).one_or_none()
        if check_password_hash(user.password, input_password):
            login_user(user)
            return redirect("/")
        else:
            return render_template(
                'login.html',
        )
    if request.method == 'GET':
        return render_template(
            'login.html',
        )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(
            username = username,
            email = email,
            password = generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    if request.method == 'GET':
        return render_template(
            'signup.html'
        )

@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    if request.method == 'GET':
        return render_template('add_recipe.html')
    if request.method == 'POST':
        # 固定の入力欄の値を取得
        title = request.form.get("title")
        cook_time = request.form.get("cook_time")
        memo = request.form.get("memo")
        # 動的な入力欄の値(list型)を取得
        ingredients = request.form.getlist("dynamic_ingredient")
        quantities = request.form.getlist("dynamic_quantity")
        instructions = request.form.getlist("dynamic_instruction")
        # DB書込
        recipe = Recipe(
            user_id=current_user.id,
            title=title,
            step_photo_path="recipe.img",
            memo=memo,
            cook_time=cook_time
        )
        db.session.add(recipe)
        db.session.commit()
        for ingredient, quantity in zip(ingredients, quantities):
            ingredient = Ingredient(
                ingredient_name = ingredient,
                quantity = quantity
            )
            db.session.add(ingredient)
            db.session.commit()
            recipe_ingredient = Recipe_ingredient(
                recipe_id = recipe.id,
                ingredient_id = ingredient.id
            )
            db.session.add(recipe_ingredient)
            db.session.commit()
        for step_number, instruction in enumerate(instructions, 1):
            step = Step(
                step_number = step_number, #1~n
                content = instruction,
                step_photo_path = "step.img"
            )
            db.session.add(step)
            db.session.commit()
            recipe_step = Recipe_step(
                recipe_id = recipe.id,
                step_id = step.id
            )
            db.session.add(recipe_step)
            db.session.commit()
        return redirect('/')

@app.route('/recipe_detail/<string:recipe_id>')
@login_required
def recipe_detail(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).one_or_none()
    recipe_ingredients = Recipe_ingredient.query.filter_by(recipe_id=recipe_id).all()
    ingredients = []
    for recipe_ingredient in recipe_ingredients:
        ingredient = Ingredient.query.filter_by(id=recipe_ingredient.ingredient_id).one_or_none()
        ingredients.append(ingredient)
    recipe_steps = Recipe_step.query.filter_by(recipe_id=recipe_id).all()
    steps = []
    for recipe_step in recipe_steps:
        step = Step.query.filter_by(id=recipe_step.step_id).one_or_none()
        steps.append(step)
    return render_template(
        'recipe_detail.html', recipe=recipe, ingredients=ingredients, steps=steps, format=format
    )

@app.route('/delete_recipe/<string:recipe_id>')
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    recipe_ingredients = Recipe_ingredient.query.filter_by(recipe_id=recipe_id).all()
    for recipe_ingredient in recipe_ingredients:
        ingredient = Ingredient.query.filter_by(id=recipe_ingredient.ingredient_id).one_or_none()
        db.session.delete(recipe_ingredient)
        db.session.delete(ingredient)
    recipe_steps = Recipe_step.query.filter_by(recipe_id=recipe_id).all()
    for recipe_step in recipe_steps:
        step = Step.query.filter_by(id=recipe_step.step_id).one_or_none()
        db.session.delete(recipe_step)
        db.session.delete(step)
    db.session.delete(recipe)
    db.session.commit()
    return redirect('/')
