from enum import Enum


class RGApiException(Exception):
    def __init__(self, error, response):
        self.error = error
        self.headers = response.headers

    def __str__(self):
        return self.error


class RGApiResponseError(Enum):
    error_400 = "Bad request"
    error_401 = "Unauthorized"
    error_404 = "Game data not found"
    error_429 = "Too many requests"
    error_500 = "Internal server error"
    error_503 = "Service unavailable"


def validate_response(response):
    if response.status_code == 400:
        raise RGApiException(RGApiResponseError.error_400, response)
    elif response.status_code == 401:
        raise RGApiException(RGApiResponseError.error_401, response)
    elif response.status_code == 404:
        raise RGApiException(RGApiResponseError.error_404, response)
    elif response.status_code == 429:
        raise RGApiException(RGApiResponseError.error_429, response)
    elif response.status_code == 500:
        raise RGApiException(RGApiResponseError.error_500, response)
    elif response.status_code == 503:
        raise RGApiException(RGApiResponseError.error_503, response)
    else:
        response.raise_for_status()


class RGApiWarning(Warning):
    def __init__(self, message):
        self.message = "CLIENT WARNING!!! " + message
        super(RGApiWarning, self).__init__(self.message)

    def __str__(self):
        return self.message
