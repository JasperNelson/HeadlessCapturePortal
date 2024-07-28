#argument parsing
import argparse
from typing import Type
from Captr.ConfigParser import Config
from Captr.Orchestrator import Orchestrator
from typing import Optional, List
import os
from Captr.LoggingRead import readLoggingConfig


#This goes into the help page

def Intake(pargs: Optional[List[str]] = None) -> argparse.Namespace:
    #in general flags that start with a capital letter change the purpose of the program and cannot be combined with other capitilized flags.
    argparser=argparse.ArgumentParser(
        prog="Capture",
        add_help=True,
        description="A cross platform tool for logging into captive portals headlessly, as well as automation.",
        epilog="Made with love by Jasper with the help of Uche and others"
        )
    mode=argparser.add_argument_group('MODE:', 'Changes the Mode/Function of the program')
    modeX=mode.add_mutually_exclusive_group()
    #Verbose Mode
    argparser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Verbose flag that will output the logs to the shell that the program was called from" 
        "Wont work if logging is disabled in the config"
        )
    argparser.add_argument(
        'default',
        nargs="?",
        type=str,
        help="Verbose flag that will output the logs to the shell that the program was called from" 
        "Wont work if logging is disabled in the config"
        )
    #Return HTML of url
    modeX.add_argument(
        '-L', '--Layout',
        nargs=1,
        type=str,
        help="Flag that will return the html layout of a given url or webpage"
        )

    #Detect Capture Portal Presence/URL
    modeX.add_argument(
        '-U', '--URL',
        action='store_true',
        help="Flag that will return the URL of a capture portal for the current network if it exists."
        )

    #Reset Credentials
    modeX.add_argument(
        '-R', '--Remove', 
        nargs=1,
        type=str,
        help="Flag that will remove the keys from the respective keyring associated with the given login file"
        )

    #Automatic Mode
    modeX.add_argument(
        '-A', '--Auto',
        nargs='?',
        type=str,
        default="",
        help="If specified will automatically search through your login files stored in the login directory specified in your config file and log you in"
        "into a network that matches the URL \n and(if specified) the SSID of the login file to the current network"
        )
    #safety prompt override
    argparser.add_argument(
        '-y', '--yes',
        action='store_true',
        help="for use wit h -A/--Auto, will stop asking to use a config file to log into a network"    
        )
    args= argparser.parse_args() if pargs is None else argparser.parse_args(pargs)
    return args
    #ROADMAPPED: Not yet implemented: 
    # argparser.add_argument('-G', '--Guided', help="Flag that will try to guide the user through a login session with choices and everything")
# Use this when logging into the network
ToUse=Intake(["--Auto"])
#print(vars(ToUse))
readLoggingConfig()
#logging.basicConfig(filename='myapp.log', level=logging.INFO)
Orchestrator(ToUse)
# conf=Config(filepath=str(os.environ["HOME"]+"/.LoginFiles")) #Would have been created during the initial setup
