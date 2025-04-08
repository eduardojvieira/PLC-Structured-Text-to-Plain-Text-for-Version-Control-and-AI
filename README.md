# PLC Structured Text to Plain Text Converter

Convert CODESYS and ABB Automation Builder projects to plain text files for version control and AI-assisted programming.

## Features

- Export projects to plaintext files (trackable in Git/VCS)
- Import modified plaintext files back into projects
- Generate project templates
- Update projects from templates
- Supports exporting:
  - Folders, POUs, EVLs, EVCs
  - Task Configurations, DUTs, Methods
  - Properties, Actions, Transitions
  - Communication Devices*

*See [Exporting Communication Devices](#exporting-communication-devices) section

## Installation

### Using Install Script (Recommended)
1. Clone this repository
2. Run `install.bat` as administrator

### Manual Installation
1. Copy `config.json` to `C:\<CODESYS INSTALL LOCATION>\CODESYS\Script Commands`
2. Edit paths in `config.json` to point to repo files

## Adding to CODESYS Toolbar
1. Tools → Customize → Toolbars
2. Add new "Scripts" toolbar
3. Add commands: 
   - Export To Files
   - Import From Files
   - Save As Template
   - Update From Template

## Project Templates

CODESCRIBE exports only implementation logic, not full project configuration. 

- Generate templates with `Save As Template`
- Create projects by:
  1. Copying template to `<project_name>.project`
  2. Opening in CODESYS
  3. Using `Import From Files`

## Exporting Communication Devices

Top-level devices under `Communication` are exported as folders. Sub-devices use native CODESYS XML.

To disable: Add `_NO_EXPORT` folder under `Communication`.

## Supported Versions

Tested on CODESYS V3.5 SP11 with IFM CR711s packages.

## Documentation

- [CODESYS Scripting Docs](https://help.codesys.com/webapp/idx-scriptingengine)
- Local: `C:\<CODESYS INSTALL LOCATION>\CODESYS\Online Help\en\ScriptEngine.chm`

## Screenshots

![Toolbar](docs/toolbar.png)

CODESYS Project:
![CODESYS Project](docs/example_project_codesys.png)

Converted to Plaintext:
![Plaintext Project](docs/example_project_vscode.png)

Template File:
![Template](docs/example_template_file.png)
