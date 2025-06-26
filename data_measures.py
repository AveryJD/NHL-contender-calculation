
# Imports
import pandas as pd

# ====================================================================================================
# SCRIPT FOR GATHERING MEANS AND STANDARD DEVIATIONS OF CONTENDER'S RELEVANT DATA TO USE IN SCORING
# ====================================================================================================

# Load the scoring data
df = pd.read_csv('relevant_data/scoring_data.csv')

# Initialize list to store all averages
measures_data = []

# Loop for calculating averages for different minimum number of playoff round wins
loop_count = 0
for rounds_won in [0, 0, 1, 1, 2, 2, 3, 3, 4]:

    # Get filtered data of teams who won the minimum number of playoff wins
    if loop_count == 0:
        team_data_set = df[df['Result'] >= rounds_won]
        team_data_set_str = 'All Teams'
    elif loop_count == 1:
        team_data_set = df[df['Result'] == rounds_won]
        team_data_set_str = 'Teams that didn\'t win a round'
    elif loop_count % 2 == 0:
        team_data_set = df[df['Result'] >= rounds_won]
        team_data_set_str = f'Teams that won at least {rounds_won} round(s)'
    else:
        team_data_set = df[df['Result'] == rounds_won]
        team_data_set_str = f'Teams that won only {rounds_won} round(s)'

    # Create columns, calculating averages and standard deviations
    averages = {
        'Team Data Set': team_data_set_str,
        'Teams Used': team_data_set.shape[0],

        'AVG T3F Game Score': round(team_data_set['Top 3 F Game Score'].mean(), 2),
        'AVG TM3F Game Score': round(team_data_set['Top Middle 3 F Game Score'].mean(), 2),
        'AVG BM3F Game Score': round(team_data_set['Bottom Middle 3 F Game Score'].mean(), 2),
        'AVG B6F Game Score': round(team_data_set['Bottom 3 F Game Score'].mean(), 2),
        'AVG T2D Game Score': round(team_data_set['Top 2 D Game Score'].mean(), 2),
        'AVG M2D Game Score': round(team_data_set['Middle 2 D Game Score'].mean(), 2),
        'AVG B2D Game Score': round(team_data_set['Bottom 2 D Game Score'].mean(), 2),
        'AVG Starting Goalie GSAx/GP': round(team_data_set['Starting Goalie GSAx/GP'].mean(), 2),

        'STD T3F Game Score': round(team_data_set['Top 3 F Game Score'].std(), 2),
        'STD TM3F Game Score': round(team_data_set['Top Middle 3 F Game Score'].std(), 2),
        'STD BM3F Game Score': round(team_data_set['Bottom Middle 3 F Game Score'].std(), 2),
        'STD B6F Game Score': round(team_data_set['Bottom 3 F Game Score'].std(), 2),
        'STD T2D Game Score': round(team_data_set['Top 2 D Game Score'].std(), 2),
        'STD M2D Game Score': round(team_data_set['Middle 2 D Game Score'].std(), 2),
        'STD B2D Game Score': round(team_data_set['Bottom 2 D Game Score'].std(), 2),
        'STD Starting Goalie GSAx/GP': round(team_data_set['Starting Goalie GSAx/GP'].std(), 2),
    }

    measures_data.append(averages)

    loop_count += 1


# Save CSV file
AVG_df = pd.DataFrame(measures_data)
AVG_df.to_csv('data_relevant/measures_data.csv', index=False)