
# Imports
import pandas as pd


# Constants
SEASONS = ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021', '2019-2020', '2018-2019']

TEAM_ABBREVIATIONS = [
    'ANA', 'BOS', 'BUF', 'CGY', 'CAR', 'CHI', 'COL', 'CBJ', 'DAL', 'DET', 'EDM',
    'FLA', 'LAK', 'MIN', 'MTL', 'NSH', 'NJD', 'NYI', 'NYR', 'OTT', 'PHI', 'PIT',
    'SJS', 'SEA', 'STL', 'TBL', 'TOR', 'VAN', 'UTA', 'VGK', 'WSH', 'WPG'
]


# ====================================================================================================
# FUNCTIONS FOR CALCULATING A TEAM'S "CONTENDER SCORE"
# ====================================================================================================

def increase_score(score, value, thresholds, reverse=False):
    """
    Returns a score based on the first matching threshold.
    
    :param score: Current score
    :param value: Numeric value to score
    :param thresholds: list of scoring thresholds (high to low)
    :param reverse: whether to treat thresholds as "less than or equal to"
    :return: updated score
    """
    if reverse:
        if value <= thresholds[0]:
            score += 15
        elif value <= thresholds[1]:
            score += 10
        elif value <= thresholds[2]:
            score += 5
    else:
        if value >= thresholds[0]:
            score += 15
        elif value >= thresholds[1]:
            score += 10
        elif value >= thresholds[2]:
            score += 5

    return score



