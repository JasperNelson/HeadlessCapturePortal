import keyring as ky #handles keyrings for us.
from keyring.backends import Windows, SecretService, kwallet, macOS, libsecret 
import bitwarden_keyring #bitwarden backend for keyring
import re #regex module 
from getpass import getpass as gp
from dataclasses import dataclass #module for dataclasses
from colorama import init, Fore, Back, Style


class key_manager():
  keyring_backends={ #list of supported keyring backends
  "secretservice":SecretService.Keyring, #for both Kwallet on KDE and libsecret in GNOME
  "kwallet":kwallet.DBusKeyring, #for Kwallet on KDE
  "windows":Windows.WinVaultKeyring, #for Windows Vault keys
  "macos":macOS.Keyring, #for MacOS keys
  "libsecret":libsecret.Keyring, #for GNOME on linux
  "bitwarden":bitwarden_keyring #for Bitwarden
  }
  def __init__(self, URL: str, username: str, keyringService: str):
    init(autoreset=False)
    if keyringService != None: #if none it means the user is going with the default keyring selection
      try:
        self.keyringService=self.keyring_backends[keyringService]
        ky.set_keyring(self.keyringService()) #manual keyring backend selection
      except KeyError:
        print(Fore.RED+f"The backend specified for your keyring ({keyringService}) is not a valid or supported backend string")
        raise ValueError 
    self.URL=URL
    self.username=username
    
    
  #checks if the key exists in the Users keyring
  def _key_exists(self) ->bool:
    if None == (ky.get_password(f"HLessCapturePortal_{self.URL}", self.username)):
        return(False)
    return(True)
  
  #temporary prompt to ask the user for their password
  def _tmp_prompt(self) ->str:
    while(True):
      first=gp(prompt=Fore.GREEN+"\n ---- Please give us the password to store in the keyring:\n")
      second=gp(prompt=Fore.GREEN+"\n ---- One More Time:\n")
      if first != second:
        print("The passwords dont match please try again")
      else:
        return(first)
    
  #adds a key to the keyring
  def _key_add(self) ->str:
     psword=self._tmp_prompt()
     ky.set_password(f"HLessCapturePortal_{self.URL}", self.username, psword)
     if None==ky.get_password(f"HLessCapturePortal_{self.URL}", self.username): #Warning for the user if the keyring did not save the key
       print(Fore.YELLOW+"Warning: Something is wrong with your keyring, the password wasnt properly saved")
     return psword

  #access the keyring if they exist
  def key_access(self):
    if self._key_exists():
      return (ky.get_password(f"HLessCapturePortal_{self.URL}", self.username))
    else:
      return(self._key_add())

x= key_manager(URL="https://example.com",username="jhasdlltest", keyringService="secretservice")
print(x.key_access())
