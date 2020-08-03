from device_detector import DeviceDetector


def device_parser(ua):
    device = DeviceDetector(ua).parse()
    deviceObj = {
        'isBot': device.is_bot(),
        'osName': device.os_name(),
        'osVersion': device.os_version(),
        'brand': device.device_brand_name(),
        'model': device.device_model(),
        'type': device.device_type()
    }
    return deviceObj