def get_contender_score(team_abbrev, forward_data, defense_data, goalie_data, ev_league_data, pp_league_data, pk_league_data, season):
    """
    Calculates a contender score for an NHL team based on various performance metrics.
    Returns a pandas Series of relevant data.
    """

    # Get top 12 forwards
    forward_data = forward_data[forward_data['team'] == team_abbrev].copy()
    forward_data = forward_data.sort_values(by="games_played", ascending=False).reset_index(drop=True)
    forward_data = forward_data.iloc[:12]

    # Get top 6 and bottom 6 forwards
    forward_data['icetime/games_played'] = forward_data['icetime'] / forward_data['games_played']
    forward_data = forward_data.sort_values(by="icetime/games_played", ascending=False).reset_index(drop=True)
    top_six_forwards = forward_data.iloc[:6]
    bottom_six_forwards = forward_data.iloc[6:12]

    # Get top 6 and bottom 6 game scores for scoring
    top_six_game_score = (top_six_forwards['gameScore'] * top_six_forwards['games_played']).sum() / top_six_forwards['games_played'].sum()
    bottom_six_game_score = (bottom_six_forwards['gameScore'] * bottom_six_forwards['games_played']).sum() / bottom_six_forwards['games_played'].sum()

    # ADD Get the number of superstar and star forwards
    super_star_f_count = 0
    star_f_count = 0


    # Get top 6 defensemen
    defense_data = defense_data[defense_data['team'] == team_abbrev].copy()
    defense_data = defense_data.sort_values(by="games_played", ascending=False).reset_index(drop=True)
    defense_data = defense_data.iloc[:6]

    # Get top 3 and bottom 3 defensemen
    defense_data['icetime/games_played'] = defense_data['icetime'] / defense_data['games_played']
    defense_data = defense_data.sort_values(by="icetime/games_played", ascending=False).reset_index(drop=True)
    top_three_defensemen = defense_data.iloc[:3]
    bottom_three_defensemen = defense_data.iloc[3:6]

    # Get top 6 and bottom 6 game scores for scoring
    top_three_game_score = (top_three_defensemen['gameScore'] * top_three_defensemen['games_played']).sum() / top_three_defensemen['games_played'].sum()
    bottom_three_game_score = (bottom_three_defensemen['gameScore'] * bottom_three_defensemen['games_played']).sum() / bottom_three_defensemen['games_played'].sum()

    # ADD Get the number of superstar and star defensemen
    super_star_d_count = 0
    star_d_count = 0


    # Get starting goalie
    goalie_data = goalie_data[goalie_data['team'] == team_abbrev].copy()
    goalie_data = goalie_data.sort_values(by="games_played", ascending=False).reset_index(drop=True)
    starting_goalie = goalie_data.iloc[0]

    # Get starting goalie GSAx for scoring
    starting_goalie_gsax = starting_goalie['xGoals'] - starting_goalie['goals']


    # Get team rankings for scoring
    team_gf_rank = ev_league_data.sort_values(by="goalsFor", ascending=False).reset_index(drop=True)
    team_gf_rank = team_gf_rank.index[team_gf_rank['team'] == team_abbrev][0] + 1

    team_ga_rank = ev_league_data.sort_values(by="goalsAgainst", ascending=True).reset_index(drop=True)
    team_ga_rank = team_ga_rank.index[team_ga_rank['team'] == team_abbrev][0] + 1

    team_pp_rank = pp_league_data.sort_values(by="goalsFor", ascending=False).reset_index(drop=True)
    team_pp_rank = team_pp_rank.index[team_pp_rank['team'] == team_abbrev][0] + 1

    team_pk_rank = pk_league_data.sort_values(by="goalsAgainst", ascending=True).reset_index(drop=True)
    team_pk_rank = team_pk_rank.index[team_pk_rank['team'] == team_abbrev][0] + 1


    # Score the team
    contender_score = 0

    contender_score = increase_score(contender_score, top_six_game_score, [65, 60, 55])
    contender_score = increase_score(contender_score, bottom_six_game_score, [30, 25, 20])
    contender_score = increase_score(contender_score, super_star_f_count, [2, 1, 999])
    contender_score = increase_score(contender_score, star_f_count, [2, 1, 1])

    contender_score = increase_score(contender_score, top_three_game_score, [50, 45, 40])
    contender_score = increase_score(contender_score, bottom_three_game_score, [25, 20, 25])
    contender_score = increase_score(contender_score, super_star_d_count, [2, 1, 999])
    contender_score = increase_score(contender_score, star_d_count, [2, 1, 999])

    contender_score = increase_score(contender_score, starting_goalie_gsax, [15, 10, 5])

    contender_score = increase_score(contender_score, team_gf_rank, [6, 11, 16], reverse=True)
    contender_score = increase_score(contender_score, team_ga_rank, [4, 9, 14], reverse=True)
    contender_score = increase_score(contender_score, team_pp_rank, [5, 10, 15], reverse=True)
    contender_score = increase_score(contender_score, team_pk_rank, [5, 10, 15], reverse=True)


    # Final Series
    score_row = pd.Series({
        'Season': season,
        'Team': team_abbrev,
        'Contender Score': contender_score,
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

    return score_row



# ====================================================================================================
# SCRIPT TO CALCULATE NHL TEAM CONTENDER SCORES
# ====================================================================================================

contender_scores = pd.DataFrame(columns=['Season', 'Team', 'Contender Score', 
                                         '5v5 GF Rank', '5v5 GA Rank', 'PP Rank', 'PK Rank', 
                                         '# of Superstar Forwards', '# of Star Forwards', 'Top 6 F Game Score', 'Bottom 6 F Game Score',
                                         '# of Superstar Defensemen', '# of Star Defensemen', 'Top 3 D Game Score', 'Bottom 3 D Game Score',
                                         'Starting Goalie GSAx'])

# Loop to iterate through the seasons and calculate each NHL team's contender score for that season
for season in SEASONS:
    print(f'Getting {season} data')


    contender_scores = pd.DataFrame()

    forward_data = pd.read_csv(f'cleaned_data/{season}_forwards.csv')
    defense_data = pd.read_csv(f'cleaned_data/{season}_defense.csv')
    goalie_data = pd.read_csv(f'cleaned_data/{season}_goalies.csv')
    ev_league_data = pd.read_csv(f'cleaned_data/{season}_es.csv')
    pp_league_data = pd.read_csv(f'cleaned_data/{season}_pp.csv')
    pk_league_data = pd.read_csv(f'cleaned_data/{season}_pk.csv')

    for team_abbrev in TEAM_ABBREVIATIONS:
        if season != '2024-2025' and team_abbrev == 'UTA':
            team_abbrev = 'ARI'

        print(f'Calculating contender score for {team_abbrev}.')

        contender_score_row = get_contender_score(team_abbrev, forward_data, defense_data, goalie_data,
                                                   ev_league_data, pp_league_data, pk_league_data, season)

        print(f"{team_abbrev} contender score for {season} is {contender_score_row['Contender Score']}.\n")

        contender_scores = pd.concat([
            contender_scores,
            contender_score_row.to_frame().T
        ], ignore_index=True)

    # Save after each season
    contender_scores = contender_scores.sort_values(by="Contender Score", ascending=False).reset_index(drop=True)
    save_path = f'scores/{season}_scores.csv'
    contender_scores.to_csv(save_path, index=False)

    print(f'Saved scores for {season}.')
