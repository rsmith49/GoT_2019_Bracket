import json

from src.utils import CHAR_TIERS

DEFAULT_SHOW_STATE_FILENAME = 'Show_State.json'


class CharState:
    def __init__(self, char_name, char_state_json):
        """

        """
        self.char_name = char_name
        self.char_state = char_state_json

    def week_died(self):
        """
        Assuming the entire char_state_json is just going to be the
        week that they died or None
        :return:
        """
        return self.char_state


class ShowState:

    def __init__(self, filename=None, **kwargs):
        """
        :param filename:

        """
        if filename is not None:
            with open(filename) as tmp_file:
                self.state = json.load(tmp_file)
        else:
            self.state = {}

        for char_name in kwargs:
            if char_name not in CHAR_TIERS:
                raise AttributeError('Unrecognized Character: ' + str(char_name))

            self.state[char_name] = kwargs[char_name]

        for char_name in self.state:
            self.state[char_name] = CharState(char_name, self.state[char_name])


def get_curr_show_state(filename=DEFAULT_SHOW_STATE_FILENAME):
    return ShowState(filename=filename)
