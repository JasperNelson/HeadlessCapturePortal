from io import BytesIO
from typing import IO
from Captr.TOMLRead import TOMLRead
from Captr.LoginParser import LoginParser


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
    assert (list(keys) == ['NETWORK', 'ACTION'])


def test_login_parser() -> None:
    # Given
    bytesFile: IO[bytes] = BytesIO(b"""
[NETWORK]
URL="https://example.com" #IMPORTANT: Additionally this is (needed for keyring functionality)
                                   
[[ACTION]]
action="click"
xpath="/html/body/div[id=login]"
""")
    
    # When
    export = LoginParser(bytesFile).export

    # Then
    assert (export.URL == "https://example.com")
    assert (len(export.Actions) == 1)
    if export.Actions[0].id is not None:
        assert (len(export.Actions[0].id.keys()) == 1)
        assert (export.Actions[0].id["xpath"] == "/html/body/div[id=login]")
