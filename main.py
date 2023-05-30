from flask import Flask, request, render_template, redirect, url_for
from dbConnection import DBconnection
from models import Dish, Ingredient

app = Flask(__name__)
db = DBconnection("bolt://localhost:7687", "neo4j", "password")


@app.route('/')
def index():
    data = {
        "dish":[],
        "ingredient": Ingredient().getAll()
    }
    dishs = Dish().getAll()
    for n in dishs:
        ingr = Dish().getIngredient(n['name'])
        obj = {
            "name" : Dish.format(n['name']),
            "name_chi" : Dish.format(n['name_chi'], True),
            'ingredient':[ {
                "name":Ingredient.format(i["name"]),
                "name_chi":Ingredient.format(i["name_chi"], True)
            } for i in ingr]
        }
        data["dish"].append(obj)
    return render_template('main.html', data=data)


@app.post('/add/dish')
def add_dish():
    name = request.form['name']
    name_chi = request.form['name_chi']
    print(f"add d : '{name}', '{name_chi}'")
    return redirect(url_for('index'))
    
@app.post('/add/ingredient')
def add_ingredient():
    name = request.form['name']
    name_chi = request.form['name_chi']
    print(f"add i : '{name}', '{name_chi}'")
    Ingredient().add(name, name_chi)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=5001, debug=True)
