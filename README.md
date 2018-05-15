# The Patronus Project
` `
This project was a 1 year research project into building a tool that can automated a cyber-red-team.
Acting in both the live environment and modelling data from that environment.
` `
The idea is to now open source the result, and allow contributions from others.
This project uses Python, JSON, Neo4j Graphing Database and a number of security tools to gather data.

![alt text][logo]
[logo]: https://github.com/benjaminturnbull/Patronus/blob/master/img/Logo_Patronus.png "Patronus Logo"

### About You
---
**Skills to have and the basic order for software install:**
You should have a good understanding of Python 3.
A good understanding of JSON.
A basic understanding of databases, specifically graphing databases.
A good understanding of Cyber Security, penetration testing or related field.
An understanding of the intent of Patronus, to act as a modelling tool for the networked target system.

**Preparing and setting up The Patronus Project:**
Python 3.6 shoud be installed first.
Git needs to be installed, optionally a system such as SourceTree.
Then move on to installing PyCharm and loading the project.
Then install Neo4j and test connection.

**A few note about the project at large**
It is under development but many parts are working.
There is a web build, very basic, using Flask.
The web build is under the `web` folder.
No details are written here for the Flask part, feel free to check it out.

### Get This Running - A Software List:
This assumes you have nothing more than a clean OS install.
The following is a list of the main programs needed.
___
* **Python**
Python 3.6 is the interpreter used in this project.
[Python 3.6.5](https://www.python.org/downloads/release/python-365/) - Select from the versions for your own system, i.e. x86-64 for Win 64 bit OS.
_________________________
* **Git**
Git is used to manage code repositories. This is the CMD MinGW64 tool.
[Git](https://git-scm.com/download/win) - Windows download
___
* **PyCharm**
PyCharm is a Python (and more) IDE
[PyCharm Pro](https://www.jetbrains.com/pycharm/) - This project was written with Jetbrains Pycharm Pro.
[PyCharm Edu](https://www.jetbrains.com/pycharm-edu/) - The Edu version can be used instead of Pro.
___
* **Neo4j**
Neo4j is a graphing database
[Neo4j Graph Database](https://neo4j.com/product/) - The Database used in this project
___
#### Other Useful software Items
* **Pip**
Pip is useful for the management of packages. Install it to handle requirements.txt
* **Sourcetree**
Sourcetree is used to manage Git repos during development (where the code is worked on)
* **Bitbucket**
Bitbucket was used in this project, prior to moving to public git.
* **Flask**
Flask is used for the web front end. The Web front is in development and is very rudimentary.

### Get This Running! - Installing:

Step by steps for the stages of installation.
`Callouts` are used to show interactions, not necessarily commands.

#### Installing Python
**Download the exe and run it:**
[Python 3.6.5 exe](https://www.python.org/ftp/python/3.6.5/python-3.6.5-amd64.exe) - Python 3.6.5 64Bit
* Download Python 3.6 from the link above and extract the file or run the x64 exe if you chose that option - direct link below.
* Select the tick box `'Add Python 3.6 to PATH'` on Windows, then `'Install Now'` and accept any UAC prompts.
* Select the `'Disable path length limit'` and accept any UAC prompts.
* `'Close'` & thats Python done for the moment.
---
#### Installing Git

**Download the exe and run it:**
[GIT](https://git-scm.com/download/win) - Windows download

* Click `'Next'` through the steps, chosing a folder for install, select extra options, such as updates.
* It is strongly suggested you change the default editor, unless you are a VIM master.
* Nano is the best option when no editors are installed.
* Leave `'Use Git from the Windows Command Prompt'` selected
* Leave `'Use the OpenSSL library'`
* On Windows, leave the top option for `'Checkout Windows-style...'`
* In most cases, it is easier to change to `'Use Windows' default...'`
* Leave `'Enable file...'`  & `Enable Git ...'` & click `'install'`
* `'Launch Git Bash'` and `'Finish'`
---

#### Installing PyCharm
**Download the exe and run it:**
[PyCharm Edu exe](https://www.jetbrains.com/education/download/download-thanks-pce.html) - Education Version, with learning Python included.
[PyCharm Pro exe](https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=windows) - Pro version, license and trials.

* Download PyCharm, either Pro or Edu
* Run the exe file, at the install options select `Python 3.6` (installed earlier) and choose the appropriate 32 or 64 bit launcher shortcut.
* If you arent sure about your OS being 32 or 64 bit, you can do something fun in Windows CMD such as `echo %PROCESSOR_ARCHITECTURE%`.
* Ensure the .py box is checked under Create associations.
* Select a Start Menu folder to house the shortcut, so you can find it later.
* Tick `Run Pycharm` and `Finish`.
* If this is a clean install, just leave `'Do not import settings'` and click OK
* Slide the scroll bar down and click Accept on T&Cs noting that you have read them, then select either Educator or Learner option.
* `Create New project` from the menu, save it as `Patronus`.
* GUI: If you prefer dark theme, Select `File` and `Settings`, then `Appearance` and under the dropdown for `Theme`, change to `Darcula`.

**Configuration Needed:**
* A number of folders need to be set as a `Sources Root` folder or the program wont fire.
* Other folders must be set as excluded.
* The setup is in testing and development, this is a part of that.


* **Folders: Sources Root**
* In the Pycharm IDE, below venv, right click the top `patronus` folder and select `Mark Directory as` and select `Sources Root`, or look for the blue.
* Do the same for the `config` and `utils` folders.

>venv>`patronus`
and
>venv>patronus>`config`
and
venv>patronus>`utils`



* **Folders: Exclude Files**
* Right click the following folders, and select `Mark Directory as` and `Excluded`
>venv>patronus>`patronus`
and
venv>patronus>`utilsv2`
and
venv>patronus>`input`

* This sets these folders in a hierarchy that allows the program to find them.
* Depending on your OS and set environment variables, OS path, you may prefer to do this part differently, go ahead.
* As tested setup was in a clean OS, and required the listed folders to be set for the program to run.
* See Installing Neo4j down the page, to complete the setup and test of this configuration.
---
### The Business of connecting to Git
**Now we are ready to load The Patronus Project:**
* Loading the Git repo via MinGW
* Here we can use the Git cmd tool to load the github repo of Patronus, into the new project folder
* launch a `cmd` prompt.
* CD into the project directory that you created.
* Commonly it will be: `\Users\'yourname'\PycharmProjects\Patronus\venv`


```.cmd
>cd \Users\dev\PycharmProjects\Patronus\venv
```
Then git clone the repo `TODO: get the right link here`
```
git clone https://github.com/`thepatronusproject`
```
Then cd to the patronus folder and perform pip install on requirements.txt
```
cd /patronus
pip install -r requirements.txt
```
If for any reason, that doesnt work, pip install each item in the below list.

```
pip install Flask pprint requests schedule xmltodict py2neo python-nmap
```

---
#### Installing Neo4j
`**Since the project started, Neo4j Community Edition has changed**`
**The way to setup Neo4j might vary from these instructions**
[See here:](https://neo4j.com/docs/operations-manual/current/installation/) - Neo4j Operations Manual
Installation pre-requisites may include Java 8, depending on server or desktop environments.

`It is recommended that you use Neo4j Desktop`
**Download the exe and extract it:**
The version used in the project was 3.2.1
This is now represented in `Neo4j Desktop`
[Neo4j Desktop](https://neo4j.com/download-thanks-desktop/?edition=desktop&flavour=winstall64&release=1.1.0&offline=true) - Version 1.1.0
* Run the Exe and install
* When installed, create a `New project` and select `New Graph` and then `Create a Local Graph`
* Call the database Neo4j and set the password Neo4j
* Start the database and test connection in a web browser to http://localhost:7474/browser/
* If you want to set a different or more secure password, edit the Neo4j password under:
>Neo4j Desktop>Projects>Project Folder>Manage>Administration

And also the password set in:

>patronus>config>graph_config.py file where you see the password 'Neo4j'.
 ---

### Finally! Test Neo4j and The Patronus Project
**Testing of the setup**
To test the setup, provided you have done the afore steps of Python, Git, PyCharm, Git Repo download and Neo4j
You can test the system by navigating to the folder

>venv\patronus\ingestion\scenario_importer\scenario_2\scenario_importer.py

Right click in the code window and select `Run 'scenario_importer'`
Or press
>Ctrl+shift+F10

This should start code running in the lower window.
Any errors will need to be carefully checked

**View Data**
Now move to a web browser and access the database at

>http://localhost:7474/browser/

You may have to log in with `neo4j:Neo4j` or your set credentials

At the ```$``` at the top of the panel, you can enter the Neo4j Cypher query to check that data is in the database:

```
$ CALL db.schema()
```
Else in the left side bar, navitate to the star icon and navigate:
>Sample Scripts > Data Profiling > What is related and how

Then top right click the 'play' icon to run the query in the database
Which should return a lovely mess of data in a visualisation of related nodes.
**Congratulations it works!**

Now add to it :)
:bowtie:
---
### Alternate Neo4j Server
##### *Untested
**Download the zip and extract it:**
[Neo4j](https://go.neo4j.com/download-thanks.html?edition=community&release=3.2.11&flavour=winzip&_ga=2.259156099.828900468.1526278480-953144785.1526278480)  -  Community Edition 3.2.11 Windows Server
* Copy Extracted files to a permanent folder location
* Navigate to the folder neo4j-community-3.2.11/bin & use the uri bar, type cmd. This launches a CMD prompt.
* After this, run `ne04j.bat start`
* You may need to run the CMD as administrator
* You may need to enable Powershell scripts with:

```posh
> Set-ExecutionPolicy Unrestricted
```
* No further testing was done on this form of Neo4j.
---


## Authors

* **Dr Ben Turnbull**
* **Research Associate G. R. Macleod**
* **Code Contributor J. Gosbell**

## License

This project is licensed under the MIT License.
