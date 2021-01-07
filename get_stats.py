# get_stats.py returns stats for a particular nba team and date range

from nba_api.stats.endpoints import teamdashboardbygeneralsplits
from team_names import teams
import pandas as pd


# start_date and end_date need to be in format of 'mm/dd/yyyy'
def get_team_stats(team, start_date, end_date, season='2020-21'):
    """Uses the nba_api to scrape team data from nba.com and returns a dataframe"""

    general_team_info = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=teams[team],
                                                                                  per_mode_detailed='Per100Possessions',
                                                                                  season=season,
                                                                                  date_from_nullable=start_date,
                                                                                  date_to_nullable=end_date,
                                                                                  timeout=120)
    gti = general_team_info.get_data_frames()[0]

    advanced_team_info = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=teams[team],
                                                                                   per_mode_detailed='Per100Possessions',
                                                                                   measure_type_detailed_defense='Advanced',
                                                                                   season=season,
                                                                                   date_from_nullable=start_date,
                                                                                   date_to_nullable=end_date,
                                                                                   timeout=120)

    ati = advanced_team_info.get_data_frames()[0]

    columns = ['W_PCT', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'PF',
               'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']

    data = [team, teams[team], gti.W_PCT, gti.FG_PCT, gti.FG3_PCT, gti.FT_PCT, gti.OREB, gti.DREB, gti.REB, gti.AST, gti.TOV, gti.STL,
            gti.BLK, gti.PF, gti.PLUS_MINUS, ati.OFF_RATING, ati.DEF_RATING, ati.TS_PCT]

    team_df = pd.concat(data, axis=1, keys=columns)

    return team_df


df = get_team_stats('Boston Celtics', '12/18/2020', '01/06/2021')
print(df)

