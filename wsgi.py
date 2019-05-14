from flask import Flask, render_template, request

from src.bracket import find_all_brackets, Bracket, DEFAULT_BRACKET_PATH
from src.char_pred import PRED_TYPES
from src.show_state import get_curr_show_state
from src.utils import CHAR_TIERS, TIERS, CHAR_NAMES

application = Flask(__name__)


@application.route('/')
def home():
    return render_template(
        'index.html'
    )


@application.route('/results/')
def list_bracket_results():
    bracket_results = []

    brackets = find_all_brackets()
    state = get_curr_show_state()

    rank = 1
    for bracket in sorted(brackets, key=lambda bracket: (
            -bracket.points(state),
            -bracket.potential_points(state)
    )):
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


@application.route('/brackets', methods=['GET'])
def bracket_creation_form():
    return render_template(
        'bracket_creation_form.html',
        tiers=TIERS,
        char_names=CHAR_NAMES,
        pred_types=PRED_TYPES
    )


@application.route('/brackets', methods=['POST'])
def create_bracket():
    return render_template(
        'bracket_created.html',
        message="Time to submit brackets has ended"
    )


@application.route('/brackets/<bracket_name>')
def show_bracket(bracket_name):
    bracket = Bracket(
        filename=DEFAULT_BRACKET_PATH + bracket_name.replace(' ', '_') + '_bracket.json'
    )
    show_state = get_curr_show_state()

    char_preds = sorted(
        [
            {
                'char_name': char_name,
                'win_perc': bracket.char_win_percs[char_name],
                'char_tier': bracket.char_preds[char_name].char_tier,
                'pred_type': bracket.char_preds[char_name].pred_type,
                'pred_week': bracket.char_preds[char_name].pred_val,
                'points': bracket.char_preds[char_name].points(
                    show_state.state[char_name]
                ),
                'potential_points': bracket.char_preds[char_name].potential_points(
                    show_state.state[char_name]
                )
            }
            for char_name in bracket.char_preds
        ],
        key=lambda x: (x['char_tier'], x['char_name'])
    )

    return render_template(
        'bracket_show.html',
        bracket_name=bracket.name,
        char_preds=char_preds,
        bracket_num_wins=bracket.num_wins
    )


@application.route('/update_show_state', methods=['POST'])
def update_show_state():
    pass

if __name__ == '__main__':
    application.run(host='0.0.0.0', port='8080')
