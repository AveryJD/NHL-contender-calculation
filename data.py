
# Imports
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import random


# Constants
SEASONS = ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021', '2019-2020', '2018-2019']


# ====================================================================================================
# HELPER FUNCTIONS FOR GETTING DATA
# ====================================================================================================

def get_page(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return None
    

def random_delay():
    """"
    Random delay between requests to prevent server overload
    """
    delay = random.uniform(10, 20)
    print(f"Waiting {delay:.2f} seconds before next request")
    time.sleep(delay)


def fix_multi_team_players(df: pd.DataFrame):
    """
    Fix players who have multiple teams listed by prompting the user to choose the final team.
    """
    for idx, row in df.iterrows():
        team = row['Team']
        if ',' in str(team):
            player_name = row['Player'] if 'Player' in row else row.get('Name', f'Unknown (index {idx})')
            print(f"{player_name}'s teams are: {team}. Choose active team (abbreviation):")
            new_team = input().strip().upper()
            df.at[idx, 'Team'] = new_team
    return df



# ====================================================================================================
# FUNCTIONS FOR GETTING DATA
# ====================================================================================================

def get_forward_data(season: str):

    random_delay()

    url_season = season.replace("-", "")  # Remove hyphen for URL formatting

    # Scrape skater individual stats
    url = f'https://www.naturalstattrick.com/playerteams.php?fromseason={url_season}&thruseason={url_season}&stype=2&sit=all&score=all&stdoi=std&rate=n&team=ALL&pos=F&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL'
    page_content = get_page(url)

    std_soup = BeautifulSoup(page_content, 'html.parser')
    std_columns = [item.text for item in std_soup.find_all('th')]
    std_data = [e.text for e in std_soup.find_all('td')]
    
    std_table = []
    start = 0
    while start + len(std_columns) <= len(std_data):
        player = std_data[start:start + len(std_columns)]
        std_table.append(player)
        start += len(std_columns)

    df = pd.DataFrame(std_table, columns=std_columns)

    # Convert relevant columns to numeric
    df['TOI'] = pd.to_numeric(df['TOI'], errors='coerce')
    df['GP'] = pd.to_numeric(df['GP'], errors='coerce')
    df['Total Points'] = pd.to_numeric(df['Total Points'], errors='coerce')

    # Add TOI per game and points per game columns
    df['TOI/GP'] = df['TOI'] / df['GP']
    df['P/GP'] = df['Total Points'] / df['GP']

     # Filter out some unnecessary forwards
    df = df[df['GP'] >= 30]

    # Fix any forwards who played for multiple teams to only show the team they finished the season on
    df = fix_multi_team_players(df)

    # Save forward data as a CSV in the proper location
    save_path = f'data/{season}_forward_data.csv'
    df.to_csv(save_path, index=False)
    print(f"{season} forward data saved")



def get_defense_data(season: str):

    random_delay()

    url_season = season.replace("-", "")  # Remove hyphen for URL formatting

    # Scrape skater individual stats
    url = f'https://www.naturalstattrick.com/playerteams.php?fromseason={url_season}&thruseason={url_season}&stype=2&sit=all&score=all&stdoi=std&rate=n&team=ALL&pos=D&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL'
    page_content = get_page(url)

    std_soup = BeautifulSoup(page_content, 'html.parser')
    std_columns = [item.text for item in std_soup.find_all('th')]
    std_data = [e.text for e in std_soup.find_all('td')]
    
    std_table = []
    start = 0
    while start + len(std_columns) <= len(std_data):
        player = std_data[start:start + len(std_columns)]
        std_table.append(player)
        start += len(std_columns)

    df = pd.DataFrame(std_table, columns=std_columns)

    # Convert TOI, GP, and Total Points values into floats (not strings)
    df['TOI'] = pd.to_numeric(df['TOI'], errors='coerce')
    df['GP'] = pd.to_numeric(df['GP'], errors='coerce')
    df['Total Points'] = pd.to_numeric(df['Total Points'], errors='coerce')

    # Add TOI per game and points per game columns
    df['TOI/GP'] = df['TOI'] / df['GP']
    df['P/GP'] = df['Total Points'] / df['GP']

    # Filter out some unnecessary defensemen
    df = df[df['GP'] >= 30]

    # Fix any defensemen who played for multiple teams to only show the team they finished the season on
    df = fix_multi_team_players(df)

    # Save defense data as a CSV in the proper location
    save_path = f'data/{season}_defense_data.csv'
    df.to_csv(save_path, index=False)
    print(f"{season} defense data saved")


def get_goalie_data(season: str):

    random_delay()

    url_season = season.replace("-", "")  # Remove hyphen for URL formatting

    # Scrape skater individual stats
    url = f'https://www.naturalstattrick.com/playerteams.php?fromseason={url_season}&thruseason={url_season}&stype=2&sit=all&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL'
    page_content = get_page(url)

    std_soup = BeautifulSoup(page_content, 'html.parser')
    std_columns = [item.text for item in std_soup.find_all('th')]
    std_data = [e.text for e in std_soup.find_all('td')]
    
    std_table = []
    start = 0
    while start + len(std_columns) <= len(std_data):
        player = std_data[start:start + len(std_columns)]
        std_table.append(player)
        start += len(std_columns)

    df = pd.DataFrame(std_table, columns=std_columns)

    # Convert GP and SV% values into floats (not strings)
    df['GP'] = pd.to_numeric(df['GP'], errors='coerce')
    df['SV%'] = pd.to_numeric(df['SV%'], errors='coerce')

    # Filter out some unnecessary goalies
    df = df[df['GP'] >= 30]

    # Fix any goalies who played for multiple teams to only show the team they finished the season on
    df = fix_multi_team_players(df)

    # Save goalie data as a CSV in the proper location
    save_path = f'data/{season}_goalie_data.csv'
    df.to_csv(save_path, index=False)
    print(f"{season} goalie data saved")


def get_team_data(season: str, situation: str):

    random_delay()

    url_season = season.replace("-", "")  # Remove hyphen for URL formatting

    # Scrape NHL league stats
    url = f'https://www.naturalstattrick.com/teamtable.php?fromseason={url_season}&thruseason={url_season}&stype=2&sit={situation}&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td='
    page_content = get_page(url)

    std_soup = BeautifulSoup(page_content, 'html.parser')
    std_columns = [item.text for item in std_soup.find_all('th')]
    std_data = [e.text for e in std_soup.find_all('td')]
    
    std_table = []
    start = 0
    while start + len(std_columns) <= len(std_data):
        player = std_data[start:start + len(std_columns)]
        std_table.append(player)
        start += len(std_columns)

    df = pd.DataFrame(std_table, columns=std_columns)

    # Convert GF and GA values into floats (not strings)
    df['GF'] = pd.to_numeric(df['GF'], errors='coerce')
    df['GA'] = pd.to_numeric(df['GA'], errors='coerce')

    # Save team data as a CSV in the proper location
    save_path = f'data/{season}_team_{situation}_data.csv'
    df.to_csv(save_path, index=False)
    print(f"{season} team data saved")


# ====================================================================================================
# SCRIPT TO SCRAPE NHL PLAYER AND TEAM DATA
# ====================================================================================================

# Loop to iterate through the seasons and collect the data
for season in SEASONS:

    print(f'Gathering data for the {season} gathered.\n')

    get_forward_data(season)
    get_defense_data(season)
    get_goalie_data(season)
    get_team_data(season, '5v5')
    get_team_data(season, 'pp')
    get_team_data(season, 'pk')

    print(f'Data for the {season} gathered.\n')