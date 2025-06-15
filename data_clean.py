
# Imports
import pandas as pd
import constants


# ====================================================================================================
# SCRIPT TO FIX INCONSISTENT TEAM ABBREVIATIONS IN RAW DATA FILES
# ====================================================================================================

for season in constants.SEASONS:
    for data_set in ['skaters', 'goalies', 'teams']:

        # Load the CSV file
        file_path = f'raw_data/{season}_{data_set}.csv'
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