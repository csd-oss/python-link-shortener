from device_detector import DeviceDetector


def device_parser(ua):
    device = DeviceDetector(ua).parse()
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
    return deviceObj
