#argument parsing
import argparse
from typing import Type
from Captr.ConfigParser import Config
import os


#This goes into the help page

def Intake() -> argparse.Namespace:
    #in general flags that start with a capital letter change the purpose of the program and cannot be combined with other capitilized flags.
    argparser=argparse.ArgumentParser(
        prog="Capture",
        add_help=True,
        description="A cross platform tool for logging into captive portals headlessly, as well as automation.",
        epilog="Made with love by Jasper, Daniella, and Brandon"
        )

    #Verbose Mode
    argparser.add_argument(
        '-v', '--Verbose',
        action='store_true',
        help="Verbose flag that will output the logs to the shell that the program was called from" 
        "Wont work if logging is disabled in the config"
        )

    #Return HTML of url
    argparser.add_argument(
        '-L', '--Layout',
        nargs=1,
        type=str,
        help="Flag that will return the html layout of a given url or webpage"
        )

    #Detect Capture Portal Presence/URL
    argparser.add_argument(
        '-U', '--URL',
        action='store_true',
        help="Flag that will return the URL of a capture portal for the current network if it exists."
        )

    #Reset Credentials
    argparser.add_argument(
        '-R', '--Remove', 
        nargs=1,
        type=str,
        help="Flag that will remove the keys from the respective keyring associated with the given login file"
        )

    #Automatic Mode
    argparser.add_argument(
        '-A', '--Auto',
        action='store_true',
        help="If specified will automatically search through your login files stored in the login directory specified in your config file and log you in"
        "into a network that matches the URL \n and(if specified) the SSID of the login file to the current network"
        )

    #safety prompt override
    argparser.add_argument(
        '-y', '--Yes',
        action='store_true',
        help="for use with -A/--Auto, will stop asking to use a config file to log into a network"    
        )
    args=argparser.parse_args()
    print(args)
    return args
    #ROADMAPPED: Not yet implemented: 
    # argparser.add_argument('-G', '--Guided', help="Flag that will try to guide the user through a login session with choices and everything")
# Use this when logging into the network
ToUse=Intake()
conf=Config(filepath=str(os.environ["HOME"]+"/.LoginFiles")) #Would have been created during the initial setup
