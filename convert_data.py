from datetime import date, timedelta
import pandas as pd
import requests

from get_stats import get_team_stats_dict
from get_matches import get_match_results
from available_stats import available_stats


# [{'Sacramento Kings': 'Boston Celtics', 'Charlotte Hornets': 'Philadelphia 76ers'}, ['W', 'L']]
# team stats is a dataframe
def to_dataframe(daily_games, start_date, end_date, season):  # , mean_dict, std_dict):
    full_dataframe = []
    game_number = 0  # counter to match with the correct game
    daily_results = daily_games[1]  # win or loss for each game
    score = daily_games[2]
    game_id = daily_games[3]

    for home_team, away_team in daily_games[0].items():  # loops through matchups
        home_team_stats = get_team_stats_dict(home_team, start_date, end_date, season)
        away_team_stats = get_team_stats_dict(away_team, start_date, end_date, season)

        current_game = [home_team, away_team]

        current_game.append(game_id[game_number])

        current_game.append(score.pop(0))

        for stat, stat_type in available_stats.items():
            current_game.append(home_team_stats[stat])

        current_game.append(score.pop(0))

        for stat, stat_type in available_stats.items():
            current_game.append(away_team_stats[stat])

        if daily_results[game_number] == 'W':
            result = 1
        else:
            result = 0

        current_game.append(result)
        game_number += 1

        print(current_game)

        full_dataframe.append(current_game)

    return full_dataframe


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def training_set(start_year, start_month, start_day, end_year, end_month, end_day, season, season_start):
    start_date = date(start_year, start_month, start_day)
    end_date = date(end_year, end_month, end_day)

    total_games = []

    for single_date in date_range(start_date, end_date):
        current_date = single_date.strftime('%m/%d/%Y')
        print(current_date)

        previous_day = single_date - timedelta(days=1)
        previous_day_formatted = previous_day.strftime('%m/%d/%Y')

        current_day_games = get_match_results(current_date, season)
        current_day_games_with_stats = to_dataframe(current_day_games, season_start, previous_day_formatted, season)

        for game in current_day_games_with_stats:
            game.append(current_date)
            total_games.append(game)

    print(total_games)
    return total_games


def make_dataframe(game_list):
    games = pd.DataFrame(game_list,
                         columns=['Home', 'Away', 'Game_ID', 'H_Score', 'H_W_PCT', 'H_FG_PCT', 'H_FG3_PCT', 'H_FT_PCT',
                                  'H_REB', 'H_AST', 'H_TOV', 'H_STL',
                                  'H_BLK', 'H_PLUS_MINUS', 'H_OFF_RATING', 'H_DEF_RATING', 'H_TS_PCT', 'A_Score',
                                  'A_W_PCT', 'A_FG_PCT', 'A_FG3_PCT',
                                  'A_FT_PCT', 'A_REB', 'A_AST', 'A_TOV', 'A_STL',
                                  'A_BLK', 'A_PLUS_MINUS', 'A_OFF_RATING', 'A_DEF_RATING', 'A_TS_PCT', 'Result',
                                  'Date'])

    print(games)
    return games


def main():
    attempts = 10

    for i in range(attempts):
        try:
            #start day has to be at least three days after the start of the season
            all_games = training_set(start_year=2020, start_month=12, start_day=27, end_year=2021, end_month=3,
                                     end_day=20,
                                     season='2020-21', season_start='12/22/2020')
            df = make_dataframe(all_games)

            print(df)
            df.to_csv(r'C:\Users\student\honors\nba\nba_data\nba_df_2020.csv', index=False)
        except requests.exceptions.ReadTimeout or ValueError:
            if i < attempts - 1:
                continue
            else:
                raise
        break


if __name__ == '__main__':
    main()