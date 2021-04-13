# make_csv.py creates a csv file of all nba teams to create the model with
from get_stats import get_team_stats
from team_names import teams
import pandas as pd


def get_all_teams(season):
    """
    Returns a dataframe of the data

    :return: It returns a dataframe of all 30 NBA teams and the selected columns
    """

    df = get_team_stats('Atlanta Hawks', season)
    try:
        for team in teams.keys():
            if team != 'Atlanta Hawks':
                print(team)
                team_stats = get_team_stats(team, season)
                df = df.append(team_stats, ignore_index=True)

    except Exception as e:
        print(f'Error occurred: {e}')

    return df


def main():
    """
    Creates a csv file of the dataframe
    """
    final_df = get_all_teams('2019-20')
    print(final_df)
    final_df.to_csv(r'C:\Users\student\honors\nba\nba_data\nba_data.csv', index=False)


if __name__ == '__main__':
    main()
