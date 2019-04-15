PRED_TYPES = {
    'DIES_BY': {
        'week_values': {
            1: 15,
            2: 13,
            3: 11,
            4: 9,
            5: 7,
            6: 5
        },
        'score_func': lambda week, pred_week, week_val, curr_week:
            week_val if week is not None and week <= pred_week else 0,
        'potential_score_func': lambda week, pred_week, week_val, curr_week:
            week_val if (week is None and curr_week < pred_week) or (week is not None and week <= pred_week) else 0
    },
    'DIES_ON': {
        'week_values': {
            1: 15,
            2: 15,
            3: 15,
            4: 15,
            5: 15,
            6: 15
        },
        'score_func': lambda week, pred_week, week_val, curr_week:
            week_val if week is not None and week == pred_week else 0,
        'potential_score_func': lambda week, pred_week, week_val, curr_week:
            week_val if (week is None and curr_week < pred_week) or (week is not None and week == pred_week) else 0
    },
    'LIVES': {
        'week_values': {
            ndx: 10
            for ndx in range(1, 7)
        },
        # We're going to say week = 7 means the character has survived the whole season
        'score_func': lambda week, pred_week, week_val, curr_week:
            week_val if week == 7 else 0,
        'potential_score_func': lambda week, pred_week, week_val, curr_week:
            week_val if week is None or week == 7 else 0
    }
}


class CharPred:

    def __init__(self, pred_type, pred_val, char_tier):
        """

        :param pred_type:
        :param pred_val: The week will be shortened to 6 if greater than 6,
                         and 1 if less than 1
        :param char_tier:
        """
        if pred_type not in PRED_TYPES:
            raise AttributeError('Unrecognized Prediction Type: ' + str(pred_type))

        self.pred_type = pred_type
        self.pred_val = max(min(pred_val, 6), 1)
        self.char_tier = char_tier

    def points(self, char_state):
        """

        :param char_state:
        :return:
        """
        return self._points(char_state, 'score_func')

    def potential_points(self, char_state):
        """

        :param char_state:
        :return:
        """
        return self._points(char_state, 'potential_score_func')

    def _points(self, char_state, score_type):
        """

        :param char_state:
        :return:
        """
        res_points = PRED_TYPES[self.pred_type][score_type](
            char_state.week_died(),
            self.pred_val,
            PRED_TYPES[self.pred_type]['week_values'][self.pred_val],
            char_state.curr_week
        )

        return 2 ** (self.char_tier - 1) * res_points
