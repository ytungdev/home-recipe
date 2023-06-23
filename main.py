from flask import Flask, request, render_template, redirect, url_for, jsonify, flash
from dbConnection import DBconnection
from models import Dish, Ingredient
import os
from dotenv import load_dotenv




load_dotenv()
URL = os.getenv('DATABASE_URL')
USERNAME = os.getenv('DATABASE_USERNAME')
PASSWORD = os.getenv('DATABASE_PASSWORD')
db = DBconnection(URL, USERNAME, PASSWORD)

app = Flask(__name__)
app.secret_key = bytes(os.getenv('APP_SECRET_KEY'), 'UTF-8')

@app.route('/')
def index():
    data = {
        "dish":Dish().getAll(),
        "ingredient": Ingredient().getAll()
    }
    return render_template('main.html', data=data)

@app.get('/dishes')
def showDishes():
    result = Dish().getStructure()
    return jsonify(result)
@app.get('/ingredients')
def showIngredients():
    result = Ingredient().getAll()
    return jsonify(result)

@app.post('/add/dish')
def add_dish():
    name = request.form['name']
    name_chi = request.form['name_chi']
    category = request.form['category']
    style = request.form['style']
    ingredients = request.form.getlist('ingredients[]')
    res = Dish().add(name,name_chi,category,style, ingredients)
    print(f"add d : '{name}', '{name_chi}', '{ingredients}'")
    print(res)
    if not res:
        flash('Invalid dish', 'dish')
    if res == 'name error':
        flash('Invalid dish : name is required', 'dish')
    return redirect(url_for('index'))
    
@app.post('/add/ingredient')
def add_ingredient():
    name = request.form['name']
    name_chi = request.form['name_chi']
    print(f"add i : '{name}', '{name_chi}'")
    res = Ingredient().add(name, name_chi)
    print(res)
    if not res:
        flash('Invalid ingredient : ingredient already exist', 'ingredient')
    if res == 'name error':
        flash('Invalid ingredient : name is required', 'ingredient')
    return redirect(url_for('index'))

@app.post('/search')
def dbSearch():
    text = request.json['data']
    result = Ingredient().search(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5001, debug=True)


