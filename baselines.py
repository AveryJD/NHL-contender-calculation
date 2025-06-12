
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
for rounds_won in [1, 2, 3, 4]:

    # Filter teams
    playoff_winners = df[df['Result'] >= rounds_won]

    # Calculate averages
    averages = {
        'Rounds Won': rounds_won,
        'Teams Used': playoff_winners.shape[0],

        'Avg GF Rank': playoff_winners['5v5 GF Rank'].mean(),
        'Avg GA Rank': playoff_winners['5v5 GA Rank'].mean(),
        'Avg PP Rank': playoff_winners['PP Rank'].mean(),
        'Avg PK Rank': playoff_winners['PK Rank'].mean(),

        'Avg # Superstar Forwards': playoff_winners['# of Superstar Forwards'].mean(),
        'Avg # Star Forwards': playoff_winners['# of Star Forwards'].mean(),
        'Avg Top 6 F Game Score': playoff_winners['Top 6 F Game Score'].mean(),
        'Avg Bottom 6 F Game Score': playoff_winners['Bottom 6 F Game Score'].mean(),

        'Avg # Superstar Defensemen': playoff_winners['# of Superstar Defensemen'].mean(),
        'Avg # Star Defensemen': playoff_winners['# of Star Defensemen'].mean(),
        'Avg Top 3 D Game Score': playoff_winners['Top 3 D Game Score'].mean(),
        'Avg Bottom 3 D Game Score': playoff_winners['Bottom 3 D Game Score'].mean(),

        'Avg Starting Goalie GSAx': playoff_winners['Starting Goalie GSAx'].mean(),
    }

    all_averages.append(averages)


# Convert to DataFrame and save
avg_df = pd.DataFrame(all_averages)
avg_df.to_csv('relevant_data/baseline_averages.csv', index=False)