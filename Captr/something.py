import yaml
import logging.config
dictconfig=dict()
with open("Captr/logging.yml", "r") as f:
            dictconfig=yaml.safe_load(f)
logging.config.dictConfig(dictconfig)
logger=logging.getLogger(__name__)
logger.info(f"modes={"foo"}")