import requests

from .common import DEFAULT_REGION, API_RATE_LIMITS
from .exceptions import validate_response, RGApiWarning


class RGApiClient(object):
    def __init__(self, key, default_region=DEFAULT_REGION, limits=API_RATE_LIMITS.DEVELOP):
        self.key = key
        self.default_region = default_region
        self.limits = limits

    def _set_api_service(self, service):
        setattr(self, service.__service_name__, service)

    def register_api_service(self, service):
        new_service_name = service.__service_name__
        new_service_version = service.__api_version__

        if hasattr(self, new_service_name):
            current_service = getattr(self, new_service_name)
            if current_service.__api_version__ == new_service_version:
                raise RGApiWarning("API Service {name}-{version} already registered!".format(name=new_service_name,
                                                                                             version=new_service_version))
            elif current_service.__api_version__ > new_service_version:
                raise RGApiWarning(" Service {service} already registered with newer version {version}! " \
                                   "(passed service version: {old})".format(service=current_service,
                                                                            version=current_service.__api_version__,
                                                                            old=new_service_version))

            elif current_service.__api_version__ < new_service_version:
                print "Updating {service} from {old_v} to {new_v}".format(service=current_service,
                                                                          old_v=current_service.__api_version__,
                                                                          new_v=new_service_version)
                delattr(self, current_service.__service_name__)
                self._set_api_service(service)
        else:
            self._set_api_service(service)
            print "API Service {name}-{version} registered! Access: cline.{name}".format(name=new_service_name,
                                                                                         version=new_service_version)

    def verify_rate_limit(self):
        for lim in self.limits:
            if not lim.request_available():
                return False
        return True

    def api_request(self, url, region, static=False, **kwargs):
        if region is None:
            region = self.default_region
        args = {'api_key': self.key}
        for k in kwargs:
            if kwargs[k] is not None:
                args[k] = kwargs[k]
        r = requests.get(
            'https://{proxy}.api.pvp.net/api/lol/{static}{region}/{url}'.format(
                proxy='global' if static else region,
                static='static-data/' if static else '',
                region=region,
                url=url
            ),
            params=args
        )
        if not static:
            for lim in self.limits:
                lim.add_request()
        validate_response(r)
        return r.json()
