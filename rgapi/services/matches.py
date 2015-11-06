class MatchesAPIService(object):
    __api_version__ = '2.2'
    __service_name__ = 'matches_api'

    def __init__(self, client):
        self.api_request = client.api_request

    def __repr__(self):
        return u"<{name}>({service}-v{version})".format(name=self.__class__.__name__,
                                                        service=self.__service_name__,
                                                        version=self.__api_version__)

    # match-v2.2
    def _match_request(self, end_url, region, **kwargs):
        return self.api_request(
            'v{version}/match/{end_url}'.format(
                version=self.__api_version__,
                end_url=end_url
            ),
            region,
            **kwargs
        )

    # match list-v2.2
    def _match_list_request(self, end_url, region, **kwargs):
        return self.api_request(
            'v{version}/matchlist/by-summoner/{end_url}'.format(
                version=self.__api_version__,
                end_url=end_url,
            ),
            region,
            **kwargs
        )

    # game-v1.3
    def _game_request(self, end_url, region, **kwargs):
        return self.api_request(
            'v{version}/game/{end_url}'.format(
                version="v1.3",  # TODO: remove
                end_url=end_url
            ),
            region,
            **kwargs
        )

    def get_match(self, match_id, region=None, include_timeline=False):
        return self._match_request(
            '{match_id}'.format(match_id=match_id),
            region,
            includeTimeline=include_timeline
        )

    def get_match_list(self, summoner_id, region=None, champion_ids=None, ranked_queues=None, seasons=None,
                       begin_time=None, end_time=None, begin_index=None, end_index=None):
        return self._match_list_request(
            '{summoner_id}'.format(summoner_id=summoner_id),
            region,
            championsIds=champion_ids,
            rankedQueues=ranked_queues,
            seasons=seasons,
            beginTime=begin_time,
            endTime=end_time,
            beginIndex=begin_index,
            endIndex=end_index
        )

    def get_recent_games(self, summoner_id, region=None):
        return self._game_request('by-summoner/{summoner_id}/recent'.format(summoner_id=summoner_id), region)
