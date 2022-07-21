from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.recipe_model import Recipe

@app.route('/recipes')
def success():
    if 'user_email' not in session:
        return redirect('/')
    recipes = Recipe.get_all_recipes()
    return render_template('recipes.html', recipes=recipes)

@app.route('/recipe/new')
def display_new():
    if 'user_email' not in session:
        return redirect('/')
    return render_template("create_recipe.html")

@app.route('/view_recipe/<int:id>')
def view_recipe(id):
    if 'user_email' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    recipe = Recipe.get_single_recipe(data)
    return render_template("view_recipe.html", recipe=recipe)

@app.route('/recipes/create', methods=['post'])
def create_recipe():
    if 'user_email' not in session:
        return redirect('/')
    #validate

    if Recipe.validate_recipe(request.form) == False:
        print('validation failed')
        return redirect('/recipe/new')
    else:
        #create recipe
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'cooked_date': request.form['cooked_date'],
            'under_30': request.form['under_30'],
            'users_id': session['user_id']
        }
        
        Recipe.create_recipe(data)
        return redirect('/recipes')

@app.route('/delete_recipe/<int:id>')
def delete_recipe(id):
    data = {
        'id': id
    }
    Recipe.delete_recipe(data)
    return redirect('/recipes')

@app.route('/edit_recipe/<int:id>')
def edit_recipe(id):
    if 'user_email' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    recipe = Recipe.get_recipe_to_edit(data)
    print(recipe)
    return render_template("edit_recipe.html", recipe=recipe)

@app.route('/recipes/edit/<int:id>', methods={'post'})
def update(id):
    if 'user_email' not in session:
        return redirect('/')
    #validate
    if Recipe.validate_recipe(request.form) == False:
        print('validation failed')
        return redirect('/recipe/new')
    else:
        #create recipe
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'cooked_date': request.form['cooked_date'],
            'under_30': request.form['under_30'],
            'id': id
        }
        
        Recipe.update_recipe(data)
        return redirect(f'/view_recipe/{id}')

