import json
import time
from flask import redirect
import requests
from device_detector import DeviceDetector


class Url:
    def __init__(
                self, shortLink="", redirectTo="",
                callbackUrl="", _id="", userAgent=""
                ):
        self.__shortLink = shortLink
        self.__redirectTo = redirectTo
        self.__callbackUrl = callbackUrl
        self._id = _id
        self.__userAgent = userAgent

    def send_callbak(self):
        if self.__callbackUrl != "":
            headers = {'content-type': 'application/json'}
            data = self.__url_obj()
            data['timestamp'] = time.time()
            print(json.dumps(data))
            requests.request(
                "POST", self.__callbackUrl, data=json.dumps(data),
                headers=headers
            )
        else:
            pass

    def redirect_user(self):
        return redirect(self.__redirectTo)

    def __parse_device(self):
        # TODO This should be async probably, cos without it
        # user gets reireted much faster
        device = DeviceDetector(self.__userAgent).parse()
        deviceObj = {
            "isBot": device.is_bot(),
            "osName": device.os_name(),
            "osVersion": device.os_version(),
            "brand": device.device_brand_name(),
            "model": device.device_model(),
            "type": device.device_type(),
            "clientName": device.client_name(),
            "clientType": device.client_type(),
            "clientVersion": device.client_version(),
            "engine": device.engine()
        }
        self.__device = deviceObj

    def __url_obj(self):
        self.__parse_device()
        url_obj = {
            "device": self.__device,
            "shortLink": self.__shortLink,
            "redirectTo": self.__redirectTo,
            "callbackUrl": self.__callbackUrl,
            "_id": self._id,
            "userAgent": self.__userAgent
            }
        return url_obj
