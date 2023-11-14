from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask_app.models import recipe
from flask_app.models.user import User

@app.route('/recipes/new', methods=['GET'])
def new_recipe():
    return render_template('add_recipe.html')

@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' in session:  
        user_id = session['user_id']
        recipe_data = {
            'user_id': user_id,  
            'name': request.form['recipe_name'],
            'description': request.form['recipe_description'],
            'instructions': request.form['recipe_instructions'],
            'under_30': request.form['recipe_cook_time'] == 'yes',
            'date_made': request.form['date_made']
        }

        recipe.Recipe.create_recipe(recipe_data)
        flash("Successfully added recipe", "recipe")
        return redirect('/recipes')
    else:
        flash("You must log in to access that", "login")
        return redirect('/')

@app.route('/recipes/view/<int:recipe_id>')
def view_recipe(recipe_id):
    # Retrieve the recipe by ID from the database
    recipe_data = recipe.Recipe.get_recipe_by_user_id(recipe_id)
    # Check if the recipe exists
    return render_template('view_recipe.html', recipe=recipe_data)
    
# edit recipe
@app.route('/recipes/edit/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):

    recipe_data = recipe.Recipe.get_recipe_by_user_id(recipe_id)

    # Check if the recipe exists
    if not recipe_data:
        flash("Recipe not found", "error")
        return redirect(url_for('homepage'))

    if request.method == 'POST':

        updated_data = {
            'name': request.form['recipe_name'],
            'description': request.form['recipe_description'],
            'instructions': request.form['recipe_instructions'],
            'under_30': request.form['recipe_cook_time'] == 'yes',
            'date_made': request.form['date_made']
        }

        print(f"Updating recipe with ID: {recipe_data.recipes_table_id}, Data: {updated_data}")

        recipe.Recipe.update_recipe(recipe_data.recipes_table_id, updated_data)
        flash("Recipe updated successfully", "success")
        return redirect(url_for('homepage'))
    
    if session['user_id'] == recipe_data.user_id:
        user = User.get_by_id(session['user_id'])
        return render_template('edit_recipe.html', recipe=recipe_data, user=user)
    flash("You thought I didn't protect against that?", "hacker")
    return redirect('/')
    # Pass the existing recipe data to the template

# delete recipe
@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    # Retrieve the recipe by ID from the database
    recipe_data = recipe.Recipe.get_recipe_by_id(recipe_id)

    # Check if the recipe exists
    if not recipe_data:
        flash("Recipe not found", "error")
        return redirect(url_for('homepage'))

    # Check if the current user is the owner of the recipe
    if session['user_id'] == recipe_data.user_id:
        # Delete the recipe from the database
        recipe.Recipe.delete_recipe(recipe_data.recipes_table_id)
        flash("Recipe deleted successfully", "success")
        return redirect(url_for('homepage'))
    else:
        flash("You thought I didn't protect against that?", "hacker")
        return redirect('/')