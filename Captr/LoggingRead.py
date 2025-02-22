import yaml
import logging.config


def readLoggingConfig(arg: dict | None = None) -> None:
    """
    function that reads from dictconfig of logging.
    """
    dictconfig = dict()
    if arg is None:
        with open("Captr/logging.yml", "r") as f:
            dictconfig = yaml.safe_load(f)
    else:
        dictconfig = arg

    logging.config.dictConfig(dictconfig)
