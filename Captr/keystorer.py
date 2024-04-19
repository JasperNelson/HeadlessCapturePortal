import keyring as ky #handles keyrings for us.
import re #regex module 
from getpass import getpass as gp
from dataclasses import dataclass #module for dataclasses


class key_manager():
  def __init__(self, URL: str, username: str):
    self.URL=URL
    self.username=username
  #checks if the key exists in the Users keyring
  def _key_exists(self) ->bool:
    if None == (ky.get_password(f"AutoCapturePortal_{self.URL}", self.username)):
        return(False)
    return(True)
  
  #temporary prompt to ask the user for their password
  def _tmp_prompt(self) ->str:
    while(True):
      first=gp(prompt="\nPlease give us the password to store in the keyring:\n")
      second=gp(prompt="\nOne More Time:\n")
      if first != second:
        print("The passwords dont match please try again")
      else:
        return(first)
    
  #adds a key to the keyring
  def key_add(self):
     psword=self._tmp_prompt()
     ky.set_password(f"AutoCapturePortal_{self.URL}", self.username, psword)

x= key_manager(URL="https://example.com",username="jhasdlltest")
x.key_add()
