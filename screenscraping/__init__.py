from .webdrivers import WEBDRIVERS

def get_driver_details(name:str):
    return WEBDRIVERS[name]

def get_browser(name:str):
    """
    #TODO complete google style docs
    :param name:
    :return:
    """
    browser_details = get_driver_details(name)
    return browser_details['class_'](executable_path=browser_details['exec_path'])

