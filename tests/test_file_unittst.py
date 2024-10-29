# mypy: allow-untyped-defs
import sys
from Captr import main


def test_Playwright(monkeypatch, capsys) -> None:
    with monkeypatch.context() as m: 
        m.setattr(sys, "argv", [sys.argv[0], './Examplelogins/TestingFile.toml', "-i", "http://127.0.0.1:5000"])
        main.main()
        print(str(capsys.readouterr().out))
        assert ("Success" in str(capsys.readouterr().out))
        