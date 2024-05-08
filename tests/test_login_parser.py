from io import BytesIO
from typing import IO, cast
import sys 
from Captr.TOMLRead import TOMLRead
from ..Captr.LoginParser import LoginParser, Action

def test_toml_read() -> None:
    # Given
    bytesFile: IO[bytes] = BytesIO(b"""
        [NETWORK]
        foo = 1
        [[ACTION]]
        bar = 1
    """)

    # When
    toml = TOMLRead(bytesFile)
    
    # Then
    keys = [k for k in toml.keys()]
    print(f"keys={keys}")
    assert(list(keys) == ['NETWORK', 'ACTION'])


def test_login_parser() -> None:
    # Given
    bytesFile: IO[bytes] = BytesIO(b"""
[NETWORK]
SSID="examplewifi" 
URL="https://example.com" #IMPORTANT: Additionally this is (needed for keyring functionality)
IP="1.0.0.1"

[[ACTION]]
action="click"
x-path="/html/body/div[id=login]"
""")
    
    # When
    export = LoginParser(bytesFile).export

    
    # Then
    assert(export.Network["SSID"] == "examplewifi")
    assert(export.Network["URL"] == "https://example.com")
    assert(export.Network["IP"] == "1.0.0.1")
    assert(len(export.Actions) == 1)
    if export.Actions[0].id is not None:
        assert(len(export.Actions[0].id.keys()) == 1)
        assert(export.Actions[0].id["x-path"] == "/html/body/div[id=login]")