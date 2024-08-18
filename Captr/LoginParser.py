from __future__ import annotations
# Parses TOML files into digestible python variables and objects
from Captr.TOMLRead import TOMLRead
from typing import Optional, NamedTuple, IO, cast


class Action(NamedTuple):
    """
    A data structure representing an action to be performed in Login Files Used by TOMLparser, 

    Attributes
    ----------
    type : str
        The type of action (e.g., 'wait', 'text', 'click', 'move').
    id : dict, optional
        The identifiers for the action, relevant for all types except 'wait'.
    content : dict, optional
        The values being entered into a field during a text action or a keyring to be called from
        either 
        {'keyring: List}
        OR
        {'value': String}
    wait : int
        Wait time for wait action

    """
    # type of action
    type: str
    # id is not used by wait actions
    id: Optional[dict[str, str]] = None
    # value is only used in text actions
    content: Optional[dict[str, str]] = None
    # only used in wait actions
    wait: Optional[int] = None


class LoginParser():
    """
    TOML file parser that translates the content of a login-file into a easily digestible NamedTuple
    This parser is specifically designed to interpret TOML files used for configuration into actionable objects based 
    on the
    'NETWORK' and 'ACTION' fields as meets our specification in the readme.

    - Validates and processes various types of actions ('wait', 'text', 'click', 'move') 
    as defined in the TOML file. (see EXAMPLE.toml)

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
    changeloginfile(filepath: str)
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

    class _ingest(NamedTuple):
        """
        Subclass of TOMLparser that defines a NamedTuple which is used for returning the value of the class
        """
        Actions: list[Action]  # forward reference
        URL: Optional[str | None] = None
        Backend: Optional[str | None] = None

    def __init__(self, filepath: IO[bytes] | str) -> None:
        """
        Constructs a LoginParser object that parses the given input.

        Arguments:
        - filepath: Either a string that points to a TOML file or a Python file-like
          such as what you can get from calling open(foo, "rb") or io.BytesIO().
        """
        self.filepath: IO[bytes] | str
        if type(filepath) is str:
            # Read the file from disk.
            self.filepath = cast(str, filepath)
        else:
            self.filepath = cast(IO[bytes], filepath)
        self.export: LoginParser._ingest
        self.ingest = self._loginparse()

    def __str__(self) -> str:
        return (
            f"the Network Portion of the file is a dictionary containing the following: \n {
                self.ingest[0]} \n"
            f"the Actions listed in the file are as follows: \n {
                self.ingest[1]}"
        )

    def __repr__(self) -> str:
        return (
            f"Network:{self.ingest[0]}, Actions{self.ingest[1]}"
        )


# defines the new type of object that we will be setting every instance of ACTION to\
    class _var_test():
        """
        helper class used internally by tomlparseer to validate and process the actions specified in the toml file
        """

        def __init__(self) -> None:
            """
            contains the crucial and valid expressions for each action type in the TOML file used as a refrence for
             errors
            """
            # allowed Identification values that are compatable with every action type
            self.t_identify_all = ["id", "xpath"]
            self.click_type = ["type", "contains", "name"] + self.t_identify_all
            # extra allwed ID value for move"
            self.t_identify_move = self.t_identify_all + ["href"]
            # valid set values for text
            self.t_choice_text = ["value", "keyring"]

        # identifies the key type being used as well as if there is only 1 of them.
        def identifytest(self, action: dict, methodOfId: list) -> str:
            numberOfId = sum(int(key in action.keys()) for key in methodOfId)
            if 1 < numberOfId:
                raise ValueError(
                    f"You can only supply one identifier for the action type in {action}")
            elif 1 > numberOfId:
                raise ValueError(
                    f"no known identifier was included for the action{action}")
            keytype = [str(TheKey) for TheKey in action if TheKey in methodOfId]
            return (keytype[0])

        def waittest(self, action: dict) -> str:
            # needs to be string to fit in with action object
            if len(action) > 2 and "wait" in action.keys():
                raise ValueError(
                    "Wait actions only accept wait=time as an argument")
            return (action["wait"])

        def clicktest(self, action: dict) -> str:
            # tells us if there is an invalid combination of values
            return (self.identifytest(action, self.click_type))

        def texttest(self, action: dict) -> tuple:
            temp = sum(int(key in action.keys()) for key in self.t_choice_text)
            valuetype = None
            # Its valid to not include any text choice, in this situation we will prompt them OTF
            if 1 < temp:
                raise ValueError(
                    "You cannot use multiple methods of defining value for a text field")
            # in case they include a value aka mode for the password
            # NOTE: could be implemented better right now its doing unnecessary compute
            elif 1 == temp:
                valuetype = [
                    str(TheKey) for TheKey in action if TheKey in self.t_choice_text][0]
            # idtype, valuetype
            return (self.identifytest(action, self.click_type), valuetype)

        def movetest(self, action: dict) -> str:
            return (self.identifytest(action, self.t_identify_move))

    # parses the toml from a file
    def _loginparse(self) -> tuple:
        """
        Internal Method used to orchestrate the parsing of the login file.
        """
        # Valid Parent Keys for the toml
        vParent = ['NETWORK', 'ACTION']
        # reads from a toml file
        tml = TOMLRead(self.filepath)
        # checks if the TOML file contains the two main Dictionaries
        if all(x in vParent for x in tml):
            net = tml['NETWORK']
            cast(dict, net)
            actions = tml['ACTION']
            place = 0  # tracks the place
            toDo = []
            backend = None
            url = None
            v = self._var_test()
            for options in net:
                try:
                    match str(options):
                        case 'URL':
                            url = net[options]
                        case 'Backend':
                            backend = net[options]
                        case _:
                            raise ValueError("invalid option in network")
                except ValueError:
                    raise ValueError("One of your steps contains a value of the wrong type\n"
                                     "e.g a boolean instead of a string")
            # parses the actions and puts the values into action objects
            for action in actions:
                place += 1
                try:
                    match action["action"]:
                        case 'wait':
                            mwait = v.waittest(action)
                            # creates action object, because its type wait cannot have an id-type
                            toDo.append(Action(type='wait', wait=int(mwait)))
                        case 'text':
                            tp = v.texttest(action)
                            idtype = tp[0]
                            valuetype = tp[1]
                            # creates action object and adds it to the list, The value can be None, when the user wants 
                            # to be prompted for the password
                            toDo.append(Action('text', {idtype: action[idtype]}, content={
                                        valuetype: action[valuetype]} if valuetype is not None else None))
                        case 'click':
                            idtype = v.clicktest(action)
                            # creates action object and adds it to the list
                            toDo.append(
                                Action('click', {idtype: action[idtype]}))
                        case 'move':
                            idtype = v.movetest(action)
                            # creates action object and adds it to the list
                            toDo.append(
                                Action('move', {idtype: action[idtype]}))
                        case _:
                            raise ValueError(
                                f"missing And/or invalid action in action#{place}")
                except TabError:
                    raise KeyError(
                        "One of your steps is missing a action, identifier, or")
            self.export = self._ingest(
                URL=url, Backend=backend, Actions=toDo)
            return self.export
        else:
            raise ValueError(
                "Error, your either missing NETWORK or ACTION from your LoginFile")

    def changeloginfile(self, filepath: str = "") -> None:
        """
        Changes the path of the set login file to the new path supplied AND parses it
        """
        self.filepath = filepath
        self.inges = self._loginparse()

v = LoginParser(r"./Examplelogins/EXAMPLE.toml")
print(v.export)
