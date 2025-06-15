
# Imports
import pandas as pd
import constants


# ====================================================================================================
# SCRIPT TO IDENTIFY STAR PLAYERS
# ====================================================================================================

for season in constants.SEASONS:

    # Load the CSV file
    file_path = f'raw_data/{season}_skaters.csv'
    skaters_df = pd.read_csv(file_path)

    # Add a column for points per game
    skaters_df['pointsPerGame'] = skaters_df['I_F_points'] / skaters_df['games_played']

    # Create star columns and set to 0
    skaters_df['isSuperStarF'] = 0
    skaters_df['isStarF'] = 0
    skaters_df['isSuperStarD'] = 0
    skaters_df['isStarD'] = 0

    # Filter forwards and defensemen
    valid_forwards = skaters_df[
        (skaters_df['position'] != 'D') &
        (skaters_df['games_played'] >= 30) &
        (skaters_df['situation'] == 'all')
    ].copy()

    valid_defensemen = skaters_df[
        (skaters_df['position'] == 'D') &
        (skaters_df['games_played'] >= 30) &
        (skaters_df['situation'] == 'all')
    ].copy()

    # Identify superstar and star forwards
    valid_forwards['forwardRank'] = valid_forwards['pointsPerGame'].rank(method='min', ascending=False)
    valid_forwards['tmpSuperStarF'] = (valid_forwards['forwardRank'] <= 25).astype(int)
    valid_forwards['tmpStarF'] = ((valid_forwards['forwardRank'] > 25) & (valid_forwards['forwardRank'] <= 100)).astype(int)

    # Identify superstar and star defensemen
    valid_defensemen['defenseRank'] = valid_defensemen['pointsPerGame'].rank(method='min', ascending=False)
    valid_defensemen['tmpSuperStarD'] = (valid_defensemen['defenseRank'] <= 15).astype(int)
    valid_defensemen['tmpStarD'] = ((valid_defensemen['defenseRank'] > 15) & (valid_defensemen['defenseRank'] <= 50)).astype(int)

    # Merge forward stars with temporary columns
    skaters_df = skaters_df.merge(
        valid_forwards[['name', 'situation', 'tmpSuperStarF', 'tmpStarF']],
        on=['name', 'situation'],
        how='left'
    )

    # Merge defense stars with temporary columns
    skaters_df = skaters_df.merge(
        valid_defensemen[['name', 'situation', 'tmpSuperStarD', 'tmpStarD']],
        on=['name', 'situation'],
        how='left'
    )

    # Overwrite initial values where matches found
    skaters_df['isSuperStarF'] = skaters_df['tmpSuperStarF'].fillna(0).astype(int)
    skaters_df['isStarF'] = skaters_df['tmpStarF'].fillna(0).astype(int)
    skaters_df['isSuperStarD'] = skaters_df['tmpSuperStarD'].fillna(0).astype(int)
    skaters_df['isStarD'] = skaters_df['tmpStarD'].fillna(0).astype(int)

    # Delete temporary columns
    skaters_df.drop(columns=['tmpSuperStarF', 'tmpStarF', 'tmpSuperStarD', 'tmpStarD'], inplace=True)

    # Save data
    skaters_df.to_csv(file_path, index=False)

