from Captr.ConfigParser import Config
#Makes a object that uses the values set in the Config  

class ConfigDistributor(): #Inherit ME!!!
    def __init__(self, confIngest: Config.Ingest) -> None:
        self.logging= confIngest.Ingest["logging"]
        self.safePrompt= confIngest.Ingest["safetyPrompt"]
        self.loginFilesDir= confIngest.Ingest["LoginFilesDir"]
