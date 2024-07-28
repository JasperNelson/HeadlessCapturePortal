#orchestrates the project
import argparse
import os
from tomllib import TOMLDecodeError
#from Captr.logging import logging
from Captr.ConfigParser import Config
from Captr.LoginParser import LoginParser, Action
from Captr.backend import backend
from Captr.Debackend import DebugBackend
from Captr.SimpleBackend import SimpleBackend
import logging
from Captr.keystorer import KeyManager
from Captr.CaptiveDetect import CaptiveDetector, CaptiveNotImplemented
from typing import NamedTuple


class Orchestrator(): 
    def __init__(self, modes: argparse.Namespace):
        #prep
        #print(vars(modes))
        self.logger=logging.getLogger(__name__)
        self.logger.debug(f"source modes={modes}")
        self.modes=self._namespaceToModes(modes)
        self.logger.debug(f"parsed modes={self.modes}")
        self.backends={"Debug":DebugBackend, "Simple": SimpleBackend}
        self.config=Config("./CONFIG.toml")
        self.logger.debug(f"Config Vars={self.config.export}")
        #backend used unless if specified differently in a config
        self.defaultBackend=self.config.export.defaultBackend
        self.loginFilesDir=self.config.export.loginFilesDir
        self.keyringBackend = self.config.export.keyringBackend if self.config.export.keyringBackend != "" else None #will be None if "" in the config
    #     print(self.defaultBackend)
        #start parsing options and split
        self.relay()

    def _LoginDirective(self, URL: str | None = None) -> None:
        """
        Internal method in Orchestrator that actually interfaces with the backends. 
        """

    def _namespaceToModes(self, modes: argparse.Namespace) -> dict:
        """
        Internal method in Orchestrator that removes the arguments used in argparse.Namespace so they can be used 
        for later parsing. (It will remove all the options not used)
        where False = the option was not used
        """
        result: dict ={}
        #Argparse.Namespace always has the keys contained in the result regardless of if they were used or not
        #so we are going to parse if they were used or not.
        option=False 
        if modes.verbose is not False:
            result["verbose"]=modes.verbose 
        if modes.Remove is not None:
            result["Remove"]=modes.Remove  
        if modes.URL is not False:
            result["URL"]=modes.URL  
        if modes.Layout is not None:
            result["Layout"]=modes.Layout 
        if modes.Auto != '':
            result["Auto"]=modes.Auto  
        if modes.yes is not False:
            result["yes"]=modes.yes  
        if modes.default is not None:
            result["default"]=modes.default 
        if len(result.keys())==0:
            self.logger.critical(f"You must supply a toml file if you want to continue the default arguments")
            raise Exception
        return result


    def Dispatch(self, login: LoginParser._ingest, CaptiveURL: str) ->None:
        """
        internal method of Orchestrator, used to dispatch to a backend
        """

        backend=self._backendBuilder(login.Backend) #activate and locate the proper backend
        if not CaptiveURL.startswith(str(login.URL)): #checks if the supplied starting string is the same
            self.logger.info(f"Captive Portal {CaptiveURL} doesnt start with {login.URL} skipping ...") 
            raise(CaptiveNotImplemented)
        else:
            try:
                ## Backend Initial Setup >>>
                backend.Start(CaptiveURL) #used in session based backends other backends can just pass on the output
                self.logger.debug(f"sending [{CaptiveURL}] Starting action to backend [{backend.__class__.__name__}]")
                ## Backend actions >>>
                for Act in login.Actions:
                    match Act.type:
                        case "click":
                            self.logger.debug(f"sending [{Act.type}] action to backend [{backend.__class__.__name__}]")
                            assert(isinstance(Act.id, dict))
                            backend.Click(Act.id)
                        case "wait":
                            self.logger.debug(f"sending [{Act.type}] action to backend [{backend.__class__.__name__}]")
                            if Act.wait is not None:
                                backend.Wait(Act.wait)
                            else: 
                                self.logger.critical("An Unexpected Error Occured Please report this!!! CODE: 2")
                        case "text":
                            # self.logger.debug(f"sending [{Act.type}] action to backend [{backend.__class__.__name__}]")
                            # self.logger.debug(f"Act.id={Act.id}"+f"\nAct.content={Act.content}")

                            assert(isinstance(Act.id, dict)) 
                            if Act.content is None:
                                content=input(f"please provide the text to input into text for the corresponding value: {Act.id}") 
                                self.logger.debug(f"sending [{Act.type}] action to backend [{backend.__class__.__name__}]")
                                backend.Text(Act.id, str(content)) #need to parse and see if its a thing
                            elif 'keyring' in Act.content and login.URL is not None:
                                logging.debug(f"sending {login.URL, Act.content['keyring'], self.keyringBackend} to keymanager")
                                x=KeyManager(login.URL, Act.content['keyring'], self.keyringBackend)
                                self.logger.debug(f"sending [{Act.type}] action to backend [{backend.__class__.__name__}]")
                                backend.Text(Act.id, x.key_access())
                            elif 'keyring' in Act.content:
                                self.logger.critical("To use a Keyring you must specify a URL")
                                raise ValueError
                            elif 'value' in Act.content:
                                self.logger.debug(f"sending [{Act.type}] action to backend [{backend.__class__.__name__}]")
                                backend.Text(Act.id, str(Act.content['value'])) #need to parse and see if its a thing
                        case "move":
                            self.logger.debug(f"sending [{Act.type}] action to backend [{backend.__class__.__name__}]")
                            assert(isinstance(Act.id, dict))
                            backend.Move(Act.id)
                        case _:
                            self.logger.critical("An Unexpected Error Occured Please report this!!! CODE: 1") #should never reach this critical error occurs if it does somehow
                            raise Exception
            except AssertionError as AE:
                self.logger.critical("An Unexpected error occured CODE: 3", AE) 
                        
            
    def _findURL(self) -> str:
        """
        internal method of Orchestrator, used to query if a CaptivePortal exists in the current network, if none is detected we will error out and exit the program

        """
        test: CaptiveDetector
        try:
            test=CaptiveDetector()
        except CaptiveNotImplemented as cni:
            self.logger.info(cni)
            exit() #since there is no Captive portal there is nothing to do
        captiveURL=test.CaptivePortalURL
        #Returns a captive portal url to the terminal
        logging.debug(f"CaptivePortalURL is {captiveURL}")
        return(captiveURL)
        
    def _backendCheck(self, name: str) -> None:
            """
            internal method of Orchestrator, used exclusively by backendBuilder
            to see if the supplied backend is a backend listed in compatable backends
            """
            if name not in self.backends.keys():
                raise ValueError(f"Bad backend: '{name}'")
        
    def _backendBuilder(self, backendOverride : None | str = None) -> backend:
        """
        internal method of Orchestrator, returns a useable backend object
        """
        #the flag used to identify the backend
        bFlag: str
        #the backend object
        backedobj: backend
        if backendOverride is not None:
            bFlag=backendOverride
        else: bFlag=self.defaultBackend
        self._backendCheck(bFlag)
        backedobj=self.backends[bFlag]()
        
       # print(backedobj)
        return backedobj
    
    def _Reader(self, filepath: str) -> LoginParser._ingest:
        """
        Internal method of Orchestrator, 
        Purpose: to take a filepath and use LoginParse to return a LoginParser._ingest NamedTuple
        """
        parsedOb=LoginParser(filepath)
        ingest=parsedOb.export
        assert isinstance(ingest, LoginParser._ingest)
        return(ingest)
    
    def _Remove(self) -> None:
        #TODO: Doesnt use a backend as it uses keystorer instead
        pass


    def _Auto(self, path: str) -> None:
        self.logger.debug(f"Started Parsing In Automatic Mode")
        if not os.path.exists(path):
            raise OSError(f"Error, The path [{path}] is invalid, or permissions dont permit access")
        #try to filter out some of the junk that may inevitably enter the directory
        loginfiles=(loginfiles for loginfiles in os.listdir(path) if loginfiles.endswith(".toml")) 
        
        #Test for the presence of a Captive Portal and return its url if present
        captiveURL=self._findURL()

        
        for lFile in loginfiles:
            try: #sent to multipledispatch for further parsing and dispatching to backends
                self.Dispatch(self._Reader(path+"/"+lFile), captiveURL)
            except TOMLDecodeError as de:
                self.logger.warn(f"The file {lFile} has a invalid toml format \n skipping ...")
            except UnicodeDecodeError as ude:
                self.logger.warn(f"The file {lFile} appears to be corrupted \n skipping ...")
            except ValueError as ve:
                self.logger.warn(f"Something was wrong with the formatting of the toml file {lFile}, Error = {ve} \n skipping ...")
            except PermissionError as pe:
                self.logger.warn(f"Permissions do not allow reading the file {lFile} \n skipping ...")
            except Exception as e: 
                self.logger.error(f"Unknown error: {str(e)} \n skipping ...")
            #next design a function that relegates actions etc. #and one that reads the url and compares it to the captive portal url
        if len(list(loginfiles))==0:
            self.logger.error(f"The directory to search for login files doesn't contain any login files Exiting. . .")



    def _URL(self) -> None:
        x=self._findURL()
        logging.debug(f"CaptivePortalURL is {x}")
        print(x)

    def _Layout(self, layout: str) -> None:
        back=self._backendBuilder()
        #needs to be supplied a url 
        back.Layout_Fetch(layout)

    def _default(self) -> None:
        filepath=self.modes["default"]
        captiveURL=self._findURL()
        try:
            session=LoginParser(filepath)
        except OSError:
            raise OSError(f"Error, the filepath is invalid or permissions dont permit read access")
        self._backendBuilder()
        self.Dispatch(self._Reader(filepath), captiveURL)
    
    def relay(self) -> None:
        """
        Function of orchestrator that parses arguments and activates the appropriate member functions. 

        Arguments: 
        None
        """
        #temp for testing
        print("reached")
        if "verbose" in self.modes:
            pass
        if "Remove" in self.modes:
            self._Remove()
        elif "Auto" in self.modes:
            if self.modes["Auto"] is None:
                self._Auto(self.loginFilesDir)
            else: #If there was a directory redirect supplied
                self._Auto(self.modes["Auto"])
        elif "URL" in self.modes:
            self._URL()
        elif "Layout" in self.modes:
            self._Layout(self.modes["Layout"])
        else:
            self._default()
       

