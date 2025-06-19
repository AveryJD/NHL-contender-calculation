
# Imports
import pandas as pd
import constants


# ====================================================================================================
# FUNCTION FOR GATHERING RELEVANT DATA
# ====================================================================================================

def get_relevant_data(season: str, team_abbrev: str) -> pd.Series:
    """
    ADD
    """

    # Load data
    skaters_df = pd.read_csv(f'raw_data/{season}_skaters.csv')
    goalies_df = pd.read_csv(f'raw_data/{season}_goalies.csv')
    teams_df = pd.read_csv(f'raw_data/{season}_teams.csv')


    # Get dataframe of forwards of the given team
    forward_df = skaters_df[(skaters_df['team'] == team_abbrev) &
                           (skaters_df['position'] != 'D') &
                           (skaters_df['situation'] == 'all')]
    
    # Get the top 12 forwards
    forward_df = forward_df.sort_values(by="games_played", ascending=False).reset_index(drop=True)
    forward_df = forward_df.iloc[:12]

    # Get different lines of forwards based on average icetime
    forward_df['icetime/games_played'] = forward_df['icetime'] / forward_df['games_played']
    forward_df = forward_df.sort_values(by="icetime/games_played", ascending=False).reset_index(drop=True)

    top_six_f = forward_df.iloc[:6]
    bottom_six_f = forward_df.iloc[6:12]

    # Get forward lines total average game scores
    top_six_f_score = (top_six_f['gameScore'] / top_six_f['games_played']).sum()
    bottom_six_f_score = (bottom_six_f['gameScore'] / bottom_six_f['games_played']).sum()

    

    # Get dataframe of defensemen of the given team
    defense_df = skaters_df[(skaters_df['team'] == team_abbrev) & 
                            (skaters_df['position'] == 'D') &
                            (skaters_df['situation'] == 'all')]
    
    # Get the top 6 defensemen
    defense_df = defense_df.sort_values(by="games_played", ascending=False).reset_index(drop=True)
    defense_df = defense_df.iloc[:6]

    defense_df['icetime/games_played'] = defense_df['icetime'] / defense_df['games_played']
    defense_df = defense_df.sort_values(by="icetime/games_played", ascending=False).reset_index(drop=True)

    top_three_d = defense_df.iloc[:3]
    bottom_three_d = defense_df.iloc[3:6]

    top_three_d_score = (top_three_d['gameScore'] / top_three_d['games_played']).sum()
    bottom_three_d_score = (bottom_three_d['gameScore'] / bottom_three_d['games_played']).sum()


    # Get dataframe of goalies of the given team
    goalie_df = goalies_df[(goalies_df['team'] == team_abbrev) &
                           (goalies_df['situation'] == 'all')]

    # Get the starting goalie of the given team    
    goalie_df = goalie_df.sort_values(by="games_played", ascending=False).reset_index(drop=True)
    starting_goalie = goalie_df.iloc[0]

    # Get the starting goalie's GSAx
    starting_goalie_gsax = starting_goalie['xGoals'] - starting_goalie['goals']


    # Get the team's even strength data
    es_df = teams_df[(teams_df['team'] == team_abbrev) & (teams_df['situation'] == '5on5')]

    # Get the team's even strength goals for and against
    team_gf = es_df.iloc[0]['goalsFor']
    team_ga = es_df.iloc[0]['goalsAgainst']

    # Get the team's special teams data
    pp_df = teams_df[(teams_df['team'] == team_abbrev) & (teams_df['situation'] == '5on4')]
    pk_df = teams_df[(teams_df['team'] == team_abbrev) & (teams_df['situation'] == '4on5')]

    # Get the team's even strength goals for and against
    team_pp_gf = pp_df.iloc[0]['goalsFor']
    team_pk_ga = pk_df.iloc[0]['goalsAgainst']

    # Adjust goals for seasons that wern't played with 82 games
    if season == '2012-2013':
        season_games = 48
    elif season == '2019-2020':
        season_games = 70
    elif season == '2020-2021':
        season_games = 56
    else:
        season_games = 82

    adjustment = 82 / season_games

    team_gf *= adjustment
    team_ga *= adjustment
    team_pp_gf *= adjustment
    team_pk_ga *= adjustment


    # Get the given team's playoff results
    result = constants.TEAM_RESULTS.get(season, {}).get(team_abbrev, 0)


    data_row = pd.Series({
        'Season': season,
        'Team': team_abbrev,
        'Result': result,
        'Top 6 F Game Score': top_six_f_score,
        'Bottom 6 F Game Score': bottom_six_f_score,
        'Top 3 D Game Score': top_three_d_score,
        'Bottom 3 D Game Score': bottom_three_d_score,
        'Starting Goalie GSAx': starting_goalie_gsax,
        'ES GF': team_gf,
        'ES GA': team_ga,
        'PP GF': team_pp_gf,
        'PK GA': team_pk_ga
    })


    return data_row



# ====================================================================================================
# SCRIPT TO GET RELEVANT DATA FOR TEAMS OVER MULTIPLE SEASONS
# ====================================================================================================

# Initialize relevant data dataframe
relevant_data = pd.DataFrame(columns=['Season', 'Team', 'Result',
                                      'Top 6 F Game Score', 'Bottom 6 F Game Score',
                                      'Top 3 D Game Score', 'Bottom 3 D Game Score',
                                      'Starting Goalie GSAx',
                                      'ES GF', 'ES GA', 'PP GF', 'PK GA'])


# Loop to iterate through the seasons and collect the relevant data for each team
for season in constants.SEASONS:
    for team_abbrev in constants.TEAM_ABBREVIATIONS:

        # Account for teams that have not been in the league for every relevant season 
        if team_abbrev == 'WPG' and season in (constants.ATL_SEASONS):
            team_abbrev = 'ATL'
        if team_abbrev == 'VGK' and season not in(constants.VGK_SEASONS):
            continue
        if team_abbrev == 'SEA' and season not in(constants.SEA_SEASONS):
            continue
        if team_abbrev == 'UTA' and season not in(constants.UTA_SEASONS):
            team_abbrev = 'ARI'

        data_row = get_relevant_data(season, team_abbrev)

        relevant_data = pd.concat([relevant_data, data_row.to_frame().T], ignore_index=True)

# Save relevant data as a CSV file
save_path = f'relevant_data/all_relevant_data.csv'
relevant_data.to_csv(save_path, index=False)