from __future__ import annotations
#Parses TOML files into digestible python variables and objects
from Captr.TOMLRead import TOMLRead
from typing import Optional, NamedTuple, Any, Type, TypeVar, IO, cast


class Action(NamedTuple):
    """
    A data structure representing an action to be performed in Login Files Used by TOMLparser, 

    Attributes
    ----------
    type : str
        The type of action (e.g., 'wait', 'text', 'click', 'move').
    id : dict, optional
        The identifiers for the action, relevant for all types except 'wait'.
    value : dict, optional
        The values associated with the action, used for all wait and text actions.
        Including Keyring Activation and Storage type. 
    """
    #type of action
    type: str
    #value is not used by wait actions
    id: Optional[dict | None] = None  
    #value is only used by text actions
    value: Optional[dict | None] = None

class LoginParser():
    """
    TOML file parser that translates the content of a login-file into a easily digestible NamedTuple 
    This parser is specifically designed to interpret TOML files used for configuration into actionable objects based on the  
    'NETWORK' and 'ACTION' fields as meets our specification in the readme. 

    - Validates and processes various types of actions ('wait', 'text', 'click', 'move') as defined in the TOML file. (see EXAMPLE.toml)

    Attributes
    ----------
    filepath : str
        The file path of the TOML file to be parsed. Needs to be set during instantiation
    ingest : NamedTuple
        Refrences and starts the process of ingesting the given file
    export : NamedTuple
        Saved version of the result from the last time running the ingest. 

    Methods
    -------
    tomlparse() -> Ingest(named Tuple)
        Parses the TOML file, validates its structure, and creates a tuple containing network details
        and a list of Actions based on the 'ACTION' section of the TOML Login file.
    changeconfigfile(filepath: str)
        Updates the filepath of the TOML file to parse and re-invokes parsing.
    ingest():
        returns the ingested TOML datastructure. 

    Possible Raises
    ------
    ValueError
        If the TOML file does not contain proper Login-File formatting. 
    TOMLDecodeError 
        If the TOML file has invalid TOML formatting (not to be confused with login formatting)
    FileNotFoundError
        If the File given does not exist or cannot be found.
    UnicodeDecodeError
        If the File given is badly corrupted or the wrong filetype. 

    Examples
    --------
    >>> parser = tomlparser("login.toml")
    >>> parser.export
    Prints parsed data from the 'login.toml' file.
    """

 
    class Ingest(NamedTuple):
        """
        Subclass of TOMLparser that defines a NamedTuple which is used for returning the value of the class
        """
        Actions: list[Action] #forward reference
        SSID: Optional[Optional[dict | None]] = None 
        URL: Optional[ str | None] = None  
        MAC: Optional[ str | None] = None
        EnforceHTTPS: Optional[ bool ] = False
        



    def __init__(self, filepath: IO[bytes] | str) -> None:
        """
        Constructs a LoginParser object that parses the given input.

        Arguments:
        - filepath: Either a string that points to a TOML file or a Python file-like
          such as what you can get from calling open(foo, "rb") or io.BytesIO().
        """
        self.filepath: IO[bytes] | str
        if type(filepath) == str:
            # Read the file from disk.
            self.filepath = cast(str, filepath)
        else:
            self.filepath = cast(IO[bytes], filepath)    
        self.export: LoginParser.Ingest
        self.ingest = self._loginparse()
    
    def __str__(self) -> str:
       return(
        f"the Network Portion of the file is a dictionary containing the following: \n {self.ingest[0]} \n" 
        f"the Actions listed in the file are as follows: \n {self.ingest[1]}"
       )
         
    def __repr__(self) -> str:
        return(
        f"Network:{self.ingest[0]}, Actions{self.ingest[1]}"
        )



    #defines the new type of object that we will be setting every instance of ACTION to\    
    class _var_test(): 
        """
        helper class used internally by tomlparseer to validate and process the actions specified in the toml file
        """
        def __init__(self) -> None:
            """
            contains the crucial and valid expressions for each action type in the TOML file used as a refrence for errors
            """
            #allowed Identification values that are compatable with every action type
            self.t_identify_all=["x-path", "id", "name", "type"]
            #extra allwed ID value for move
            self.t_identify_move=self.t_identify_all+["href"]
                #valid set values for text
            self.t_choice_text=["value", "keyring"]
            self

        #identifies the key type being used as well as if there is only 1 of them.
        def identifytest(self, action: dict, method: list) -> str:
            numberOfId=sum(int(key in action.keys()) for key in method)
            if 1 < numberOfId:
                raise ValueError("You can only supply one identifier for this action type")
            elif 1 > numberOfId: 
                raise ValueError("you need to supply some form of identifier for this action type")
            keytype=[str(TheKey) for TheKey in action if TheKey in method]
            return(keytype[0])
        
        def waittest(self, action: dict) -> str:
            #needs to be string to fit in with action object
            if len(action) > 2 and "wait" in action.keys():
                raise ValueError("Wait actions only accept wait=time as an argument")
            return(action["wait"])
    
        def clicktest(self, action: dict) -> str:
            #tells us if there is an invalid combination of values 
            return(self.identifytest(action, self.t_identify_all))

        def texttest(self, action: dict) -> tuple:
            temp=sum(int(key in action.keys()) for key in self.t_choice_text)
            valuetype=None
            #Its valid to not include any text choice, in this situation we will prompt them OTF
            if 1 < temp:
                raise ValueError("You cannot use multiple methods of defining value for a text field")
            #in case they include a value aka mode for the password
            #NOTE: could be implemented better right now its doing unnecessary compute
            elif 1 == temp:
                valuetype=[str(TheKey) for TheKey in action if TheKey in self.t_choice_text][0]
            #idtype, valuetype
            return(self.identifytest(action, self.t_identify_all), valuetype)
            
        def movetest(self, action: dict) -> str:
            return(self.identifytest(action, self.t_identify_move))
        
    #parses the toml from a file
    def _loginparse(self) -> tuple:
        """
        Internal Method used to orchestrate the parsing of the login file.
        """
        #Valid Parent Keys for the toml
        vParent=['NETWORK', 'ACTION']
        #reads from a toml file
        tml=TOMLRead(self.filepath)
        #checks if the TOML file contains the two main Dictionaries 
        if all(x in vParent for x in tml):
            net=tml['NETWORK']
            cast(dict, net)
            actions=tml['ACTION']
            place=0 #tracks the place
            toDo=[]
            mac=None
            url=None
            https=False
            ssid=None
            
            v=self._var_test()
            for options in net:
                try: 
                    match str(options):
                        case 'SSID':
                            ssid=net[options]
                        case 'URL':
                            url=net[options]
                        case 'MAC':
                            mac=net[options]
                        case 'EnforceHTTPS':
                            https=bool(net[options])
                        case _:
                            raise ValueError(f"invalid option in network")
                except ValueError:
                    raise ValueError("One of your steps contains a value of the wrong type \n e.g a boolean instead of a string")
            # parses the actions and puts the values into action objects
            for action in actions:
                place+=1
                try:
                    match action["action"]:
                        case 'wait':
                            wait=v.waittest(action)
                            #creates action object, because its type wait cannot have an id-type 
                            toDo.append(Action(type='wait', value={'wait' : wait}))
                        case 'text':
                            tp=v.texttest(action)
                            idtype=tp[0]
                            valuetype=tp[1]
                            #creates action object and adds it to the list, The value can be None, when the user wants to be prompted for the password
                            toDo.append(Action('text', {idtype : action[idtype]}, value={valuetype : action[valuetype]} if valuetype!=None else None))
                        case 'click':
                            idtype=v.clicktest(action)
                            #creates action object and adds it to the list
                            toDo.append(Action('click', {idtype : action[idtype]}))
                        case 'move':
                            idtype=v.movetest(action)
                            #creates action object and adds it to the list
                            toDo.append(Action('move', {idtype : action[idtype]}))
                        case _:
                            raise ValueError(f"missing And/or invalid action in action#{place}")
                except KeyError:
                    raise KeyError("One of your steps is missing a action")
            self.export=self.Ingest(URL=url, EnforceHTTPS=https, MAC=mac, SSID=ssid, Actions=toDo)
            return self.export 
        else:
            raise ValueError("Error, your either missing NETWORK or ACTION from your LoginFile")
        
    def changeconfigfile(self,filepath: str="") -> None:
        """
        Changes the path of the set config file to the new path supplied AND parses it
        """
        self.filepath=filepath
        self.ingest=self._loginparse()

    def result(self) -> object:
        '''
        returns the ingested data. 
        '''
        return self.export

v=LoginParser(r"EXAMPLE.toml")
print(v.result())

