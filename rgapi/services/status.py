# lol-status-v1.0
import requests

from ..exceptions import validate_response


class ServerStatusAPIService(object):
    __api_version__ = '1.0'
    __service_name__ = 'status_api'

    def __init__(self, client=None):
        if client is not None:
            client.register_api_service(self)

    def __repr__(self):
        return u"<{name}>({service}-v{version})".format(name=self.__class__.__name__,
                                                        service=self.__service_name__,
                                                        version=self.__api_version__)

    @staticmethod
    def get_status(region=None):
        if region is None:
            url = 'shards'
        else:
            url = 'shards/{region}'.format(region=region)
        r = requests.get('http://status.leagueoflegends.com/{url}'.format(url=url))
        validate_response(r)
        return r.json()
