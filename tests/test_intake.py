from Captr.main import Intake
import argparse
import pytest
    
# def test_auto() -> None:
result=Intake(["--URL"])
print(result)
assert(result.Auto=="")

