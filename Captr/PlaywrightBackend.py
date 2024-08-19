from Captr.backend import backend
from playwright import sync_api as sa
import logging
import time


class PlayWrightBackend(backend):
    """
    Class that serves as a factory for all the PlayWrightBackends
    """
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.browser : sa._generated.Browser
        self.page : sa._generated.Page

    def _checker(self, value: str) -> bool:
        """checks the types of the values against a set value"""
        allowedVals = ["spinbutton", "button", "checkbox", "textbox", "searchbox"]
        if value in allowedVals:
            return True
        else:
            return False

    def Layout_Fetch(self, URL: str) -> str:  #Return the Layout after javascript is rendered
        return self.page.content()
    def Start(self, URLstart: str) -> bool:  #default url 
        self.page.goto(URLstart)
        self.logger.debug(f"Setting the starting URL to {URLstart}")
        return True
    def Move(self, locator: dict) -> bool:  #used to move to a URI without interacting with anything
        match list(locator.keys()):
            case ["xpath"]:
                try:  #will error out if there is no href contained in the item
                    self.logger.debug(f"starting moving to items with xpath:{locator["xpath"]}")
                    url = self.page.locator(f'xpath={str(locator["xpath"])}').get_attribute('href')
                    assert isinstance(url, str)
                    self.page.goto(url)
                except AssertionError:
                    self.logger.warning("cannot find href in target, skipping. . .")
                    return False
            case ["id"]:
                try:  #will error out if there is no href contained in the item
                    self.logger.debug(f"starting moving to items with id:{locator["id"]}")
                    url = self.page.locator(f"#{str(locator["id"])}").get_attribute('href')
                    assert isinstance(url, str)
                    self.page.goto(url)
                except AssertionError:
                    self.logger.warning("cannot find href in target, skipping. . .")
                    return False
            case ['href']:  #no need to use playwright for this the URL is already supplied for us
                self.page.goto(locator["href"])
        return True
    def Text(self, locator: dict, value: str) -> bool:
        match list(locator.keys()):
            case ["type"]:
                self.logger.debug(f"typing chars to the corresponding type:{locator["type"]}")
                if self._checker(locator["type"]) is True:
                    self.page.get_by_role(locator["type"]).press_sequentially(value)
                else:
                    self.logger.warning(f"Notice: type:{locator["type"]} is not supported skipping . . .")
            case ["name"]:
                self.logger.debug(f"typing chars to the name:{locator["name"]}")
                self.page.locator(f'input[name="{locator["name"]}"]').press_sequentially(value)
            case ["contains"]:
                self.logger.debug(f"starting typing strings to items that contain the substring:{locator["contains"]}")
                self.page.get_by_alt_text(locator["contains"]).press_sequentially(value)
                self.page.get_by_placeholder(locator["contains"]).press_sequentially(value)
                self.page.get_by_title(locator["contains"]).press_sequentially(value)
                self.page.get_by_label(locator["contains"]).press_sequentially(value)
            case ["xpath"]:
                self.logger.debug(f"starting typing strings to items with xpath:{locator["xpath"]}")
                self.page.locator(f'xpath={str(locator["xpath"])}').press_sequentially(value)
            case ["id"]:
                self.logger.debug(f"starting typing strings to id:{locator["id"]}")
                self.page.locator(f"#{str(locator["id"])}").press_sequentially(value)
            case _:
                pass

        return True
    def Wait(self, Timespan: int) -> bool:
        time.sleep(Timespan)
        return True
    def Click(self, locator: dict) -> bool:
        match list(locator.keys()):
            case ["type"]:
                self.logger.debug(f"clicking items of the corresponding type:{locator["type"]}")
                if self._checker(locator["type"]) is True:    
                    self.page.get_by_role(locator["type"]).click()
                else:
                    self.logger.warning(f"Notice: type:{locator["type"]} is not supported skipping . . .")
            case ["name"]:
                self.logger.debug(f"starting clicking items containing the name:{locator["name"]}")
                self.page.locator(f'input[name="{locator["name"]}"]').click()
            case ["contains"]:
                self.logger.debug(f"starting clicking items with substring:{locator["contains"]}")
                self.page.get_by_alt_text(locator["contains"]).click()
                self.page.get_by_placeholder(locator["contains"]).click()
                self.page.get_by_title(locator["contains"]).click()
                self.page.get_by_label(locator["contains"]).click()
            case ["xpath"]:
                self.logger.debug(f"starting clicking to the item with xpath:{locator["id"]}")
                self.page.locator(f'xpath={str(locator["xpath"])}').click()
            case ["id"]:
                self.logger.debug(f"starting clicking to the item with id:{locator["id"]}")
                self.page.locator(f"#{str(locator["id"])}").click()
            case _:
                pass
        return True
    

class FirefoxPlaywrightBackend(PlayWrightBackend):
    def __init__(self) -> None:
        """
        Playwright Backend using Firefox
        """
        super().__init__()
        self.browser = sa.sync_playwright().start().firefox.launch()
        self.logger.debug("Initializing firefox browser instance")
        self.page = self.browser.new_page()


class FirefoxVizPlaywrightBackend(PlayWrightBackend):
    """
    Playwright Backend that will launch the Firefox browser in a non-headless mode
    """
    def __init__(self) -> None:
        super().__init__()
        self.browser = sa.sync_playwright().start().firefox.launch(headless=False)
        self.logger.debug("Initializing firefox browser instance")
        self.page = self.browser.new_page()


class ChromiumPlaywrightBackend(PlayWrightBackend):
    """
    Playwright Backend using chromium
    """
    def __init__(self) -> None:
        super().__init__()
        self.browser = sa.sync_playwright().start().chromium.launch()
        self.logger.debug("Initializing chromium browser instance")
        self.page = self.browser.new_page()


class ChromiumVizPlaywrightBackend(PlayWrightBackend):
    """
    Playwright Backend that will launch the Chromium browser in a non-headless mode
    """
    def __init__(self) -> None:
        super().__init__()
        self.browser = sa.sync_playwright().start().chromium.launch(headless=False)
        self.logger.debug("Initializing chromium browser instance")
        self.page = self.browser.new_page()
