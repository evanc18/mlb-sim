from SQLGnome import SQLGnome
import pandas as pd
from data_loader import DB_PATH


def build_at_bats():
    q_in = []
    sqlgnome = SQLGnome(q_in, DB_PATH, 1, 1)
    sqlgnome.connect_db()
    data, keys = sqlgnome.filter_rows('statcast',  filter='[game_date] = "2021-11-02"', verbose=False)
    data = pd.DataFrame(data=data, columns=keys)
    print(data)
    print(data['events'].unique())
    pa_end_events = ['field_out', 'home_run', 'single', 'strikeout', 'sac_fly', 'walk', 'hit_by_pitch', 'double', 'field_error', 'grounded_into_double_play', 'force_out', 'triple', 'fielders_choice_out', 'double_play', 'sac_bunt',]

if __name__ == "__main__":
    build_at_bats()