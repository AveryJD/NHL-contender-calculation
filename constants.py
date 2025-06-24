# ====================================================================================================
# CONSTANTS USED THROUOUGHT CODE
# ====================================================================================================

SEASONS = [
    '2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021',
    '2019-2020', '2018-2019', '2017-2018', '2016-2017', '2015-2016',
    '2014-2015', '2013-2014', '2012-2013', '2011-2012', '2010-2011',
    '2009-2010', '2008-2009'
]


TEAM_ABBREVIATIONS = [
    'ANA', 'BOS', 'BUF', 'CGY', 'CAR', 'CHI', 'COL', 'CBJ', 'DAL', 'DET', 'EDM',
    'FLA', 'LAK', 'MIN', 'MTL', 'NSH', 'NJD', 'NYI', 'NYR', 'OTT', 'PHI', 'PIT', 
    'SJS', 'SEA', 'STL', 'TBL', 'TOR', 'VAN', 'UTA', 'VGK', 'WSH', 'WPG'
]

TEAM_NAME_MAP = {
    'Anaheim Ducks': 'ANA',
    'Boston Bruins': 'BOS',
    'Buffalo Sabres': 'BUF',
    'Calgary Flames': 'CGY',
    'Carolina Hurricanes': 'CAR',
    'Chicago Blackhawks': 'CHI',
    'Colorado Avalanche': 'COL',
    'Columbus Blue Jackets': 'CBJ',
    'Dallas Stars': 'DAL',
    'Detroit Red Wings': 'DET',
    'Edmonton Oilers': 'EDM',
    'Florida Panthers': 'FLA',
    'Los Angeles Kings': 'LAK',
    'Minnesota Wild': 'MIN',
    'Montreal Canadiens': 'MTL',
    'Nashville Predators': 'NSH',
    'New Jersey Devils': 'NJD',
    'New York Islanders': 'NYI',
    'New York Rangers': 'NYR',
    'Ottawa Senators': 'OTT',
    'Philadelphia Flyers': 'PHI',
    'Pittsburgh Penguins': 'PIT',
    'San Jose Sharks': 'SJS',
    'Seattle Kraken': 'SEA',
    'St. Louis Blues': 'STL',
    'Tampa Bay Lightning': 'TBL',
    'Toronto Maple Leafs': 'TOR',
    'Vancouver Canucks': 'VAN',
    'Utah Hockey Club': 'UTA',
    'Vegas Golden Knights': 'VGK',
    'Washington Capitals': 'WSH',
    'Winnipeg Jets': 'WPG',
    'Atlanta Thrashers': 'ATL',
    'Phoenix Coyotes': 'ARI',
    'Arizona Coyotes': 'ARI',
}


ATL_SEASONS = ['2010-2011', '2009-2010', '2008-2009']

VGK_SEASONS = ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021', '2019-2020', '2018-2019', '2017-2018']

SEA_SEASONS = ['2024-2025', '2023-2024', '2022-2023', '2021-2022']

UTA_SEASONS = ['2024-2025']

Z_STATS = {
    'top_f': {
        'mean': 4.96,
        'std': 0.84
    },
    'bottom_f': {
        'mean': 2.26,
        'std': 0.60
    },
    'top_d': {
        'mean': 1.79,
        'std': 0.47
    },
    'bottom_d': {
        'mean': 0.99,
        'std': 0.36
    },
    'goalie_gsax': {
        'mean': 8.51,
        'std': 12.64
    },
    'goals_for': {
        'mean': 165.35,
        'std': 19.36
    },
    'goals_against': {
        'mean': 141.28,
        'std': 16.08
    },
    'power_play': {
        'mean': 49.25,
        'std': 10.57
    },
    'penalty_kill': {
        'mean': 40.99,
        'std': 7.91
    }
}




