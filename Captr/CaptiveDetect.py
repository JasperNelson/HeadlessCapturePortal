from __future__ import annotations
import requests as rq
import logging
import yaml
from typing import NamedTuple, Type




class CaptiveDetector:
    """
    Class to be used to detect if a captive portal is present in a network or if there is some other type of authentication.
    
    Attributes
    ----------
        CaptivePortalURL: The URL/IP of the Captive Portal if present
        PortalResult: Boolean, True if a captive portal is found that matches the files choice to possibly mandate HTTPS
        
    """
    def __init__(self,  URL: str, HTTPSonlyswitch: bool = False, loggingSwitch: bool = True) -> None: 
        with open ('logging.yml', 'r') as file:
            logging.config.dictConfig(yaml.safe_load(file))
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
        if (self.resultcode >= 300 and self.resultcode < 400) or self.resultcode == 511:
            secondURL=firstquery.headers.get('Location')
            if self.httpsSwitch == True and secondURL.startswith('https://'):
                self.CaptivePortalURL=str(secondURL)
                return(True)
            elif self.httpsSwitch == False:
                self.CaptivePortalURL=str(secondURL)
                return(True)
            else:
                return(False)
            
        else: 
            return(False)
        
n=CaptiveDetector('http://ping.archlinux.org', False)
print(n.resultcode)