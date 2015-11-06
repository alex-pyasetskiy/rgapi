from datetime import datetime, timedelta

import pytz

EPOCH = datetime(1970, 1, 1, 0, 0, tzinfo=pytz.utc)


def convert_epoch_millis_to_datetime(epoch_millis):
    return EPOCH + timedelta(milliseconds=epoch_millis)


class Summoner(object):
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.profile_icon_id = kwargs['profileIconId']
        self.revision_date = convert_epoch_millis_to_datetime(kwargs['revisionDate'])
        self.summoner_level = kwargs['summonerLevel']

    def __stringify(self):
        obj_dict = self.__dict__
        object_string = ''
        for key in obj_dict:
            object_string = object_string + '{0}: {1}\n'.format(key, obj_dict[key])

        return object_string

    def __repr__(self):
        return self.__stringify()

    def __str__(self):
        return self.__stringify()

    def __unicode__(self):
        return self.__stringify()


class SummonerApiService(object):
    __api_version__ = '1.4'
    __service_name__ = 'summoners_api'

    def __init__(self, client):
        self.base_request = client.base_request

    def _summoner_request(self, end_url, region, **kwargs):
        return self.base_request(
            'v{version}/summoner/{end_url}'.format(
                version=self.__api_version__,
                end_url=end_url
            ),
            region,
            **kwargs
        )

    @staticmethod
    def sanitized_name(name):
        return name.replace(' ', '').lower()

    def get_summoners(self, names=None, ids=None, region=None):
        """
        Get summoner objects mapped by standardized summoner name for a given list of summoner names.

        :param names: list of requested names
        :type names: list[str]

        :param ids: list of summoner IDs associated with summoners to retrieve.
        :type ids: list[str]

        :param region: Region where to retrieve the data.
        :type region: Region

        :return: dictionary contains the summoner objects mapped by the standardized summoner name or None.
        :rtype: dict[str,dict] | None
        """
        if (names is None) != (ids is None):
            return self._summoner_request(
                'by-name/{summoner_names}'.format(
                    summoner_names=','.join([self.sanitized_name(n) for n in names])) if names is not None
                else '{summoner_ids}'.format(summoner_ids=','.join([str(i) for i in ids])),
                region
            )
        else:
            return None

    def get_summoner(self, name=None, _id=None, region=None):
        """
        Get single summoner objects mapped by standardized summoner name.

        :param name: requested names
        :type name: str

        :param _id: summoner IDs associated with summoners to retrieve.
        :type _id: str

        :param region: Region where to retrieve the data.
        :type region: Region

        :return: dictionary contains the summoner objects mapped by the standardized summoner name or None.
        :rtype: dict[str,dict] | None
        """
        if (name is None) != (_id is None):
            if name is not None:
                name = self.sanitized_name(name)
                return self.get_summoners(names=[name], region=region)[name]
            else:
                return self.get_summoners(ids=[_id], region=region)[str(_id)]
        return None

    def get_summoner_names(self, summoner_ids, region=None):
        """
        Get summoner names mapped by summoner ID for a given list of summoner IDs

        :param summoner_ids: Comma-separated list of summoner IDs associated with summoner names to retrieve.
        :type summoner_ids: list[str]

        :param region: Region where to retrieve the data.
        :type region: Region

        :return: summoner names mapped by summoner ID for a given list of summoner IDs.
        :rtype: dict[str,str]
        """
        return self._summoner_request(
            '{summoner_ids}/name'.format(summoner_ids=','.join([str(s) for s in summoner_ids])),
            region
        )

    def get_mastery_pages(self, summoner_ids, region=None):
        return self._summoner_request(
            '{summoner_ids}/masteries'.format(summoner_ids=','.join([str(s) for s in summoner_ids])),
            region
        )

    def get_rune_pages(self, summoner_ids, region=None):
        """
        Get rune pages mapped by summoner ID for a given list of summoner IDs.

        :param summoner_ids: list or summoners ids
        :type summoner_ids: list[str]

        :param region: Region where to retrieve the data.
        :type region: Region

        :return: runa pages
        :rtype: dict
        """
        return self._summoner_request(
            '{summoner_ids}/runes'.format(summoner_ids=','.join([str(s) for s in summoner_ids])),
            region
        )