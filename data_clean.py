
# Imports
import pandas as pd
import constants


# ====================================================================================================
# SCRIPT TO FIX INCONSISTENT TEAM ABBREVIATIONS IN RAW DATA FILES
# ====================================================================================================

for season in constants.SEASONS:
    for data_set in ['skaters', 'goalies', 'teams']:

        # Load the CSV file
        file_path = f'data_raw/{season}_{data_set}.csv'
        df = pd.read_csv(file_path)

        # Define replacements
        replacements = {
            'L.A': 'LAK',
            'N.J': 'NJD',
            'S.J': 'SJS',
            'T.B': 'TBL'
        }

        # Replace values across the entire DataFrame
        df = df.replace(replacements, regex=False)

        # Save data
        df.to_csv(file_path, index=False)



# ====================================================================================================
# SCRIPT TO CHANGE TEAM NAMES TO THEIR ABREVIATIONS IN STANDINGS FILES
# ====================================================================================================


for season in constants.SEASONS:
    file_path = f'data_standings/{season}.csv'
    
    # Read CSV and rename the 2nd column to 'Team'
    df = pd.read_csv(file_path, header=0)
    if df.columns[1] != 'Team':
        df.columns.values[1] = 'Team'

    # Replace full names with abbreviations
    df['Team'] = df['Team'].map(constants.TEAM_NAME_MAP).fillna(df['Team'])  

    # Save updated CSV
    df.to_csv(file_path, index=False)

