
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

    # Get top 6 and bottom 6 forwards
    forward_df['icetime/games_played'] = forward_df['icetime'] / forward_df['games_played']
    forward_df = forward_df.sort_values(by="icetime/games_played", ascending=False).reset_index(drop=True)
    top_six_forwards = forward_df.iloc[:6]
    bottom_six_forwards = forward_df.iloc[6:12]

    # Get top 6 and bottom 6 average game scores
    top_six_game_score = (top_six_forwards['gameScore'] * top_six_forwards['games_played']).sum() / top_six_forwards['games_played'].sum()
    bottom_six_game_score = (bottom_six_forwards['gameScore'] * bottom_six_forwards['games_played']).sum() / bottom_six_forwards['games_played'].sum()

    # Get the number of superstar and star forwards
    super_star_f_count = len(forward_df[forward_df['gameScore'] >= 80])
    star_f_count = len(forward_df[(forward_df['gameScore'] >= 70) & (forward_df['gameScore'] < 80)])


    # Get dataframe of defensemen of the given team
    defense_df = skaters_df[(skaters_df['team'] == team_abbrev) & 
                            (skaters_df['position'] == 'D') &
                            (skaters_df['situation'] == 'all')]
    
    # Get the top 6 defensemen
    defense_df = defense_df.sort_values(by="games_played", ascending=False).reset_index(drop=True)
    defense_df = defense_df.iloc[:6]

    # Get top 3 and bottom 3 defensemen
    defense_df['icetime/games_played'] = defense_df['icetime'] / defense_df['games_played']
    defense_df = defense_df.sort_values(by="icetime/games_played", ascending=False).reset_index(drop=True)
    top_three_defensemen = defense_df.iloc[:3]
    bottom_three_defensemen = defense_df.iloc[3:6]

    # Get top 6 and bottom 6 average game scores
    top_three_game_score = (top_three_defensemen['gameScore'] * top_three_defensemen['games_played']).sum() / top_three_defensemen['games_played'].sum()
    bottom_three_game_score = (bottom_three_defensemen['gameScore'] * bottom_three_defensemen['games_played']).sum() / bottom_three_defensemen['games_played'].sum()

    # Get the number of superstar and star defensemen
    super_star_d_count = len(defense_df[defense_df['gameScore'] >= 70])
    star_d_count = len(defense_df[(defense_df['gameScore'] >= 50) & (defense_df['gameScore'] < 70)])


    # Get dataframe of goalies of the given team
    goalie_df = goalies_df[(goalies_df['team'] == team_abbrev) &
                           (goalies_df['situation'] == 'all')]

    # Get the starting goalie of the given team    
    goalie_df = goalie_df.sort_values(by="games_played", ascending=False).reset_index(drop=True)
    starting_goalie = goalie_df.iloc[0]

    # Get the starting goalie's GSAx
    starting_goalie_gsax = starting_goalie['xGoals'] - starting_goalie['goals']


    # Get dataframe of team even strength data
    es_df = teams_df[(teams_df['situation'] == '5on5')]

    # Get the given team's goals for ranking
    team_gf_rank = es_df.sort_values(by="goalsFor", ascending=False).reset_index(drop=True)
    team_gf_rank = team_gf_rank.index[team_gf_rank['team'] == team_abbrev][0] + 1

    # Get the given team's goals against ranking
    team_ga_rank = es_df.sort_values(by="goalsAgainst", ascending=True).reset_index(drop=True)
    team_ga_rank = team_ga_rank.index[team_ga_rank['team'] == team_abbrev][0] + 1

    # Get dataframe of team power play data
    pp_df = teams_df[(teams_df['situation'] == '5on4')]

    # Get the given team's power play ranking
    team_pp_rank = pp_df.sort_values(by="goalsFor", ascending=False).reset_index(drop=True)
    team_pp_rank = team_pp_rank.index[team_pp_rank['team'] == team_abbrev][0] + 1

    # Get dataframe of team penalty kill data
    pk_df = teams_df[(teams_df['situation'] == '4on5')]

    # Get the given team's penalty kill ranking
    team_pk_rank = pk_df.sort_values(by="goalsAgainst", ascending=True).reset_index(drop=True)
    team_pk_rank = team_pk_rank.index[team_pk_rank['team'] == team_abbrev][0] + 1

    # Get the given team's playoff results
    result = constants.TEAM_RESULTS.get(season, {}).get(team_abbrev, 0)


    # Final series containing the relevant data
    data_row = pd.Series({
        'Season': season,
        'Team': team_abbrev,
        'Result': result,
        '5v5 GF Rank': team_gf_rank,
        '5v5 GA Rank': team_ga_rank,
        'PP Rank': team_pp_rank,
        'PK Rank': team_pk_rank,
        '# of Superstar Forwards': super_star_f_count,
        '# of Star Forwards': star_f_count,
        'Top 6 F Game Score': top_six_game_score,
        'Bottom 6 F Game Score': bottom_six_game_score,
        '# of Superstar Defensemen': super_star_d_count,
        '# of Star Defensemen': star_d_count,
        'Top 3 D Game Score': top_three_game_score,
        'Bottom 3 D Game Score': bottom_three_game_score,
        'Starting Goalie GSAx': starting_goalie_gsax
    })

    return data_row



# ====================================================================================================
# SCRIPT TO GET RELEVANT DATA FOR TEAMS OVER MULTIPLE SEASONS
# ====================================================================================================

# Initialize relevant data dataframe
relevant_data = pd.DataFrame(columns=['Season', 'Team', 'Result', 
                                         '5v5 GF Rank', '5v5 GA Rank', 'PP Rank', 'PK Rank', 
                                         '# of Superstar Forwards', '# of Star Forwards', 'Top 6 F Game Score', 'Bottom 6 F Game Score',
                                         '# of Superstar Defensemen', '# of Star Defensemen', 'Top 3 D Game Score', 'Bottom 3 D Game Score',
                                         'Starting Goalie GSAx'])

# Loop to iterate through the seasons and collect the relevant data for each team
for season in constants.SEASONS:
    for team_abbrev in constants.TEAM_ABBREVIATIONS:

        # Account for newer teams
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