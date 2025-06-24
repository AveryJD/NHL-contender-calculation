# score_calculation.py

import pandas as pd
import constants

SET_WEIGHTS = {
    'top_f':        8,
    'bottom_f':     3,
    'top_d':        5,
    'bottom_d':     5,
    'goalie_gsax':  3,
    'goals_for':    1,
    'goals_against':1,
    'power_play':   1,
    'penalty_kill': 1,
}


def increase_score(score: float, value: float, type: str, weights=SET_WEIGHTS, z_stats=constants.Z_STATS) -> float:
    factor = weights.get(type)

    mean = z_stats[type]['mean']
    std = z_stats[type]['std']

    # Flip direction for metrics where lower is better
    if type in ['goals_against', 'penalty_kill']:
        z = (mean - value) / std
    else:
        z = (value - mean) / std

    score += z * factor
    return score


def get_contender_score(team_abbrev, season, relevant_data, season_data, weights=SET_WEIGHTS):

    team_data = relevant_data[
        (relevant_data['Team'] == team_abbrev) &
        (relevant_data['Season'] == season)
    ].iloc[0]

    season_data = season_data[season_data['Team'] == team_abbrev].iloc[0]

    top_f_score = team_data['Top 6 F Game Score']
    bottom_f_score = team_data['Bottom 6 F Game Score']
    top_d_score = team_data['Top 3 D Game Score']
    bottom_d_score = team_data['Bottom 3 D Game Score']
    starting_goalie_gsax = team_data['Starting Goalie GSAx']

    team_gf_rank = team_data['ES GF']
    team_ga_rank = team_data['ES GA']
    team_pp_rank = team_data['PP GF']
    team_pk_rank = team_data['PK GA']

    standings_rank = season_data['Rk']

    result = team_data['Result']

    score = 0

    score = increase_score(score, top_f_score, 'top_f', weights)
    score = increase_score(score, bottom_f_score, 'bottom_f', weights)
    score = increase_score(score, top_d_score, 'top_d', weights)
    score = increase_score(score, bottom_d_score, 'bottom_d', weights)
    score = increase_score(score, starting_goalie_gsax, 'goalie_gsax', weights)
    
    score = increase_score(score, team_gf_rank, 'goals_for', weights)
    score = increase_score(score, team_ga_rank, 'goals_against', weights)
    score = increase_score(score, team_pp_rank, 'power_play', weights)
    score = increase_score(score, team_pk_rank, 'penalty_kill', weights)

    score = round(score, 2)

    return score, result, standings_rank



# ====================================================================================================
# SCORE CALCULATION LOOP FOR ALL SEASONS
# ====================================================================================================

relevant_data = pd.read_csv('data_relevant/all_relevant_data.csv')

for season in constants.SEASONS:
    rows = []

    standings_data = pd.read_csv(f'data_standings/{season}.csv')

    for team_abbrev in constants.TEAM_ABBREVIATIONS:
        if team_abbrev == 'WPG' and season in constants.ATL_SEASONS:
            team_abbrev = 'ATL'
        if team_abbrev == 'VGK' and season not in constants.VGK_SEASONS:
            continue
        if team_abbrev == 'SEA' and season not in constants.SEA_SEASONS:
            continue
        if team_abbrev == 'UTA' and season not in constants.UTA_SEASONS:
            team_abbrev = 'ARI'

        contender_score, result, standings_rank = get_contender_score(team_abbrev, season, relevant_data, standings_data, SET_WEIGHTS)

        if result != -1:
            rows.append({
                'Season': season,
                'Team': team_abbrev,
                'Contender Score': contender_score,
                'Standings Rank': standings_rank,
                'Result': result
            })

    df = pd.DataFrame(rows)
    df = df.sort_values(by="Contender Score", ascending=False).reset_index(drop=True)

    df.to_csv(f'scores/{season}_scores.csv', index=False)
