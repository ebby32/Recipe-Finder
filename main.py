import tkinter
import webbrowser
from tkinter import *
import requests
import os
from dotenv import load_dotenv

load_dotenv()


SPOON_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

def open_recipe(url):
    webbrowser.open_new(url)

def get_ingredients():
    new_window = tkinter.Toplevel(window)
    ingre = input_ingredients.get()
    parameter = {
        'ingredients':ingre,
        'number':5,
        'apiKey': os.environ['SPOON_API_KEY']
    }
    response = requests.get(SPOON_URL, params=parameter)
    # print(response.json())
    data = response.json()



    for recipe in data:
        # print(recipe['title'])
        recipe_label = Label(new_window,text=recipe['title'], font = ('Times new Romans', 24, 'bold'), fg = 'blue', cursor= 'hand2')
        recipe_label.pack(pady = 10, padx = 50)

        # recipe_label.bind('<Button-1>', lambda e: open_recipe('www.google.com'))

        parameter = {
            'query':recipe['title'],
            'number': 1,
            'apiKey': os.environ['SPOON_API_KEY']

        }

        response = requests.get('https://api.spoonacular.com/recipes/complexSearch',params=parameter)
        # print(response.json()['results'][0]['id'])

        try:
            id = response.json()['results'][0]['id']

            params_info = {
                'id':response.json()['results'][0]['id'],
                'apiKey': os.environ['SPOON_API_KEY']
            }

            recipe_info = requests.get(f'https://api.spoonacular.com/recipes/{id}/information',params=params_info)

            # print(recipe_info.json())

            url = recipe_info.json()['sourceUrl']
            recipe_label.bind('<Button-1>', lambda e: open_recipe(url))

        except IndexError:
            continue








# creating UI
window = Tk()
window.title('Recipe Finder')
window.config(padx=50, pady= 50)

canvas = Canvas(width=250, height= 50, bg='blue')
canvas.grid(row=1, column = 1)

canvas.create_text(
    125,25,
    width=250,
    text = "Recipe Finder",
    font = ('Times new Romans', 24, 'bold'),
    fill = 'white'
)

#Ingredients input field
ingredients = Label(text = 'Ingredients; Enter your ingredients here.')
ingredients.grid(column = 1, row = 3)

input_ingredients = Entry(width=35)
input_ingredients.grid(column = 1, row =4)

search_button = Button(text= 'Search', command=get_ingredients)
search_button.grid(column = 1, row = 5)




window.mainloop()