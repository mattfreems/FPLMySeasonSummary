from get_data import get
from player import Player

def getOverallGWStats(range=(1,38)):
    """
    Gets data for each gw in range
    :param range: between which GW's should data be displayed
    :return:
    """
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    gw_data = get(url)['events'][(range[0]-1):range[1]]
    return gw_data

def getGWStats(gw):
    """
    Returns overall stats for one GW
    :param gw: the GW for which you want the stats from
    :return:
    """
    return getOverallGWStats((gw,gw))

def getAverageGWScores(range = (1,38)):
    """
    Return the average GW score for the GW's in the range specified
    :param range: between which GW's should data be displayed
    :return: list of average scores
    """
    gw_data = getOverallGWStats(range)
    return [gw['average_entry_score'] for gw in gw_data]

def getHighestManagerScores(range = (1,38)):
    """
    Return the highest score in each GW for the GW's in the range specified
    :param range: between which GW's should data be displayed
    :return: list of highest scores
    """
    gw_data = getOverallGWStats(range)
    return [gw['highest_score'] for gw in gw_data]

def getHighestPlayerScores(range=(1,38)):
    """
    The player that scored the highest number of points in the GW in the GW range
    :param range: between which GW's should data be displayed
    :return: the id, name and points they scored
    """
    gw_data = getOverallGWStats(range)
    players = [gw['top_element_info'] for gw in gw_data]
    for p in players:
        p['name'] = Player(p['id']).getName()
    return players

def getHighestPlayerScoresGW(gw):
    """
    Get the highest scoring player in specific GW
    :param gw: the GW to get the highest scoring player from
    :return: the name, id and score from the player
    """
    return getHighestPlayerScores((gw,gw))

def getNumManagers():
    """
    Gets the total number of managers in the game
    :return: int: total number of managers
    """
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    return get(url)['total_players']
