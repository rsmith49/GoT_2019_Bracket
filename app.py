from flask import Flask, render_template, request

from src.bracket import find_all_brackets, Bracket
from src.char_pred import PRED_TYPES
from src.show_state import get_curr_show_state
from src.utils import CHAR_TIERS, TIERS, CHAR_NAMES

app = Flask(__name__)


@app.route('/')
def home():
    return render_template(
        'index.html'
    )


@app.route('/results/')
def list_bracket_results():
    bracket_results = [
        {
            'rank': 'Place',
            'bracket_name': 'Bracket Name',
            'points': 'Points',
            'potential_points': 'Potential Points'
        }
    ]

    brackets = find_all_brackets()
    state = get_curr_show_state()

    rank = 1
    for bracket in sorted(brackets, key=lambda bracket: -bracket.points(state)):
        bracket_results.append({
            'rank': rank,
            'bracket_name': bracket.name,
            'points': bracket.points(state),
            'potential_points': bracket.potential_points(state)
        })

        rank += 1

    return render_template(
        'bracket_list.html',
        bracket_list=bracket_results
    )


@app.route('/brackets', methods=['GET'])
def bracket_creation_form():
    return render_template(
        'bracket_creation_form.html',
        tiers=TIERS,
        char_names=CHAR_NAMES,
        pred_types=PRED_TYPES
    )


@app.route('/brackets', methods=['POST'])
def create_bracket():
    bracket_name = request.form['bracket_name']
    char_preds = {
        char_name: {
            'pred_type': request.form[char_name + ' Prediction Type'],
            'pred_val': int(request.form[char_name + ' Week'])
        }
        for char_name in CHAR_TIERS
    }

    bracket = Bracket(name=bracket_name, **char_preds)
    try:
        bracket.save()
    except FileExistsError:
        return request.form['bracket_name'] + ' bracket could not be created, bracket with ' \
                                              'same name already exists'

    return request.form['bracket_name'] + ' bracket created!'

if __name__ == '__main__':
    app.run()
