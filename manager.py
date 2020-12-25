from get_data import get
from player import Player

class Manager:
    def __init__(self, _id, _range=(1,38)):
        self.id = _id
        self.range = _range

    def getSummaryData(self):
        """
        Gets the basic team summary data for the manager

         - important keys of the resulting dict are:
            - summary_overall_points, summary_overall_rank, summary_event_rank, summary_event_points,
              last_deadline_total_transfers

        """
        url = f"https://fantasy.premierleague.com/api/entry/{self.id}/"
        return get(url)

    def getTransferData(self):
        """
        Restructure the transfer history of the manager
        :return:
        """
        url = f"https://fantasy.premierleague.com/api/entry/{self.id}/transfers/"
        transfers_url = get(url)
        min_gw = self.range[0]
        max_gw = self.range[1]
        chips = Manager.getChips(self)
        transfers = []

        for gw in range(min_gw, max_gw+1):
            trans_list = [t for t in transfers_url if t['event'] == gw]
            t_in_id = [t['element_in'] for t in trans_list]
            t_in_names = [Player(t).getName() for t in t_in_id]
            t_out_id = [t['element_out'] for t in trans_list]
            t_out_names = [Player(t).getName() for t in t_out_id]
            t_in_cost = [t['element_in_cost']/10 for t in trans_list]
            t_out_cost = [t['element_out_cost']/10 for t in trans_list]
            transfers.append({'in': {'id': t_in_id, 'name': t_in_names, 'price': t_in_cost},
                             'out': {'id': t_out_id, 'name': t_out_names, 'price': t_out_cost}})

        for chip in chips:
            if chip['name'] == 'wildcard' or chip['name'] == 'freehit':
                transfers[chip['event']-1] = chip['name']
        return transfers

    def getDetailedGWData(self):
        """
        Get in-depth individual GW data for the manager including picks

        :return: list of dicts where each element is a separate GW - each GW has 'active chip', 'automatic_subs',
        'entry_history', 'picks'
        """

        gw_range = self.range
        min_gw = gw_range[0]
        max_gw = gw_range[1]
        gw_data = []
        url = f"https://fantasy.premierleague.com/api/entry/{self.id}/event/"

        for gw in range(min_gw, max_gw+1):
            gw_url = url + f"{gw}/picks/"
            gw_data.append(get(gw_url))

        #for gw in gw_data:
        #    for pick in gw['picks']:
        #        pick['points'] = Player(pick['element']).getSingleGWData(gw['entry_history']['event'])['total_points']

        return gw_data

    def getSummaryGWData(self):
        """
        GW summary data for each week
        Also returns past season performance
        And chips played throughout the season
        :return:
        """
        gw_range = self.range
        min_gw = gw_range[0]
        max_gw = gw_range[1]

        url = f"https://fantasy.premierleague.com/api/entry/{self.id}/history/"
        summary_data = get(url)

        summary_data['current'] = summary_data['current'][(min_gw-1):(max_gw)]

        return summary_data

    def getMiniLeagueData(self):
        """
        Get a list of all the minileagues the manager is apart of and the position they are in
        :return:
        """
        league_data = Manager.getSummaryData(self)['leagues']
        return league_data

    def getOverallPoints(self):
        """
        Return overall points from the manager
        :return:
        """
        return Manager.getSummaryData(self)['summary_overall_points']

    def getOverallRank(self):
        """
        Get current rank of manager
        :return:
        """
        return Manager.getSummaryData(self)['summary_overall_rank']

    def MiniLeagueSummary(self):
        """
        Returns a summary of classic leagues the manager is a member of
        :return:
        """
        league_data = Manager.getMiniLeagueData(self)['classic']
        league_summary = []

        for l in league_data:
            if l['league_type'] == 'x':
                l_id = l['id']
                standings_url = f"https://fantasy.premierleague.com/api/leagues-classic/{l_id}/standings/"
                standings = get(standings_url)['standings']
                league_summary.append({'league_id': l_id, 'league_name': l['name'], 'rank': l['entry_rank'],
                                       'standings': standings})
        return league_summary

    def getChips(self):
        """
        Return the chips data for the manager
        :return:
        """
        return Manager.getSummaryGWData(self)['chips']

    def getHits(self):
        """
        Get a list of costs of transfers per GW
        :return: list of len self.range where each element corresponds to the respective GW
        """
        hits = []
        summary = Manager.getSummaryGWData(self)
        gws = summary['current']
        for gw in gws:
            hits.append(gw['event_transfers_cost'])

        return hits

    def getRanks(self):
        """
        Overall rank after each GW in self.range
        :return:
        """
        ranks = []
        summary = Manager.getSummaryGWData(self)
        gws = summary['current']
        for gw in gws:
            ranks.append(gw['overall_rank'])

        return ranks

    def getCaptainData(self):
        """
        Get the Captain pick and points for each gameweek in self.range
        :return:
        """
        gws = Manager.getDetailedGWData(self)
        captains = [player for gw in gws for player in gw['picks'] if player['multiplier']==2]
        return captains

    def getPastSeasonData(self):
        """
        Previous season data for the manager
        :return:
        """
        url = f"https://fantasy.premierleague.com/api/entry/{self.id}/history/"
        summary_data = get(url)
        return summary_data['past']

    def getName(self):
        """
        Returns the name of the FPL manager
        :return: [0] gives first name, [1] gives last name
        """
        f_n = Manager.getSummaryData(self)['player_first_name']
        l_n = Manager.getSummaryData(self)['player_last_name']
        return f_n, l_n

