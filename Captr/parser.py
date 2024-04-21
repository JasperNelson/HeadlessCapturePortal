#Parses TOML files into digestible python variables and objects
import tomllib as toml
from dataclasses import dataclass
from typing import Optional, Tuple, Any, Callable
from pprint import pprint

#defines the values that can be present in a 
class toml_parser():
    """
    TOML file parser that translates the content into structured Python variables and objects.

    This parser is specifically designed to interpret TOML files used for configuration into actionable objects based on 
    'NETWORK' and 'ACTION'. 
    - Validates and processes various types of actions ('wait', 'text', 'click', 'move') as defined in the TOML file. (see EXAMPLE.toml)

    Attributes
    ----------
    filepath : str
        The file path of the TOML file to be parsed. Needs to be set during instantiation
    ingest : tuple
        Contains parsed data from the TOML file, including network configurations and a list of action objects. In the format
        (dict('NETWORK'),list(ACTION, ACTION, ACTION, ACTION))

    Methods
    -------
    tomlparse() -> tuple
        Parses the TOML file, validates its structure, and creates a tuple containing network details
        and a list of Actions based on the 'ACTION' section of the TOML file.
    changeconfigfile(filepath: str)
        Updates the filepath of the TOML file to parse and re-invokes parsing.
    ingest():
        returns the ingested TOML datastructure. 

    Raises
    ------
    ValueError
        If the TOML file does not contain the required sections or contains bad data. 

    Examples
    --------
    >>> parser = tomlparser("config.toml")
    >>> parser.print()
    Prints parsed data from the 'config.toml' file.
    """
    def __init__(self, filepath: str="") -> None:
        self.filepath = str(filepath)
        self.ingest=tuple(self._tomlparse())    

    def __str__(self) -> str:
       return(
        f"the Network Portion of the file is a dictionary containing the following: \n {self.ingest[0]} \n" 
        f"the Actions listed in the file are as follows: \n {self.ingest[1]}"
       )
         
    def __repr__(self) -> str:
        return(
        f"Network:{self.ingest[0]}, Actions{self.ingest[1]}"
        )

    #defines the new type of object that we will be setting every instance of ACTION to
   
    @dataclass
    class Action():
        """
        A data structure representing an action to be performed, parsed from the TOML file.

        Attributes
        ----------
        type : str
            The type of action (e.g., 'wait', 'text', 'click', 'move').
        id : dict, optional
            The identifiers for the action, relevant for all types except 'wait'.
        value : dict, optional
            The values associated with the action, used for all wait and text actions.
        """
        #type of action
        type: str
        #value is not used by wait actions
        id: Optional[dict] = None
        #value is only used by text actions
        value: Optional[dict] = None

    class _var_test(): 
        """
        helper class used internally by tomlparseer to validate and process the actions specified in the toml file
        """
        def __init__(self) -> None:
            """
            contains the crucial and valid expressions for the TOML file used as a refrence for errors
            """
            #allowed Identification values that are compatable with every action type
            self.t_identify_all=["x-path", "id", "name", "type"]
            #extra allwed ID value for move
            self.t_identify_move=self.t_identify_all+["href"]
                #valid set values for text
            self.t_choice_text=["value", "keyring"]

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
    def _tomlparse(self) -> tuple:
        """
        Internal Method used to orchestrate the parsing of the toml file.
        """
        #Valid Parent Keys for the toml
        vParent=['NETWORK', 'ACTION']
        #reads from a toml file
        with open(self.filepath, "rb") as stream:
            try:
                tml=toml.load(stream)
            except UnicodeDecodeError as err:
                print("ERROR: Your TOML File Appears to be corrupted or your pointing to the wrong file")
                raise err
            except toml.TOMLDecodeError:
                raise toml.TOMLDecodeError("Your TOML File Appears to have Formatting Error")
            except FileNotFoundError:
                raise FileNotFoundError("Cannot Find the File, Ensure the file path is correct and the file exits")

        #checks if the TOML file contains the two main Dictionaries 
        if all(x in vParent for x in tml):
            net=tml['NETWORK']
            actions=tml['ACTION']
            place=0 #tracks the place
            toDo=[]
            v=self._var_test()
            for action in actions:
                place+=1
                match action["action"]:
                    case 'wait':
                        wait=v.waittest(action)
                        #creates action object, because its type wait cannot have an id-type 
                        toDo.append(self.Action(type='wait', value={'wait' : wait}))
                    case 'text':
                        tp=v.texttest(action)
                        idtype=tp[0]
                        valuetype=tp[1]
                        #creates action object and adds it to the list, The value can be None, when the user wants to be prompted for the password
                        toDo.append(self.Action('text', {idtype : action[idtype]}, value={valuetype : action[valuetype]} if valuetype!=None else None))
                    case 'click':
                        idtype=v.clicktest(action)
                        #creates action object and adds it to the list
                        toDo.append(self.Action('click', {idtype : action[idtype]}))
                    case 'move':
                        idtype=v.movetest(action)
                        #creates action object and adds it to the list
                        toDo.append(self.Action('move', {idtype : action[idtype]}))
                    case _:
                        raise ValueError(f"missing And/or invalid action in action#{place}")
            return(net, toDo)
        else:
            raise ValueError("Error, your either missing NETWORK or ACTION from your CONFIG")
    
    def changeconfigfile(self,filepath: str="") -> None:
        """
        Changes the path of the set config file to the new path supplied AND parses it
        """
        self.filepath=filepath
        self.ingest=self._tomlparse()

    def result(self) -> tuple:
        '''
        returns the ingested data
        '''
        return tuple(self.ingest)

v=toml_parser(r"EXAMPLE.toml")
print(v.result())