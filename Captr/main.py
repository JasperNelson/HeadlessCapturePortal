#argument parsing
import argparse


#This goes into the help page
def helpPage():
        print("""
Capture(captr) - A cross-platform tool for managing captive portals headlessly.

USAGE:
    captr [OPTIONS]

NOTE:                       In general you cannot combine args/flags that are capitalized.          
OPTIONS:

    None                    Default behavior, specify a login file and start the attempt to login dont include the .toml 
          
    -v, --Verbose           Output the logs to the shell that the program was called from for the respective task.

    -L, --Layout            Return the HTML layout of a given URL or webpage.
                            SYNTAX: -L <url>

    -U, --URL               Return the URL of a capture portal for the current network, if it exists.
                            SYNTAX: -U

    -R, --Remove            Remove the keys from the respective keyring associated with the given login file.
                            SYNTAX: -R <LoginFileName>

    -A, --Auto              Automatically search through your login files and log you into a network that matches the URL 
                            and (if specified) the SSID of the login file to the current network.
                            SYNTAX: -A

    -y, --Yes               For use with -A/--auto, will stop asking to use a config file to log into a network.

    -h, --Help              Show this full help message and exit.

EXAMPLES:
    captr --Verbose <loginFileName>
    captr --Layout http://example.com
    captr --Remove <loginFileName>
    captr --Auto --yes
    captr -vR <loginFileName>

Made with love by Jasper, Daniella, and Brandon
        """)

#in general flags that start with a capital letter change the purpose of the program and cannot be combined with other capitilized flags.
argparser=argparse.ArgumentParser(
    prog="Capture",
    add_help=False,
    description="A cross platform tool for logging into captive portals headlessly, as well as automation.",
    epilog="Made with love by Jasper, Daniella, and Brandon"
    )

#Verbose Mode
argparser.add_argument(
    '-v', '--Verbose',
    action='store_true',
    help="Verbose flag that will output the logs to the shell that the program was called from."
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
    help="If specified will automatically search through your login files and log you"
    "into a network that matches the URL \n and(if specified) the SSID of the login file to the current network"
    )

#safety prompt override
argparser.add_argument(
    '-y', '--Yes',
    action='store_true',
    help="for use with -A/--Auto, will stop asking to use a config file to log into a network"    
    )

argparser.add_argument(
    '-h', '--Help',
    action='store_true',
    help="lists a help page",
    )   

args=argparser.parse_args()
print(args)

#Not yet implemented: 
# argparser.add_argument('-G', '--Guided', help="Flag that will try to guide the user through a login session with choices and everything")

#print(help(argparse.Action))