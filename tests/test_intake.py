from Captr.main import Intake
import argparse
import pytest
    
def test_auto() -> None:
    result=Intake(["--Auto"])
    print(result)
    assert(result.Auto=="")

