# Headless Capture Portal
## Architecture

* Major Classes:
    * `WebLogin`: Attempts to log into captive portal given a set of settings and actions
    * `LoginParser.Ingest`: Named tuple.
        1. First Element: Dictionary of Settings
        2. Second Element: List of actions
    * `LoginParser`: Takes a toml file path, reads a toml file from the given path, and creates a Ingest NamedTuple containing settings and actions.
    * `Config`: Takes a toml file path, reads a toml file from the given path, and creates a Ingest NamedTuple containing Configuration information
    * `KeyManager`: Manages keys from the current operating systems keyring.
    * `main`: Reads command line flags from user and returns toml file.
    * `Orchestrator`: The "meat" of the program orchestrator is a class that takes inputs and sends them to the backends.
    * Unit Tests: pytest files excercising objects above

### Current Login File Specification:

## Network Configuration

- **URL** (`URL`):
  - Overrides the default starting URL for the capture portal. 
    - Note: if the URL does not match then 
  - Important: This is **NECESSARY** FOR:
    -  Keyring functionality
    - Automatic Login/Detection/Authentication mode. Without a specified URL the file will be IGNORED any time you use the `-A`, or `--Auto` flags. 
  - Example: `URL="https://example.com"`

- **Backend** (`Backend`):
  - Defines the Backend to be used by the Captive Portal 
  - Purpose: To dictate the backend to be utilized by the Captive portal, overriding the default located in the `Config` file
  - Currently Valid strings:
    - `Debug` Backend used for troubleshooting and testing purposes
    - `f_Playwright` Backend which utilizes firefox and playwright
    - `f_v_Playwright` Visual Backend for firefox and playwright
    - `c_Playwright` Backend for Chrome
    - `c_v_Playwright` Visual Backend for Chrome

## Actions Configuration

### Click Actions

- **General Click**:
  - Action: `click`
  - Description: Clicks on elements specified by ID, name, or type.
  - **Identifiers:** (you can only have one of these)
    - ID: Supports regular expressions. Unique identifier.
      - Example: `id="example"`
    - Name: Targets elements by their name attribute on the webpage.
      - Example: `name="examplename"`
    - Type: Targets elements by their type attribute.
      - Example: `type="checkbox"`

### Wait Action

- **Wait**:
  - Action: `wait`
  - Description: Pauses the execution for a specified number of seconds before proceeding.
  - Duration: Time in seconds.
  - Example: `wait=30`

### Text Input Actions

- **Text Input**:
  - Action: `text`
  - Description: Enters text into a field. If `value` is not specified, the user will be prompted. 
  - **Identifiers:** (you can only have one of these)
    - ID: Supports regular expressions. Unique identifier.
      - Example: `id="example"`
    - Name: Targets elements by their name attribute on the webpage.
      - Example: `name="examplename"`
    - Type: Targets elements by their type attribute.
      - Example: `type="checkbox"`
    - xpath: Targets elements by their xpath attribute.
      - Example: `xpath=\foo`
  - **"Enterables":** 
    - Value: The text to enter. Optional.
      - Example: `name="name", value="examplestringEGUserName"`

#### Secure Text Entry
- **Password Input**:
  - Action: `text`
  - Description: Utilizes the operating system's keyring to securely store and access passwords.
  - Name: `password`
  - Keyring Configuration:
    - Supported backends include: SecretService, KWallet, Windows Vault, macOS Keyring, libsecret, and Bitwarden.
    - The format for keyring values is `[username, *keyring-service]`.
        - \*\*Valid keyring-service name strings are `secretservice`, `kwallet`, `windows`, `macos`, `libsecret`, and `bitwarden`
    - During initialization, if `-R` is passed, it allows changing the set keyring password.
  - Example: `keyring=["YourUserName"]`

### Navigation Actions

- **Move Action**:
  - Action: `move`
  - Description: Navigates to a new page specified by href, ID.
  - Examples:
    - `href="href_url"` (navigates to a page by URL)
    - `id="ID"` (navigates to a page by the element ID)

## Important Notes

- <span style="color: red; font-weight: bold; background-color: black;">It is highly recommended NOT to store passwords in plaintext. Use the keyring options provided for secure password management.</span>
- Ensure that your configuration aligns with the network and operational requirements specified in this document.

#### FOR DEVELOPERS
* Environment Setup:
    * use anaconda \\ disclaimer we are not affiliated with Anaconda in any way.
        1. go to <https://docs.anaconda.com/free/miniconda/>  And install it.
        2. make sure to add conda to your path when you are in the install process.
        3. setup a conda environment and with it use the commands 
            ```
            conda create -n captrportal
            conda activate captrportal
            conda install python
            pip install -r requirements.txt
            ```

#### ROADMAP:
##### FOR  1.0 (First Release)
1. [x] ~~Define a TOML format to define per session actions and settings~~
2. [x] ~~Create a Parser to digest the Defined TOML structure~~
3. [x] ~~Define a safe way to store and process passwords~~
4. [x] Define a module that verifies that a captive portal actually exists on the network and that it meets the specifications defined in the `Login` files.
5. [x] ~~Define an extensible configuration file format~~
6. [x] Finish "Quick" frontend (all the commands that cause an immediate action)
7. [x] Setup the Auto login to automatically login to a captive portal from a matching given url
8. [x] Setup Unit Tests 
9. [x] Develop Modular and Actionable Network Portion of Backend using requests that will take commands from the frontend. HOWEVER ensure that we are creating a good api that 
can be expanded on by additional installable packages/modules. (i.e [Selenium] or [Custom backends]) 
10. [x] Develop Debug Backend
11. [x] Setup the yes command to bypass questions
12. [x] Setup verbose command to automatically enable verbose logging
13. [x] Setup Layout command to automatically return the layout of a URL. 
14. [x] Setup Default command to login using a single given login toml file
15. [x] Setup The Auto command to login using a directory of files contained in the config or manually specified
16. [x] Setup the URL command to return the captive portal
1. [x] Develop the Playwright Backend
##### FOR 2.0
1. [ ] Create a Selenium backend, 
2. [ ] Create a Custom backend using requests(wont support javascript but will be faster)
2. [ ] Create a Intuitive TUI that will guide a user in creating a TOML Login file for a given network. 
3. [ ] Allow for specification of Automatic Login by SSID and IP addresses. (as opposed to just URL) 
##### FAR FUTURE
1. [ ] Port portions of program to GOLANG/RUST????
