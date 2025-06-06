# Imports
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import random


# Constants
SEASONS = ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021', '2019-2020', '2018-2019']

TEAM_ABBREVIATIONS = [
    'ANA', 'BOS', 'BUF', 'CGY', 'CAR', 'CHI', 'COL', 'CBJ', 'DAL', 'DET', 'EDM',
    'FLA', 'L.A', 'MIN', 'MTL', 'NSH', 'N.J', 'NYI', 'NYR', 'OTT', 'PHI', 'PIT',
    'S.J', 'SEA', 'STL', 'T.B', 'TOR', 'VAN', 'UTA', 'VGK', 'WSH', 'WPG'
]

TEAM_NAMES = {
    'ANA': 'Anaheim Ducks',         'ARI': 'Arizona Coyotes',       'BOS': 'Boston Bruins',
    'BUF': 'Buffalo Sabres',        'CGY': 'Calgary Flames',        'CAR': 'Carolina Hurricanes',
    'CHI': 'Chicago Blackhawks',    'COL': 'Colorado Avalanche',    'CBJ': 'Columbus Blue Jackets',
    'DAL': 'Dallas Stars',          'DET': 'Detroit Red Wings',     'EDM': 'Edmonton Oilers',
    'FLA': 'Florida Panthers',      'L.A': 'Los Angeles Kings',     'MIN': 'Minnesota Wild',
    'MTL': 'Montreal Canadiens',    'NSH': 'Nashville Predators',   'N.J': 'New Jersey Devils',
    'NYI': 'New York Islanders',    'NYR': 'New York Rangers',      'OTT': 'Ottawa Senators',
    'PHI': 'Philadelphia Flyers',   'PIT': 'Pittsburgh Penguins',   'S.J': 'San Jose Sharks',
    'SEA': 'Seattle Kraken',        'STL': 'St Louis Blues',        'T.B': 'Tampa Bay Lightning',
    'TOR': 'Toronto Maple Leafs',   'VAN': 'Vancouver Canucks',     'UTA': 'Utah Hockey Club',
    'VGK': 'Vegas Golden Knights',  'WSH': 'Washington Capitals',   'WPG': 'Winnipeg Jets'
}


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
# FUNCTIONS FOR CALCULATING A TEAM'S "CONTENDER SCORE"
# ====================================================================================================

