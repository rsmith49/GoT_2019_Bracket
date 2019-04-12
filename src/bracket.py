import json
import os

from src.char_pred import CharPred
from src.utils import CHAR_TIERS

DEFAULT_BRACKET_PATH = 'brackets/'


class Bracket:

    def __init__(self, filename=None, name=None, **kwargs):
        """
        :param filename:

        """
        if filename is not None:
            if len(kwargs) > 0:
                raise AttributeError('Filename and Character arguments present')

            with open(filename) as tmp_file:
                char_preds_json = json.load(tmp_file)

            self.char_preds = {
                char_name: CharPred(
                    char_preds_json['preds'][char_name]['pred_type'],
                    char_preds_json['preds'][char_name]['pred_val'],
                    CHAR_TIERS[char_name]
                )
                for char_name in char_preds_json['preds']
            }

            self.name = char_preds_json['name']
        else:
            if name is None:
                raise AttributeError('Need a name for the bracket')

            self.name = name
            self.char_preds = {}

            for char_name in kwargs:
               self.char_preds[char_name] = CharPred(
                   kwargs[char_name]['pred_type'],
                   kwargs[char_name]['pred_val'],
                   CHAR_TIERS[char_name]
               )

        if set(self.char_preds.keys()) != set(CHAR_TIERS.keys()):
            raise AttributeError('Some characters have been unset')

    def points(self, show_state):
        """
        :param show_state:

        :return:
        """
        return self._points(show_state, 'score_func')

    def potential_points(self, show_state):
        """

        :param show_state:
        :return:
        """
        return self._points(show_state, 'potential_score_func')

    def _points(self, show_state, score_type):
        """

        :param score_type:
        :return:
        """
        total_points = 0

        for char_name in show_state.state:
            total_points += self.char_preds[char_name]._points(
                show_state.state[char_name],
                score_type
            )

        return total_points

    def save(self, dirpath=DEFAULT_BRACKET_PATH):
        """
        Saves the bracket to a JSON file it can then be read from
        :return:
        """
        json_to_save = {
            'preds': {
                char_name: {
                    'pred_type': self.char_preds[char_name].pred_type,
                    'pred_val': self.char_preds[char_name].pred_val
                }
                for char_name in self.char_preds
            },
            'name': self.name
        }
        new_filename = self.name.replace(' ', '_').lower() + '_bracket.json'

        existing_files = os.listdir(dirpath)
        if new_filename in existing_files:
            raise FileExistsError()

        with open(dirpath + new_filename, 'w') as tmp_file:
            json.dump(json_to_save, tmp_file)


def find_all_brackets(dirpath=DEFAULT_BRACKET_PATH):
    """
    Finds and returns all the brackets saved in dirpath
    :param dirpath:
    :return:
    """
    bracket_files = os.listdir(dirpath)

    return [
        Bracket(filename=dirpath + bracket_filename)
        for bracket_filename in bracket_files
        if bracket_filename[-5:] == '.json'
    ]
