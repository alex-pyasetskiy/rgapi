# Regions
from collections import deque
import time

from enum import Enum


class RateLimit(object):
    def __init__(self, allowed_requests, seconds):
        self.allowed_requests = allowed_requests
        self.seconds = seconds
        self.made_requests = deque()

    def __reload(self):
        t = time.time()
        while len(self.made_requests) > 0 and self.made_requests[0] < t:
            self.made_requests.popleft()

    def add_request(self):
        self.made_requests.append(time.time() + self.seconds)

    def request_available(self):
        self.__reload()
        return len(self.made_requests) < self.allowed_requests


class REGIONS(Enum):
    BRAZIL = 'br'
    EUROPE_NORDIC_EAST = 'eune'
    EUROPE_WEST = 'euw'
    KOREA = 'kr'
    LATIN_AMERICA_NORTH = 'lan'
    LATIN_AMERICA_SOUTH = 'las'
    NORTH_AMERICA = 'na'
    OCEANIA = 'oce'
    RUSSIA = 'ru'
    TURKEY = 'tr'


DEFAULT_REGION = REGIONS.EUROPE_WEST


class API_RATE_LIMITS(Enum):
    DEVELOP = (RateLimit(10, 10), RateLimit(500, 600),)
    PRODUCTION = (RateLimit(3000, 10), RateLimit(180000, 600),)
