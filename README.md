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

## Installation

1. Copy the Script Commands folder to `C:\<CODESYS INSTALL LOCATION>\CODESYS\Script Commands` (Example: `C:\Program Files\CODESYS 3.5.20.50\CODESYS\Script Commands`) for CODESYS or `C:\<AUTOMATION BUILDER INSTALL LOCATION>\AutomationBuilder\Script Commands` (Example: `C:\Program Files\ABB\AB2.8\AutomationBuilder\Script Commands`) for Automation Builder
   
2. Open CODESYS or Automation Builder without opening a Project
   
3. In menu, select Tools -> Customize
   ![customize](img/1.%20codesys.png)
   ![customize](img/1.%20AB.png)

4. In Toolbars select one tollbar like Standard or create a new toolbar and inside it click Add Command...
   ![toolbar](img/2.%20toolbar.png)

5. In categories select ScriptEngine Commands and under commands add: Export to Files and Import From files.
   ![add](img/3.%20commands.png)

6. Now you should have the export and import buttons in the toolbar.
   ![export](img/4.%20buttons.png)


## Usage Example

1. Create a project in Codesys/Automation Builder.
   ![project](img/5.%20project.png)

2. Create a new folder under the Application, make sure to move all the POUs, DUTs, Methods, Functions, Function Blocks, etc. to this new folder since this is the location used for syncing. Anything outside of this folder will not be imported/exported. Things like communication or recipe management should be outside this folder since this script doesn't support importing/exporting this objects.
   ![src](img/6.%20src.png)
   
3. Now you can click on the button Export to Files to export all the POUs, DUTs, Methods, Functions, Function Blocks, etc. to the filesystem. The files will be generated in the project folder under `<Project Name>/<Device Name>/<Application Name>/src`.
   ![export](img/7.%20export.png)
   ![files](img/8.%20files.png)

4. You can now open the files in any text editor or IDE. In this case I will use Windsurf AI IDE.
   ![ide](img/9.%20ide.png)
   ![ai](img/10.%20ai.png)

   Note: make sure to dont delete the line `// --- BEGIN IMPLEMENTATION ---` betweeen the variable definition and the code. This allow the script to split the declaration and implementation and CODESYS and Automation Builder keep them separated.

5. You can now import the modified files into the project using the import from files command and upload the project to your PLC.
   ![imported](img/11.%20imported.png)

6. After working on a feature or bug fix, you can make a commit and push the changes to your repository and show the changed code since the filesystem has the code in plain text files. Make sure to save the binary project in he repository.
   ![git](img/12.%20git.png)

## Supported Versions

Tested on CODESYS V3.5 SP20.

## Documentation

- [CODESYS Scripting Docs](https://help.codesys.com/webapp/idx-scriptingengine)
- Local: `C:\<CODESYS INSTALL LOCATION>\CODESYS\Online Help\en\ScriptEngine.chm`
