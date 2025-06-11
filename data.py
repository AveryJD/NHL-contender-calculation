
# Imports
import pandas as pd


# Constants
SEASONS = ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021', '2019-2020', '2018-2019']



# ====================================================================================================
# FUNCTIONS FOR CLEANING DATA
# ====================================================================================================

def clean_skater_data(season: str):

    df = pd.read_csv(f'raw_data/{season}_skaters.csv')

    # Account for the shortened COVID season (56 games) when filtering players
    if season == '2020-2021':
        min_gp = 20
    else:
        min_gp = 30

    # Filter forward dataframe
    forward_df = df[
        (df['position'] != 'D') &
        (df['situation'] == 'all') &
        (df['games_played'] >= min_gp)
    ]

    # Filter defense dataframe
    defense_df = df[
        (df['position'] == 'D') &
        (df['situation'] == 'all') &
        (df['games_played'] >= min_gp)
    ]

    # Save forward dataframe as a CSV
    save_path = f'cleaned_data/{season}_forwards.csv'
    forward_df.to_csv(save_path, index=False)
    print(f"{season} forward data saved")

    # Save defense dataframe as a CSV
    save_path = f'cleaned_data/{season}_defense.csv'
    defense_df.to_csv(save_path, index=False)
    print(f"{season} defense data saved")


def clean_goalie_data(season: str):

    df = pd.read_csv(f'raw_data/{season}_goalies.csv')

    # Account for the shortened COVID season (56 games) when filtering players
    if season == '2020-2021':
        min_gp = 20
    else:
        min_gp = 30

    # Filter goalie dataframe
    goalie_df = df[
        (df['situation'] == 'all') &
        (df['games_played'] >= min_gp)
    ]

    # Save goalie dataframe as a CSV
    save_path = f'cleaned_data/{season}_goalies.csv'
    goalie_df.to_csv(save_path, index=False)
    print(f"{season} goalie data saved")


def clean_team_data(season: str):

    df = pd.read_csv(f'raw_data/{season}_teams.csv')

    # Filter even strength dataframe
    es_df = df[
        (df['situation'] == '5on5')
    ]

    # Filter power play dataframe
    pp_df = df[
        (df['situation'] == '5on4')
    ]

    # Filter penalty kill dataframe
    pk_df = df[
        (df['situation'] == '4on5')
    ]


    # Save even strength dataframe as a CSV
    save_path = f'cleaned_data/{season}_es.csv'
    es_df.to_csv(save_path, index=False)
    print(f"{season} even strength data saved")

    # Save power play dataframe as a CSV
    save_path = f'cleaned_data/{season}_pp.csv'
    pp_df.to_csv(save_path, index=False)
    print(f"{season} power play data saved")

    # Save penalty kill dataframe as a CSV
    save_path = f'cleaned_data/{season}_pk.csv'
    pk_df.to_csv(save_path, index=False)
    print(f"{season} penalty kill data saved")


# ====================================================================================================
# SCRIPT TO CLEANUP NHL PLAYER AND TEAM DATA
# ====================================================================================================

# Loop to iterate through the seasons and collect the data
for season in SEASONS:

    print(f'Gathering data for the {season} season.\n')

    clean_skater_data(season)
    clean_goalie_data(season)
    clean_team_data(season)

    print(f'Data for the {season} season gathered.\n')

