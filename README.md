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