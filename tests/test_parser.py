import pytest
from tomllib import TOMLDecodeError
from Captr.LoginParser import LoginParser

#checks to see if the fuctionality of the class is intact
print(((LoginParser(r"./Examplelogins/EXAMPLE.toml")).export))
assert(str((LoginParser(r"./Examplelogins/EXAMPLE.toml")).export) == "_ingest(Actions=[Action(type='click', id={'id': 'example'}, content=None, wait=None, Print=None), Action(type='click', id={'contains': 'garply thud'}, content=None, wait=None, Print=None), Action(type='click', id={'name': 'examplename'}, content=None, wait=None, Print=None), Action(type='click', id={'type': 'checkbox'}, content=None, wait=None, Print=None), Action(type='click', id={'xpath': 'xpathere'}, content=None, wait=None, Print=None), Action(type='wait', id=None, content=None, wait=30, Print=None), Action(type='text', id={'name': 'exname'}, content=None, wait=None, Print=None), Action(type='text', id={'xpath': 'xpath'}, content={'value': 'examplestringEGUserName'}, wait=None, Print=None), Action(type='text', id={'xpath': 'xpath'}, content={'keyring': 'YourUserName'}, wait=None, Print=None), Action(type='move', id={'href': 'href_url'}, content=None, wait=None, Print=None), Action(type='move', id={'id': 'ID'}, content=None, wait=None, Print=None)], URL='example.com', Backend='Debug')")

#tests to see if the error checking is workin
def test_Bad_Login_Files() -> None:
    with pytest.raises(UnicodeDecodeError):
        LoginParser(r"./TestingFiles/CORRUPTED_TOML")
    with pytest.raises(ValueError):
        LoginParser(r"./TestingFiles/BADLOGIN.toml")
    with pytest.raises(KeyError):
        LoginParser(r"./TestingFiles/BADLOGIN_2.toml")
    with pytest.raises(ValueError):
        LoginParser(r"./TestingFiles/BADLOGIN_3.toml")
    with pytest.raises(TOMLDecodeError):
        LoginParser(r"./TestingFiles/BAD_TOML.toml")
