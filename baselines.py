
# Imports
import pandas as pd


# ====================================================================================================
# SCRIPT FOR GATHERING AVERAGES OF CONTENDER'S RELEVANT DATA TO USE AS BASELINES FOR SCORING
# ====================================================================================================

# Load the relevant data
df = pd.read_csv('relevant_data/all_relevant_data.csv')

# Initialize list to store all averages
all_averages = []

# Loop for calculating averages for different minimum number of playoff round wins
loop_count = 0
for rounds_won in [0, 0, 1, 2, 3, 4]:

    # Filter teams
    if loop_count == 0:
        playoff_winners = df[df['Result'] >= rounds_won]
        team_data_set = 'All Teams'
    elif loop_count == 1:
        playoff_winners = df[df['Result'] == rounds_won]
        team_data_set = 'Teams that didn\'t win a round'
    else:
        playoff_winners = df[df['Result'] >= rounds_won]
        team_data_set = f'Teams that won at least {rounds_won} round(s)'

    # Calculate averages
    averages = {
        'Team Data Set': team_data_set,
        'Teams Used': playoff_winners.shape[0],

        'Avg GF Rank': round(playoff_winners['5v5 GF Rank'].mean(), 2),
        'Avg GA Rank': round(playoff_winners['5v5 GA Rank'].mean(), 2),
        'Avg PP Rank': round(playoff_winners['PP Rank'].mean(), 2),
        'Avg PK Rank': round(playoff_winners['PK Rank'].mean(), 2),

        'Avg # Superstar Forwards': round(playoff_winners['# of Superstar Forwards'].mean(), 2),
        'Avg # Star Forwards': round(playoff_winners['# of Star Forwards'].mean(), 2),
        'Avg Top 6 F Game Score': round(playoff_winners['Top 6 F Game Score'].mean(), 2),
        'Avg Bottom 6 F Game Score': round(playoff_winners['Bottom 6 F Game Score'].mean(), 2),

        'Avg # Superstar Defensemen': round(playoff_winners['# of Superstar Defensemen'].mean(), 2),
        'Avg # Star Defensemen': round(playoff_winners['# of Star Defensemen'].mean(), 2),
        'Avg Top 3 D Game Score': round(playoff_winners['Top 3 D Game Score'].mean(), 2),
        'Avg Bottom 3 D Game Score': round(playoff_winners['Bottom 3 D Game Score'].mean(), 2),

        'Avg Starting Goalie GSAx': round(playoff_winners['Starting Goalie GSAx'].mean(), 2),
    }

    all_averages.append(averages)

    loop_count += 1


# Convert to DataFrame and save
avg_df = pd.DataFrame(all_averages)
avg_df.to_csv('relevant_data/baseline_averages.csv', index=False)