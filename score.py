
# Imports
import pandas as pd
import constants

# ====================================================================================================
# FUNCTIONS FOR CALCULATING A TEAM'S "CONTENDER SCORE"
# ====================================================================================================

def increase_score(score, value, thresholds, reverse=False):
    """
    ADD
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



def get_contender_score(team_abbrev, season, relevant_data):
    """
    ADD
    """

    # Filter to the exact row for that team and season
    team_data = relevant_data[
        (relevant_data['Team'] == team_abbrev) &
        (relevant_data['Season'] == season)
    ].iloc[0]

    # Extract variables
    top_six_game_score = team_data['Top 6 F Game Score']
    bottom_six_game_score = team_data['Bottom 6 F Game Score']
    super_star_f_count = team_data['# of Superstar Forwards']
    star_f_count = team_data['# of Star Forwards']

    top_three_game_score = team_data['Top 3 D Game Score']
    bottom_three_game_score = team_data['Bottom 3 D Game Score']
    super_star_d_count = team_data['# of Superstar Defensemen']
    star_d_count = team_data['# of Star Defensemen']

    starting_goalie_gsax = team_data['Starting Goalie GSAx']

    team_gf_rank = team_data['5v5 GF Rank']
    team_ga_rank = team_data['5v5 GA Rank']
    team_pp_rank = team_data['PP Rank']
    team_pk_rank = team_data['PK Rank']

    result = team_data['Result']


    # Score the team
    contender_score = 0

    contender_score = increase_score(contender_score, top_six_game_score, [70, 65, 60])
    contender_score = increase_score(contender_score, bottom_six_game_score, [35, 30, 25])
    contender_score = increase_score(contender_score, super_star_f_count, [2, 1, 999])
    contender_score = increase_score(contender_score, star_f_count, [2, 1, 999])

    contender_score = increase_score(contender_score, top_three_game_score, [55, 50, 45])
    contender_score = increase_score(contender_score, bottom_three_game_score, [30, 25, 20])
    contender_score = increase_score(contender_score, super_star_d_count, [2, 1, 999])
    contender_score = increase_score(contender_score, star_d_count, [2, 1, 999])

    contender_score = increase_score(contender_score, starting_goalie_gsax, [12, 8, 4])

    contender_score = increase_score(contender_score, team_gf_rank, [6, 11, 16], reverse=True)
    contender_score = increase_score(contender_score, team_ga_rank, [4, 9, 14], reverse=True)
    contender_score = increase_score(contender_score, team_pp_rank, [5, 10, 15], reverse=True)
    contender_score = increase_score(contender_score, team_pk_rank, [7, 12, 17], reverse=True)


    return contender_score, result



# ====================================================================================================
# SCRIPT TO CALCULATE CONTENDER SCORES FOR TEAMS OVER MULTIPLE SEASONS 
# ====================================================================================================

# Initialize contender scores dataframe
contender_scores = pd.DataFrame(columns=['Season', 'Team', 'Contender Score', 'Result'])

# Load relevant data
relevant_data = pd.read_csv(f'relevant_data/all_relevant_data.csv')

# Loop to iterate through the seasons and calculate each NHL team's contender score for that season
for season in constants.SEASONS:
    for team_abbrev in constants.TEAM_ABBREVIATIONS:

        # Account for newer teams
        if team_abbrev == 'VGK' and season not in(constants.VGK_SEASONS):
            continue
        if team_abbrev == 'SEA' and season not in(constants.SEA_SEASONS):
            continue
        if team_abbrev == 'UTA' and season not in(constants.UTA_SEASONS):
            team_abbrev = 'ARI'

        # Get team's contender score
        contender_score, result = get_contender_score(team_abbrev, season, relevant_data)

        # Make a row with the team's contender score information
        new_row = pd.DataFrame([{
            'Season': season,
            'Team': team_abbrev,
            'Contender Score': contender_score,
            'Result': result
        }])

        # Add the team's row to the main dataframe
        contender_scores = pd.concat([contender_scores, new_row], ignore_index=True)


# Save contender scores as a CSV file
contender_scores = contender_scores.sort_values(by="Contender Score", ascending=False).reset_index(drop=True)
save_path = f'scores/{season}_scores.csv'
contender_scores.to_csv(save_path, index=False)