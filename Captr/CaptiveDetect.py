from __future__ import annotations
import requests as rq
import logging
import yaml
from typing import NamedTuple, Type

class CaptiveNotImplemented(Exception):
    """Raised when there isnt a captive portal detected"""
    pass

class CaptiveDetector:
    """
    Class to be used to detect if a captive portal is present in a network or if there is some other type of authentication.
    
    Attributes
    ----------
        CaptivePortalURL: The URL/IP of the Captive Portal if present
        PortalResult: Boolean, True if a captive portal is found that matches the files choice to possibly mandate HTTPS
        
    """
    def __init__(self,  URL: str, HTTPSonlyswitch: bool = False, loggingSwitch: bool = True) -> None: 
        #with open ('logging.yml', 'r') as file:
#            logging.config.dictConfig(yaml.safe_load(file))
        self.logger=logging.getLogger(__name__)
        self._URL=URL
        self._session=rq.Session()
        self._session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'})
        self.resultcode: int
        self.httpsSwitch=HTTPSonlyswitch
        self.PortalResult=bool(self.PortalDetect())
        self.CaptivePortalURL: str
    
    def PortalDetect(self)->bool:
        """
        Method that returns a true or false depending on if a method exists or not as well as checks if the captive portal page is https
        """
        firstquery = self._session.head(self._URL)
        self.resultcode=int(firstquery.status_code)
        #these status codes would indicate the potential presence of a captive portal.
        if (self.resultcode >= 300 and self.resultcode < 400): #deals with 3XX redirect captive portals
            secondURL=firstquery.headers.get('Location')
        #checking that there was a location
            if isinstance(secondURL, str):
                if self.httpsSwitch == True and secondURL.startswith('https://'):
                    self.CaptivePortalURL=str(secondURL)
                    return(True)
                elif self.httpsSwitch == False:
                    self.CaptivePortalURL=str(secondURL)
                    return(True)
                else:
                    return(False)
            else: #TODO: Better define the exception something weird occured if this is triggered
                raise CaptiveNotImplemented('There seems to be a unsupported redirect')
        elif self.resultcode == 511: #deals with 511 type captive portals
        #TODO: figure out how to implement this
            raise NotImplementedError("Sorry, Currently we dont support 511 captive portals but its on our roadmap!")
        else: 
            return(False)
        
n=CaptiveDetector('http://ping.archlinux.org', False)
print(n.resultcode)