# VS Code Workspace Tools for the CoRE Simulation Models for OMNeT++
This project is supposed to help you set up VS Code as your IDE for OMNeT++ development with the CoRE simulation models.
What you will find is a set of scripts and configuration files to set up your workspace and to create build and run tasks for all models.

I got inspiration from this repository: https://github.com/rjmalves/omnetpp-VS Code

This is a work in progress and suggestions and additions are welcome!

## Features
- Model-repository setup
  - [x] Clone all models 
    - [ ] Add script call argument to clone from GitHub
    - [ ] Add options to clone only some models
  - [x] Check out the correct branch 
    - [ ] Add script call argument to choose the branches
- [x] Create Build tasks for all models
  - [ ] add JSON config for models and dependencies
- [X] Create launch configs for simulations
  - [X] Create run tasks for the currently open file with qtenv (switched to launch configs)
  - [X] Attach debugger -- debug in VS Code
  - [ ] Create run task for parameter studies and batch runs in cmdenv

## Prerequisites
- On Windows use the WSL: Windows Subsystem for Linux (https://learn.microsoft.com/en-us/windows/wsl/install)
  - Recommended distro is Ubuntu (mine is currently running 22.04 LTS)
  - NOTE: In the WSL there is no Papierkorb (Recycle Bin) so be careful when deleting files.
- OMNeT++ (https://omnetpp.org/)
  - Follow the install guide for Linux and your distro
- VS Code (https://code.visualstudio.com/)
  - Some Usefull plugins for VS Code are:
    - On Windows: WSL
    - C/C++
    - C/C++ Extension Pack
    - Makefile Tools
    - OMNeT++ NED
    - Github Copilot (+Chat)

## Setup VS Code Workspace
Open this repository in VS Code and install the recommended extensions.
Inside the `.VS Code` folder you will find the `settings.JSON`, `c_cpp_properties.JSON` and a default `tasks.JSON` file.

**Adjust the paths in the `settings.JSON` and `c_cpp_properties.JSON` to your OMNeT++ installation.**

The `tasks.JSON` file contains a default setup for tasks, which should work if you use the `setup_models.sh` script to setup the workspace. If the tasks do not work for you checkout the `create_tasks.py` script, adjust it to your needs, and generate new tasks.

The `launch.JSON` file contains a default setup for launch configs, which should work if you use the `setup_models.sh` script to setup the workspace. If the launch configs do not work for you checkout the `create_tasks.py` script and look for everything containing "run", adjust it to your needs, and generate new launch configs.

## Setup models
In the top level of this repository is a script to clone all models and checkout the correct branches.

Launch the script with `./setup_models.sh`.

By default, the inet framework will be cloned from GitHub; all CoRE simulation models will be cloned from the inet rg git.
Make sure you have access to the repositories and SSH is configured correctly.

For now you have to edit the script to change the branches to checkout or to exclude some of our models from git clone.

## Clone repo into existing OMNeT++ workspace
If you already have an OMNeT++ workspace and want to add this repository to it, you can do so by cloning this repository into your workspace.
```bash	
cd <path to your workspace>
rm -rf .git
git init
git remote add origin git@github.com:CoRE-RG/OMNeT4VS Code.git
git fetch
git checkout origin/master -t --mixed
```
**Make sure though that all frameworks exist in the correct place to use the scripts, tasks, and lauch configurations in this repository.**

## Create Build Tasks
In the top level of this repository is a python script `create_tasks.py` to create build tasks for all models.
At the top of the script there are some definitions you might want to adjust to your needs, note that they use relative paths depending on the `settings.JSON`, so they should work out of the box if you use the `setup_models.sh` script.
Then there are a lot of helper functions to create the tasks.
At the bottom of the script is the actual execution of the functions to create the tasks, which you can adjust to your needs, e.g., if you do not want exclude specific models.

Run the script using `python3 create_tasks.py` in the repository root. 
It will create a
`tasks.JSON` file in the `.VS Code` folder. If there was an old `tasks.JSON` file it will be moved to `tasks.JSON.old` with an index if there are multiple so you do not loose a task configuration.

## Building the models
To build the models go to the top menu and select `Terminal` -> `Run Task...`. 
You can select a specific model or build all models at once.
There are two build tasks for each model, one for debug and one for release builds.
You can also clean the build directories with the `clean` task.

## Create run tasks
In the `create_tasks.py` script, there are also functions to create launch configs for simulations (look for "run" in the names).
There are four launch configs that all run a simulation for the currently openned file with qtenv: Debug (uses opp_run_dbg) and Release (uses opp_run), each with and without building all models beforehand.
It should be possible to adjust the script to create more run tasks, e.g., for parameter studies or batch runs in cmdenv.
This is future work...

## Run a simulation
To launch a simulation go to the `run and debug` tab of VS Code and select the config you want to run.
Make sure you have the main simulation ini file (e.g., omnetpp.ini) open in the editor.
Just click run and the simulation should start.
The debugger will be attached automatically and you can use breakpoints and step through the code.
