from get_data import get

class Player:
    all_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    all_info = get(all_url)

    def __init__(self, _id, _range=(1,38)):
        self.id = _id
        self.range = _range
        self.player_info = next((p for p in self.all_info['elements'] if p['id'] == self.id), None)

    def getName(self):
        """
        Get the name of the player with self.id
        :return: name as str()
        """
        return self.player_info['first_name'], self.player_info['second_name']

    def getOverallPoints(self):
        """
        Get the total number of points scored by the player with self.id
        :return:
        """
        return self.player_info['total_points']

    def getAllGWData(self):
        """
        Shows the data from each GW in the self.range for the player
        :return: list of dictionaries where each dictionary is a separate GW
        """
        gw_range = self.range
        min_gw = gw_range[0]
        max_gw = gw_range[1]
        gw_data = []

        for gw in range(min_gw, max_gw+1):
            gw_url = f'https://fantasy.premierleague.com/api/event/{gw}/live/'
            gw_data.append(next((p['stats'] for p in get(gw_url)['elements'] if p['id'] == self.id), None))

        return gw_data

    def getSingleGWData(self, gameweek):
        """
        Gets player data for a single GW
        :param gameweek: the GW to select
        :return: data from that one GW as a dictionary
        """
        gw_url = f'https://fantasy.premierleague.com/api/event/{gameweek}/live/'

        gw_data = next((p['stats'] for p in get(gw_url)['elements'] if p['id'] == self.id), None)

        return gw_data

    def __str__(self):
        return f"Player id is {self.id} \n" \
        f"Player info is {self.player_info}"