TEAM_RESULTS = {
    '2024-2025': {
        'FLA': 4, 'EDM': 3, 'DAL': 2, 'CAR': 2,
        'WPG': 1, 'VGK': 1, 'TOR': 1, 'WSH': 1,
        'LAK': 0, 'MIN': 0, 'DAL': 0, 'STL': 0,
        'NJD': 0, 'MTL': 0, 'TBL': 0, 'OTT': 0
    },
    '2023-2024': {
        'FLA': 4, 'EDM': 3, 'DAL': 2, 'NYR': 2,
        'COL': 1, 'VAN': 1, 'BOS': 1, 'CAR': 1,
        'LAK': 0, 'VGK': 0, 'NSH': 0, 'WIN': 0,
        'TOR': 0, 'NYI': 0, 'WSH': 0, 'TBL': 0
    },
    '2022-2023': {
        'VGK': 4, 'FLA': 3, 'DAL': 2, 'CAR': 2,
        'SEA': 1, 'EDM': 1, 'TOR': 1, 'NJD': 1,
        'LAK': 0, 'WIN': 0, 'MIN': 0, 'COL': 0,
        'NYR': 0, 'NYI': 0, 'TBL': 0, 'BOS': 0
    },
    '2021-2022': {
        'COL': 4, 'TBL': 3, 'EDM': 2, 'NYR': 2,
        'STL': 1, 'CGY': 1, 'FLA': 1, 'CAR': 1,
        'DAL': 0, 'NSH': 0, 'LAK': 0, 'MIN': 0,
        'WSH': 0, 'PIT': 0, 'TOR': 0, 'BOS': 0
    },
    '2020-2021': {
        'TBL': 4, 'MTL': 3, 'VGK': 2, 'NYI': 2,
        'WPG': 1, 'COL': 1, 'BOS': 1, 'CAR': 1,
        'EDM': 0, 'NSH': 0, 'MIN': 0, 'STL': 0,
        'WSH': 0, 'PIT': 0, 'TOR': 0, 'FLA': 0
    },
    '2019-2020': {
        'TBL': 4, 'DAL': 3, 'VGK': 2, 'NYI': 2,
        'VAN': 1, 'COL': 1, 'PHI': 1, 'BOS': 1,
        'CGY': 0, 'STL': 0, 'ARI': 0, 'CHI': 0,
        'CBJ': 0, 'WSH': 0, 'CAR': 0, 'MTL': 0
    },
    '2018-2019': {
        'STL': 4, 'BOS': 3, 'SJS': 2, 'CAR': 2,
        'COL': 1, 'DAL': 1, 'CBJ': 1, 'NYI': 1,
        'VGK': 0, 'WIN': 0, 'CGY': 0, 'NSH': 0,
        'PIT': 0, 'TOR': 0, 'WSH': 0, 'TBL': 0
    },
    '2017-2018': {
        'WSH': 4, 'VGK': 3, 'WPG': 2, 'TBL': 2,
        'NSH': 1, 'SJS': 1, 'BOS': 1, 'PIT': 1,
        'ANA': 0, 'MIN': 0, 'LAK': 0, 'COL': 0,
        'PHI': 0, 'TOR': 0, 'CBJ': 0, 'NJD': 0
    },
    '2016-2017': {
        'PIT': 4, 'NSH': 3, 'ANA': 2, 'OTT': 2,
        'STL': 1, 'EDM': 1, 'WSH': 1, 'NYR': 1,
        'SJS': 0, 'CGY': 0, 'MIN': 0, 'CHI': 0,
        'CBJ': 0, 'TOR': 0, 'BOS': 0, 'MTL': 0
    },
    '2015-2016': {
        'PIT': 4, 'SJS': 3, 'STL': 2, 'TBL': 2,
        'DAL': 1, 'NSH': 1, 'NYI': 1, 'WSH': 1,
        'ANA': 0, 'LAK': 0, 'MIN': 0, 'CHI': 0,
        'PHI': 0, 'NYR': 0, 'DET': 0, 'FLA': 0
    },
    '2014-2015': {
        'CHI': 4, 'TBL': 3, 'ANA': 2, 'NYR': 2,
        'MIN': 1, 'CGY': 1, 'MTL': 1, 'WSH': 1,
        'VAN': 0, 'WIN': 0, 'NSH': 0, 'STL': 0,
        'NYI': 0, 'PIT': 0, 'DET': 0, 'OTT': 0
    },
    '2013-2014': {
        'LAK': 4, 'NYR': 3, 'CHI': 2, 'MTL': 2,
        'ANA': 1, 'MIN': 1, 'BOS': 1, 'PIT': 1,
        'SJS': 0, 'DAL': 0, 'STL': 0, 'COL': 0,
        'PHI': 0, 'CBJ': 0, 'TBL': 0, 'DET': 0
    },
    '2012-2013': {
        'CHI': 4, 'BOS': 3, 'LAK': 2, 'PIT': 2,
        'DET': 1, 'SJS': 1, 'OTT': 1, 'NYR': 1,
        'STL': 0, 'VAN': 0, 'ANA': 0, 'MIN': 0,
        'TOR': 0, 'WSH': 0, 'MTL': 0, 'NYI': 0
    },
    '2011-2012': {
        'LAK': 4, 'NJD': 3, 'ARI': 2, 'NYR': 2,
        'STL': 1, 'NSH': 1, 'WSH': 1, 'PHI': 1,
        'DET': 0, 'CHI': 0, 'SJS': 0, 'VAN': 0,
        'PIT': 0, 'FLA': 0, 'BOS': 0, 'OTT': 0
    },
    '2010-2011': {
        'BOS': 4, 'VAN': 3, 'SJS': 2, 'TBL': 2,
        'NSH': 1, 'DET': 1, 'WSH': 1, 'PHI': 1,
        'ANA': 0, 'ARI': 0, 'LAK': 0, 'CHI': 0,
        'PIT': 0, 'MTL': 0, 'BUF': 0, 'NYR': 0
    },
    '2009-2010': {
        'CHI': 4, 'PHI': 3, 'SJS': 2, 'MTL': 2,
        'DET': 1, 'VAN': 1, 'PIT': 1, 'BOS': 1,
        'ARI': 0, 'LAK': 0, 'NSH': 0, 'COL': 0,
        'OTT': 0, 'BUF': 0, 'NJD': 0, 'WSH': 0
    },
    '2008-2009': {
        'PIT': 4, 'DET': 3, 'CHI': 2, 'CAR': 2,
        'ANA': 1, 'VAN': 1, 'BOS': 1, 'WSH': 1,
        'CGY': 0, 'STL': 0, 'CBJ': 0, 'SJS': 0,
        'PHI': 0, 'NJD': 0, 'NYR': 0, 'MTL': 0
    },
}
