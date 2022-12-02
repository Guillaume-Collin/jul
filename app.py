from flask import Flask, render_template, request
import pandas as pd
from random import randint

app = Flask(__name__)

COLUMNS = ["Trois choix", "Thematique", "Situation", "précision", "verbatim"]

def get_random_sentence(data):
    idx = randint(0, len(data) - 1)
    return data.iloc[idx]
    
@app.route("/", methods=['GET', 'POST'])
def index():
    data = pd.read_excel('data/citations.xlsx')

    possibilities = dict()
    all_possibilities = set()
    for column in COLUMNS:
        possibilities[column] = set(data[column])
        all_possibilities.update(possibilities[column])
    
    if request.method == 'POST':
        phrase = ''
        if request.form.get('selection') == 'Ton humeur Jul du jour':
            phrase = get_random_sentence(data['verbatim'])
            return render_template("citation.html", citation = phrase)

        elif request.form.get('selection') == 'Te présenter':
            phrase = get_random_sentence(data[data['Trois choix'] == "se présenter"]['verbatim'])
            return render_template("citation.html", citation = phrase)

        elif request.form.get('selection') == 'Parler Jul en toutes situations':
            categories = []
            possible_categories = list(set(data[data["Trois choix"] == "adaptée à la situation"]['Thematique']))
            for categorie in possible_categories:
                categories.append(categorie)
            print(categories)
            return render_template("situation_menu.html",len = len(categories), categories = categories)

        elif request.form.get('selection') in all_possibilities:
            for i, column in enumerate(COLUMNS):
                if request.form.get('selection') in possibilities[column]:
                    if COLUMNS[i + 1] == "verbatim":
                        phrase = get_random_sentence(data[data[column] == request.form.get('selection')]['verbatim'])
                        return render_template("citation.html", citation = phrase)

                    elif (len(set(data[data[column] == request.form.get('selection')][COLUMNS[i + 1]])) == 1):
                        phrase = get_random_sentence(data[data[column] == request.form.get('selection')]['verbatim'])
                        return render_template("citation.html", citation = phrase)
                        # empty
                    
                    else:
                        categories = []

                        possible_categories = list(set(data[data[column] == request.form.get('selection')][COLUMNS[i + 1]]))
                        for categorie in possible_categories:
                            categories.append(categorie)
                        return render_template("situation_menu.html", len = len(categories), categories = categories)
                        
    return render_template("selection_menu.html")


if __name__ == "__main__":
    app.directory='./'
    app.run(host='127.0.0.1', port=5000)