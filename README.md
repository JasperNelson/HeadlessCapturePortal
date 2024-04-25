# Headless Capture Portal
## Architecture
!["TOML Capture Portal Diagram"](./images/TOML-Capture-Architecture.png)
* Major Classes:
    * `WebLogin`: Attempts to log into captive portal given a set of settings and actions
    * `SettingsAndActions`: Named tuple.
        1. First Element: Dictionary of Settings
        2. Second Element: List of actions
    * `toml_parser`: Takes a toml file path, reads a toml file from the given path, and creates a settings and actions object.
    * `Cmdline`: Reads command line flags from user and returns toml file.
    * Unit Tests: pytest files excercising objects above

##### FOR DEVELOPERS
* Environment Setup:
    * use anaconda
        1. go to https://docs.anaconda.com/free/miniconda/  And install it.
        2. make sure to add conda to your path when you are in the install process.
        3. setup a conda environment and with it use the commands 
            ```
            conda create -n captrportal
            conda activate captrportal
            conda install python
            pip install -r requirements.txt
            ```