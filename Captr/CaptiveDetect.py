from __future__ import annotations
import requests as rq
import logging


class CaptiveNotImplemented(Exception):
    """Raised when there isnt a captive portal detected"""
    pass


class CaptiveDetector:
    """
    Class to be used to detect if a captive portal is present in a network or if there is some other type of'
     ' authentication.
    
    Key Attributes:
    ----------
        CaptivePortalURL: The URL/IP of the Captive Portal if present
        
    """
    def __init__(self) -> None: 
        self.logger = logging.getLogger(__name__)
        self._session = rq.Session()
        self._session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like '
                                      'Gecko) Chrome/104.0.0.0 Safari/537.36'})
        self.resultcode: int
        self.CaptivePortalURL: str   
        self.PortalDetect()
      
    def PortalDetect(self) -> None:
        """
        Method that returns a true or false depending on if a method exists or not as well as checks if the captive 
        portal page is https
        """
        firstquery = self._session.head("http://ping.archlinux.org")
        self.resultcode = int(firstquery.status_code)
        self.logger.debug(f"resultcode={self.resultcode}")
        #these status codes would indicate the potential presence of a captive portal.
        if (self.resultcode >= 300 and self.resultcode < 400):  #deals with 3XX redirect captive portals
            secondURL = firstquery.headers.get('Location')
        #checking that there was a location in the location portion of the header. 
            if isinstance(secondURL, str):
                self.logger.debug(f"Captiveportaltest url={secondURL}")
                self.CaptivePortalURL = str(secondURL)
            else:  #TODO: Better define this exception something really weird occured if this is triggered
                raise CaptiveNotImplemented('There seems to be a unsupported redirect')
        elif self.resultcode == 511:  #deals with 511 type captive portals
            # TODO: figure out how to implement this
            raise NotImplementedError("Sorry, Currently we dont support 511 captive portals but its on our roadmap!")
        else: 
            raise CaptiveNotImplemented("The network doesnt appear to be under a captive portal")
        
#n=CaptiveDetector('http://ping.archlinux.org', False)
#print(n.resultcode)
