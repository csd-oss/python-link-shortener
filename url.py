from device_detector import DeviceDetector


class Url:
    def __init__(
                self, shortLink="", redirectTo="",
                callbackUrl="", _id="", userAgent=""):
        self.__shortLink = shortLink
        self.__redirectTo = redirectTo
        self.__callbackUrl = callbackUrl
        self._id = _id
        self.__userAgent = userAgent

    def parse_device(self):
        device = DeviceDetector(self.__userAgent).parse()
        deviceObj = {
            'isBot': device.is_bot(),
            'osName': device.os_name(),
            'osVersion': device.os_version(),
            'brand': device.device_brand_name(),
            'model': device.device_model(),
            'type': device.device_type(),
            'clientName': device.client_name(),
            'clientType': device.client_type(),
            'clientVersion': device.client_version(),
            'engine': device.engine()
        }
        self.__device = deviceObj


url = Url()

print(url.__dict__)
