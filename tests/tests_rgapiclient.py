from unittest import TestCase

from nose.tools import assert_is_instance, assert_in, assert_dict_equal

from nose.tools import raises

from rgapi import RGApiClient
from rgapi.exceptions import RGApiWarning

key = 'fd8b51de-ce68-4a1d-89a4-d216dcdac89d'

# test data, RU
summoner = {"shanmar": {
    "id": 310558,
    "name": "Shanmar",
    "profileIconId": 936,
    "revisionDate": 1446828133000,
    "summonerLevel": 30
}}


class FakeApiService(object):
    __api_version__ = '2.0'
    __service_name__ = 'super_api'

    def __init__(self, client=None, version='2.0'):
        self.__api_version__ = version
        if client is not None:
            client.register_api_service(self)

    def do_some(self):
        return {"awesome": "response"}


# noinspection PyUnresolvedReferences
class RgpiClientSpec(TestCase):
    def setUp(self):
        self.client = RGApiClient("key")

    def test_registration_new_api_service(self):
        service = FakeApiService()
        self.client.register_api_service(service)

        assert_in('super_api', self.client.__dict__)
        assert_is_instance(self.client.super_api, FakeApiService)
        assert_dict_equal(self.client.super_api.do_some(), {"awesome": "response"})

    @raises(RGApiWarning)
    def test_registration_existing_api_service_raisin_RGApiWarning(self):
        service = FakeApiService()
        self.client.register_api_service(service)
        self.client.register_api_service(service)

        #
        # assert_in('super_api', self.client.__dict__)
        # assert_is_instance(self.client.super_api, FakeApiService)
        # print self.client.super_api.__dict__
        # assert_dict_equal(self.client.super_api.do_some(), {"awesome": "response"})
