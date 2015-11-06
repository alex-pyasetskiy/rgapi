class ServerStatusAPIService(object):
    __api_version__ = '1.3'
    __service_name__ = 'stats_api'

    def __init__(self, client):
        self.api_request = client.api_request

    def __repr__(self):
        return u"<{name}>({service}-v{version})".format(name=self.__class__.__name__,
                                                        service=self.__service_name__,
                                                        version=self.__api_version__)

    def _stats_request(self, end_url, region, **kwargs):
        return self.api_request(
            'v{version}/stats/{end_url}'.format(
                version=self.__api_version__,
                end_url=end_url
            ),
            region,
            **kwargs
        )

    def get_stat_summary(self, summoner_id, region=None, season=None):
        """
        Retrieve player stats summaries by summoner ID

        :param summoner_id: ID of the summoner for which to retrieve player stats.
        :type summoner_id: str

        :param region: Region where to retrieve the data.
        :type region: str

        :param season: specified, stats for the given season are returned. Current season by default
        :type season: str

        :return: collection of player stats summary information.
        :rtype: dict
        """
        return self._stats_request(
            'by-summoner/{summoner_id}/summary'.format(summoner_id=summoner_id),
            region,
            season='SEASON{}'.format(season) if season is not None else None)

    def get_ranked_stats(self, summoner_id, region=None, season=None):
        """
        Retrieve ranked stats by summoner ID.

        :param summoner_id: ID of the summoner for which to retrieve player stats.
        :type summoner_id: str

        :param region: Region where to retrieve the data.
        :type region: str

        :param season: specified, stats for the given season are returned. Current season by default
        :type season: str

        :return: object that contains ranked stats information.
        :rtype: dict
        """
        return self._stats_request(
            'by-summoner/{summoner_id}/ranked'.format(summoner_id=summoner_id),
            region,
            season='SEASON{}'.format(season) if season is not None else None
        )