def get_contender_score(team_abbrev, forward_data, defense_data, goalie_data, ev_league_data, pp_league_data, pk_league_data):
    """
    Calculates a contender score for an NHL team based on various performance metrics.
    """

    team_name = TEAM_NAMES.get(team_abbrev)


    # Get the top 12 forwards by games played for the given team
    forward_data = forward_data[forward_data['Team'] == team_abbrev]
    forward_data = forward_data.sort_values(by="GP", ascending=False).reset_index(drop=True)
    forward_data = forward_data.iloc[:12]
    
    # Get the top 6 and bottom 6 by time on ice
    forward_data = forward_data.sort_values(by="TOI/GP", ascending=False).reset_index(drop=True)
    top_six_forwards = forward_data.iloc[:6]
    bottom_six_forwards = forward_data.iloc[6:12]

    # Get any super star forwards
    super_star_forwards = forward_data[
        (forward_data['GP'] >= 30) &
        (forward_data['TOI/GP'] >= 20) & 
        (forward_data['P/GP'] >= 1.1)
    ]

    # Get any star forwards
    star_forwards = forward_data[
        (forward_data['GP'] >= 30) &
        (forward_data['TOI/GP'] >= 15) & 
        (forward_data['P/GP'] >= 0.9)
    ]
    # Avoid double counting super star forwards
    star_forwards = star_forwards[~star_forwards['Player'].isin(super_star_forwards['Player'])]


    # Get the top 6 defensemen by games played for the given team
    defense_data = defense_data[defense_data['Team'] == team_abbrev]
    defense_data = defense_data.sort_values(by="GP", ascending=False).reset_index(drop=True)
    defense_data = defense_data.iloc[:6]
    
    # Get the top 3 and bottom 3 defensemen by time on ice
    defense_data = defense_data.sort_values(by="TOI/GP", ascending=False).reset_index(drop=True)
    top_three_defensemen = defense_data.iloc[:3]
    bottom_three_defensemen = defense_data.iloc[3:6]

    # Get any super star defensemen
    super_star_defensemen = defense_data[
        (defense_data['GP'] >= 30) &
        (defense_data['TOI/GP'] >= 23) & 
        (defense_data['P/GP'] >= 0.7)
    ]

    # Get any star defensemen
    star_defensemen = defense_data[
        (defense_data['GP'] >= 30) &
        (defense_data['TOI/GP'] >= 20) & 
        (defense_data['P/GP'] >= 0.5)
    ]
    # Avoid double counting super star defensemen
    star_defensemen = star_defensemen[~star_defensemen['Player'].isin(super_star_defensemen['Player'])]


    # Get the starting goalie
    goalie_data = goalie_data[goalie_data['Team'] == team_abbrev]
    goalie_data = goalie_data.sort_values(by="GP", ascending=False).reset_index(drop=True)
    starting_goalie = goalie_data.iloc[0]


    # Get the 5v5 goals for rank
    gf_league_data = ev_league_data.sort_values(by="GF", ascending=False).reset_index(drop=True)
    team_gf_rank = gf_league_data.index[gf_league_data['Team'] == team_name].tolist()
    team_gf_rank = team_gf_rank[0] + 1

    # Get the 5v5 goals against rank
    ga_league_data = ev_league_data.sort_values(by="GA", ascending=True).reset_index(drop=True)
    team_ga_rank = ga_league_data.index[ga_league_data['Team'] == team_name].tolist()
    team_ga_rank = team_ga_rank[0] + 1

    # Get the power play rank
    pp_league_data = pp_league_data.sort_values(by="GF", ascending=False).reset_index(drop=True)
    team_pp_rank = pp_league_data.index[pp_league_data['Team'] == team_name].tolist()
    team_pp_rank = team_pp_rank[0] + 1

    # Get the penalty kill rank
    pk_league_data = pk_league_data.sort_values(by="GA", ascending=True).reset_index(drop=True)
    team_pk_rank = pk_league_data.index[pk_league_data['Team'] == team_name].tolist()
    team_pk_rank = team_pk_rank[0] + 1


    # Initialize contender score
    contender_score = 0


    # Score the top six forwards


    # Score the bottom six forwards


    # Score any super star forwards
    super_star_forwards_count = super_star_forwards.shape[0]
    contender_score += 10 * super_star_forwards_count

    # Score any star forwards
    star_forwards_count = star_forwards.shape[0]
    contender_score += 5 * star_forwards_count



    # Score the top three defensemen


    # Score the bottom three defensemen


    # Score any super star defensemen
    super_star_defensemen_count = super_star_defensemen.shape[0]
    contender_score += 10 * super_star_defensemen_count

    # Score any star defensemen
    star_defensemen_count = star_defensemen.shape[0]
    contender_score += 5 * star_defensemen_count

 
    # Score team starting goalie
    stating_goalie_svp = starting_goalie['SV%']
    if stating_goalie_svp >= 0.916:
        contender_score += 15
    elif stating_goalie_svp >= 0.908:
        contender_score += 10
    elif stating_goalie_svp >= 0.900:
        contender_score += 5


    # Score team 5v5 goals for
    if team_gf_rank <= 5:
        contender_score += 15
    elif team_gf_rank <= 10:
        contender_score += 10
    elif team_gf_rank <= 15:
        contender_score += 5

    # Score team 5v5 goals against
    if team_ga_rank <= 5:
        contender_score += 15
    elif team_ga_rank <= 10:
        contender_score += 10
    elif team_ga_rank <= 15:
        contender_score += 5

    # Score team power play
    if team_pp_rank <= 5:
        contender_score += 15
    elif team_pp_rank <= 10:
        contender_score += 10
    elif team_pp_rank <= 15:
        contender_score += 5

    # Score team penalty kill
    if team_pk_rank <= 5:
        contender_score += 15
    elif team_pk_rank <= 10:
        contender_score += 10
    elif team_pk_rank <= 15:
        contender_score += 5


    #print(super_star_forwards)
    #print(star_forwards)
    #print(top_six_forwards)
    #print(bottom_six_forwards)

    #print(super_star_defensemen)
    #print(star_defensemen)
    #print(top_three_defensemen)
    #print(bottom_three_defensemen)

    #print(starting_goalie)

    #print(f'Team goals for rank: {team_gf_rank}')
    #print(f'Team goals against rank: {team_ga_rank}')
    #print(f'Team PP rank: {team_pp_rank}')
    #print(f'Team PK rank: {team_pk_rank}')


    return contender_score


# ====================================================================================================
# SCRIPT TO SCRAPE NHL PLAYER PROFILES AND STATS DATA
# ====================================================================================================
"
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


# Loop to iterate through the seasons and calculate each NHL team's contender score for that season
for season in SEASONS:

    contender_scores = pd.DataFrame(columns=['Team', 'Score'])

    print(f'Getting {season} data')

    forward_data = pd.read_csv(f'data/{season}_forward_data.csv')
    defense_data = pd.read_csv(f'data/{season}_defense_data.csv')
    goalie_data = pd.read_csv(f'data/{season}_goalie_data.csv')

    ev_league_data =  pd.read_csv(f'data/{season}_team_5v5_data.csv')
    pp_league_data =  pd.read_csv(f'data/{season}_team_pp_data.csv')
    pk_league_data =  pd.read_csv(f'data/{season}_team_pk_data.csv')

    for team_abbrev in TEAM_ABBREVIATIONS:
        if season != '2024-2025' and team_abbrev == 'UTA':
            team_abbrev = 'ARI'

        print('\n\n\n')
        print(f'Calculating contender score for {team_abbrev}')

        team_contender_score = get_contender_score(team_abbrev, forward_data, defense_data, goalie_data, ev_league_data, pp_league_data, pk_league_data)

        print(f'{team_abbrev} contender score for {season} is {team_contender_score}')

        contender_scores = pd.concat([
            contender_scores,
            pd.DataFrame({'Team': [team_abbrev], 'Score': [team_contender_score]})
        ], ignore_index=True)


    # Save the DataFrame to a CSV file in the scores folder
    output_path = f'scores/{season}_scores.csv'
    contender_scores.to_csv(output_path, index=False)

    print(f'Saved scores for {season} to {output_path}')

