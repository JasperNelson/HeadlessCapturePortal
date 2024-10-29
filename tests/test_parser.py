import pytest
from tomllib import TOMLDecodeError
from Captr.LoginParser import LoginParser

#checks to see if the fuctionality of the class is intact
print(((LoginParser(r"./Examplelogins/EXAMPLE.toml")).export))
assert(str((LoginParser(r"./Examplelogins/EXAMPLE.toml")).export) == "_ingest(Actions=[Action(type='click', id={'id': 'example'}, content=None, wait=None, Print=None), Action(type='click', id={'contains': 'garply thud'}, content=None, wait=None, Print=None), Action(type='click', id={'name': 'examplename'}, content=None, wait=None, Print=None), Action(type='click', id={'type': 'checkbox'}, content=None, wait=None, Print=None), Action(type='click', id={'xpath': 'xpathere'}, content=None, wait=None, Print=None), Action(type='wait', id=None, content=None, wait=30, Print=None), Action(type='text', id={'name': 'exname'}, content=None, wait=None, Print=None), Action(type='text', id={'xpath': 'xpath'}, content={'value': 'examplestringEGUserName'}, wait=None, Print=None), Action(type='text', id={'xpath': 'xpath'}, content={'keyring': 'YourUserName'}, wait=None, Print=None), Action(type='move', id={'href': 'href_url'}, content=None, wait=None, Print=None), Action(type='move', id={'id': 'ID'}, content=None, wait=None, Print=None)], URL='example.com', Backend='Debug')")
# assert(repr(TOMLparser(r"EXAMPLE.toml"))=="Network:{'SSID': 'examplewifi', 'URL': 'https://example.com', 'IP': '1.0.0.1'}, Actions[Action(type='click', id={'id': 'example'}, value=None), Action(type='click', id={'x-path': '/html/body/div/div/main/div/p[81]'}, value=None), Action(type='click', id={'name': 'examplename'}, value=None), Action(type='click', id={'type': 'checkbox'}, value=None), Action(type='wait', id=None, value={'wait': 30}), Action(type='text', id={'name': 'name'}, value=None), Action(type='text', id={'name': 'name'}, value={'value': 'examplestringEGUserName'}), Action(type='text', id={'name': 'password'}, value={'keyring': ['YourUserName']}), Action(type='move', id={'href': 'href_url'}, value=None), Action(type='move', id={'id': 'ID'}, value=None)]")
# assert(str(TOMLparser(r"EXAMPLE.toml").export)=="Ingest(Network={'SSID': 'examplewifi', 'URL': 'https://example.com', 'IP': '1.0.0.1'}, Actions=[Action(type='click', id={'id': 'example'}, value=None), Action(type='click', id={'x-path': '/html/body/div/div/main/div/p[81]'}, value=None), Action(type='click', id={'name': 'examplename'}, value=None), Action(type='click', id={'type': 'checkbox'}, value=None), Action(type='wait', id=None, value={'wait': 30}), Action(type='text', id={'name': 'name'}, value=None), Action(type='text', id={'name': 'name'}, value={'value': 'examplestringEGUserName'}), Action(type='text', id={'name': 'password'}, value={'keyring': ['YourUserName']}), Action(type='move', id={'href': 'href_url'}, value=None), Action(type='move', id={'id': 'ID'}, value=None)])")


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
