
# Imports
import pandas as pd


# ====================================================================================================
# SCRIPT FOR GATHERING AVERAGES AND STANDARD DEVIATIONS OF CONTENDER'S RELEVANT DATA TO USE IN SCORING
# ====================================================================================================

# Load the relevant data
df = pd.read_csv('data_relevant/all_relevant_data.csv')

# Initialize list to store all averages
baseline_data = []

# Loop for calculating averages for different minimum number of playoff round wins
loop_count = 0
for rounds_won in [0, 0, 1, 1, 2, 2, 3, 3, 4]:

    # Filter teams
    if loop_count == 0:
        playoff_winners = df[df['Result'] >= rounds_won]
        team_data_set = 'All Teams'
    elif loop_count == 1:
        playoff_winners = df[df['Result'] == rounds_won]
        team_data_set = 'Teams that didn\'t win a round'
    elif loop_count % 2 == 0:
        playoff_winners = df[df['Result'] >= rounds_won]
        team_data_set = f'Teams that won at least {rounds_won} round(s)'
    else:
        playoff_winners = df[df['Result'] == rounds_won]
        team_data_set = f'Teams that won only {rounds_won} round(s)'

    # Create columns, calculating averages and standard deviations
    averages = {
        'Team Data Set': team_data_set,
        'Teams Used': playoff_winners.shape[0],

        'AVG T6F Game Score': round(playoff_winners['Top 6 F Game Score'].mean(), 2),
        'AVG B6F Game Score': round(playoff_winners['Bottom 6 F Game Score'].mean(), 2),
        'AVG T3D Game Score': round(playoff_winners['Top 3 D Game Score'].mean(), 2),
        'AVG B3D Game Score': round(playoff_winners['Bottom 3 D Game Score'].mean(), 2),
        'AVG Starting Goalie GSAx': round(playoff_winners['Starting Goalie GSAx'].mean(), 2),

        'AVG ES GF': round(playoff_winners['ES GF'].mean(), 2),
        'AVG ES GA': round(playoff_winners['ES GA'].mean(), 2),
        'AVG PP GF': round(playoff_winners['PP GF'].mean(), 2),
        'AVG PK GA': round(playoff_winners['PK GA'].mean(), 2),


        'STD T6F Game Score': round(playoff_winners['Top 6 F Game Score'].std(), 2),
        'STD B6F Game Score': round(playoff_winners['Bottom 6 F Game Score'].std(), 2),
        'STD T3D Game Score': round(playoff_winners['Top 3 D Game Score'].std(), 2),
        'STD B3D Game Score': round(playoff_winners['Bottom 3 D Game Score'].std(), 2),
        'STD Starting Goalie GSAx': round(playoff_winners['Starting Goalie GSAx'].std(), 2),

        'STD ES GF': round(playoff_winners['ES GF'].std(), 2),
        'STD ES GA': round(playoff_winners['ES GA'].std(), 2),
        'STD PP GF': round(playoff_winners['PP GF'].std(), 2),
        'STD PK GA': round(playoff_winners['PK GA'].std(), 2),
    }

    baseline_data.append(averages)

    loop_count += 1


# Convert to DataFrame and save
AVG_df = pd.DataFrame(baseline_data)
AVG_df.to_csv('data_relevant/baseline_data.csv', index=False)