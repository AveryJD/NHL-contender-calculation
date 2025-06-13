
# Imports
import pandas as pd


# ====================================================================================================
# SCRIPT FOR GATHERING AVERAGES OF CONTENDER'S RELEVANT DATA TO USE AS BASELINES FOR SCORING
# ====================================================================================================

# Load the relevant data
df = pd.read_csv('relevant_data/all_relevant_data.csv')

# Initialize list to store all averages
baseline_data = []

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

    # Create columns, calculating averages and standard deviations
    averages = {
        'Team Data Set': team_data_set,
        'Teams Used': playoff_winners.shape[0],

        'AVG # Superstar Forwards': round(playoff_winners['# of Superstar Forwards'].mean(), 2),
        'AVG # Star Forwards': round(playoff_winners['# of Star Forwards'].mean(), 2),
        'AVG Top 6 F Game Score': round(playoff_winners['Top 6 F Game Score'].mean(), 2),
        'AVG Bottom 6 F Game Score': round(playoff_winners['Bottom 6 F Game Score'].mean(), 2),

        'AVG # Superstar Defensemen': round(playoff_winners['# of Superstar Defensemen'].mean(), 2),
        'AVG # Star Defensemen': round(playoff_winners['# of Star Defensemen'].mean(), 2),
        'AVG Top 3 D Game Score': round(playoff_winners['Top 3 D Game Score'].mean(), 2),
        'AVG Bottom 3 D Game Score': round(playoff_winners['Bottom 3 D Game Score'].mean(), 2),

        'AVG Starting Goalie GSAx': round(playoff_winners['Starting Goalie GSAx'].mean(), 2),

        'AVG GF Rank': round(playoff_winners['5v5 GF Rank'].mean(), 2),
        'AVG GA Rank': round(playoff_winners['5v5 GA Rank'].mean(), 2),
        'AVG PP Rank': round(playoff_winners['PP Rank'].mean(), 2),
        'AVG PK Rank': round(playoff_winners['PK Rank'].mean(), 2),


        'SD # Superstar Forwards': round(playoff_winners['# of Superstar Forwards'].std(), 2),
        'SD # Star Forwards': round(playoff_winners['# of Star Forwards'].std(), 2),
        'SD Top 6 F Game Score': round(playoff_winners['Top 6 F Game Score'].std(), 2),
        'SD Bottom 6 F Game Score': round(playoff_winners['Bottom 6 F Game Score'].std(), 2),

        'SD # Superstar Defensemen': round(playoff_winners['# of Superstar Defensemen'].std(), 2),
        'SD # Star Defensemen': round(playoff_winners['# of Star Defensemen'].std(), 2),
        'SD Top 3 D Game Score': round(playoff_winners['Top 3 D Game Score'].std(), 2),
        'SD Bottom 3 D Game Score': round(playoff_winners['Bottom 3 D Game Score'].std(), 2),

        'SD Starting Goalie GSAx': round(playoff_winners['Starting Goalie GSAx'].std(), 2),

        'SD GF Rank': round(playoff_winners['5v5 GF Rank'].std(), 2),
        'SD GA Rank': round(playoff_winners['5v5 GA Rank'].std(), 2),
        'SD PP Rank': round(playoff_winners['PP Rank'].std(), 2),
        'SD PK Rank': round(playoff_winners['PK Rank'].std(), 2),
    }

    baseline_data.append(averages)

    loop_count += 1


# Convert to DataFrame and save
AVG_df = pd.DataFrame(baseline_data)
AVG_df.to_csv('relevant_data/baseline_data.csv', index=False)