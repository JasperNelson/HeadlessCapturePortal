import keyring as ky #handles keyrings for us.
from keyring.backends import Windows, SecretService, kwallet, macOS, libsecret 
import bitwarden_keyring #bitwarden backend for keyring
import re #regex module 
from typing import cast
from getpass import getpass as gp
from dataclasses import dataclass #module for dataclasses
from colorama import init, Fore


class KeyManager():
  keyring_backends={ #list of supported keyring backends
  "secretservice":SecretService.Keyring, #for both Kwallet on KDE and libsecret in GNOME
  "kwallet":kwallet.DBusKeyring, #for Kwallet on KDE
  "windows":Windows.WinVaultKeyring, #for Windows Vault keys
  "macos":macOS.Keyring, #for MacOS keys
  "libsecret":libsecret.Keyring, #for GNOME on linux
  "bitwarden":bitwarden_keyring #for Bitwarden
  }

  def __init__(self, URL: str, username: str, keyringBackend: str):
    init(autoreset=False)
    if keyringBackend != None: #if none it means the user is going with the default keyring selection
      try:
        self.userKeyringBackend=keyringBackend
        self.keyringBackend=self.keyring_backends[keyringBackend]
        ky.set_keyring(self.keyringBackend()) #manual keyring backend selection
      except KeyError:
        error=f"The backend specified for your keyring ({keyringBackend}) is not a valid or supported backend string"
        raise KeyError(error) #wrong value for the service
    self.URL=URL
    self.username=username
    
    
  #checks if the key exists in the Users keyring
  def _key_exists(self) ->bool:
    try:
      if None == (ky.get_password(f"HLessCapturePortal_{self.URL}", self.username)):
          return(False)
      return(True)
    except NameError: 
       error=f"The backend specified for your keyring ({self.userKeyringBackend}) is not accessible or installed"
       raise NameError(error) 
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
  def key_access(self)->str:
    if self._key_exists():
      #Can never return None given the configuration
      return cast(str, ky.get_password(f"HLessCapturePortal_{self.URL}", self.username))
    else:
      return cast(str, self._key_add())


#example implementation
x= KeyManager(URL="https://example.com",username="jhasdlltest", keyringBackend="windows")
print(x.key_access())
