# get_matches.py gets the daily matches for a specific date and the results of the games

from nba_api.stats.endpoints import leaguegamelog, scoreboard, leaguestandings
from team_names import teams



def get_match_results(date, season):
    """
    Returns the matchup and result of the game

    :param date: Day of games scheduled in form 'mm/dd/yyyy'
    :param season: Season in form of 'yyyy-yy'
    :return: [{Boston Celtics: Los Angeles Lakers}], ['W']
    """

    game_log = leaguegamelog.LeagueGameLog(season=season, league_id='00', date_from_nullable=date,
                                           date_to_nullable=date, season_type_all_star='Regular Season', timeout=120)
    game_log_dict = game_log.get_normalized_dict()
    list_of_teams = game_log_dict['LeagueGameLog']

    daily_match = {}
    win_loss = []
    score = []
    game_id = []

    for i in range(0, len(list_of_teams), 2):

        if '@' in list_of_teams[i]['MATCHUP']:

            away_team = list_of_teams[i]['TEAM_NAME']
            home_team = list_of_teams[i + 1]['TEAM_NAME']

            win_loss.append(list_of_teams[i + 1]['WL'])

            game_id.append(list_of_teams[i + 1]['GAME_ID'])

            score.append(list_of_teams[i + 1]['PTS'])
            score.append(list_of_teams[i]['PTS'])

        else:
            away_team = list_of_teams[i + 1]['TEAM_NAME']
            home_team = list_of_teams[i]['TEAM_NAME']

            win_loss.append(list_of_teams[i]['WL'])

            game_id.append(list_of_teams[i]['GAME_ID'])

            score.append(list_of_teams[i]['PTS'])
            score.append(list_of_teams[i + 1]['PTS'])

        daily_match.update({home_team: away_team})

    match_results = [daily_match, win_loss, score, game_id]

    return match_results


def get_daily_matches(date):
    """
    This method creates a dictionary of daily game matchups.

    :param date: Day of games scheduled in form 'mm/dd/yyyy'
    :return: A dictionary of game matchups {home_team:away_team}
    """

    daily_match = scoreboard.Scoreboard(league_id='00', game_date=date, timeout=120)
    daily_match_dict = daily_match.get_normalized_dict()
    games = daily_match_dict['GameHeader']

    match = {}

    for game in games:

        home_team_id = game['HOME_TEAM_ID']

        for team, team_id in teams.items():
            if team_id == home_team_id:
                home_team = team

        away_team_id = game['VISITOR_TEAM_ID']

        for team, team_id in teams.items():
            if team_id == away_team_id:
                away_team = team

        match.update({home_team: away_team})

    return match


def main():
    print(get_daily_matches('10/19/18'))
    print(get_match_results('10/19/18', '2018-19'))


main()
