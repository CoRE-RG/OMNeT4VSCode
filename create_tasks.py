#!/usr/bin/env python

##############################################
# Author: Timo Haeckel                       #
# Script to create tasks for the core        #
# simulation models, such as build, run and  #
# test tasks                                 #
##############################################
import os
import shutil
import json
from collections import OrderedDict

vscode_folder = ".vscode"
tasks_file = "tasks.json"

sep = ':' # path separator

# project roots
inetRoot = "${workspaceFolder}/inet"
core4inetRoot = "${workspaceFolder}/CoRE4INET"
openflowRoot = "${workspaceFolder}/OpenFlow"
fico4omnetRoot = "${workspaceFolder}/FiCo4OMNeT"
signalsandgatewaysRoot = "${workspaceFolder}/SignalsAndGateways"
soa4coreRoot = "${workspaceFolder}/SOA4CoRE"
sdn4coreRoot = "${workspaceFolder}/SDN4CoRE"

# project lib paths
libDbgExt = "_dbg"
inetLib = inetRoot + os.sep + "src" + os.sep + "INET"
core4inetLib = core4inetRoot + os.sep + "src" + os.sep + "CoRE4INET"
openflowLib = openflowRoot + os.sep + "src" + os.sep + "OpenFlow"
fico4omnetLib = fico4omnetRoot + os.sep + "src" + os.sep + "FiCo4OMNeT"
signalsandgatewaysLib = signalsandgatewaysRoot + os.sep + "src" + os.sep + "SignalsAndGateways"
soa4coreLib = soa4coreRoot + os.sep + "src" + os.sep + "SOA4CoRE"
sdn4coreLib = sdn4coreRoot + os.sep + "src" + os.sep + "SDN4CoRE"

# project ned paths
inetNedPath = inetRoot + "/src" + sep + inetRoot + "/examples" + sep + inetRoot + "/tutorials" + sep + inetRoot + "/showcases"
core4inetNedPath = core4inetRoot + "/src" + sep + core4inetRoot + "/examples"
openflowNedPath = openflowRoot + "/src" + sep + openflowRoot + "/scenarios"
fico4omnetNedPath = fico4omnetRoot + "/src" + sep + fico4omnetRoot + "/examples"
signalsandgatewaysNedPath = signalsandgatewaysRoot + "/src" + sep + signalsandgatewaysRoot + "/examples"
soa4coreNedPath = soa4coreRoot + "/src" + sep + soa4coreRoot + "/examples"
sdn4coreNedPath = sdn4coreRoot + "/src" + sep + sdn4coreRoot + "/examples"
# combined ned path
nedPath = inetNedPath + sep + core4inetNedPath + sep + openflowNedPath + sep + fico4omnetNedPath + sep + signalsandgatewaysNedPath + sep + soa4coreNedPath + sep + sdn4coreNedPath

# project images paths
inetImagesPath = inetRoot + "/images"
core4inetImagesPath = core4inetRoot + "/images"
openflowImagesPath = openflowRoot + "/images"
imagesPath = inetImagesPath + sep + core4inetImagesPath + sep + openflowImagesPath

run_command = "${config:omnetppInstallDir}/bin/opp_run"
run_command_dbg = "${config:omnetppInstallDir}/bin/opp_run_dbg"
run_cwd_currentFileDir = "${fileDirname}"
run_group = {
    "kind": "test",
    "isDefault": False
}
run_args_default = [
    "--image-path=" + imagesPath,
    "--ned-path=" + nedPath,
    "-l",
    inetLib,
    "-l",
    core4inetLib,
    "-l",
    openflowLib,
    "-l",
    fico4omnetLib,
    "-l",
    signalsandgatewaysLib,
    "-l",
    soa4coreLib,
    "-l",
    sdn4coreLib
]

## Adjust the path to your OMNeT++ installation and workspace
omnetpp_task_env = {
    "PATH": "${config:omnetppInstallDir}/bin/"
            + ":${workspaceFolder}/inet/src:${workspaceFolder}/inet/src/inet"
            + ":${workspaceFolder}/CoRE4INET/src:${workspaceFolder}/CoRE4INET/src/core4inet"
            + ":${workspaceFolder}/FiCo4OMNeT/src:${workspaceFolder}/FiCo4OMNeT/src/fico4omnet"
            + ":${workspaceFolder}/OpenFlow/src:${workspaceFolder}/OpenFlow/src/openflow"
            + ":${workspaceFolder}/SignalsAndGateways/src:${workspaceFolder}/SignalsAndGateways/src/signalsandgateways"
            + ":${workspaceFolder}/SOA4CoRE/src:${workspaceFolder}/SOA4CoRE/src/soa4core"
            + ":${workspaceFolder}/SDN4CoRE/src:${workspaceFolder}/SDN4CoRE/src/sdn4core"
            + ":${env:PATH}",
    "OMNETPP_ROOT": "${config:omnetppInstallDir}",
    "OMNETPP_IMAGE_PATH": "${config:omnetppInstallDir}/images",
    "OMNETPP_CONFIGFILE": "${config:omnetppInstallDir}/Makefile.inc"
}

make_module = "/usr/bin/make"

task_command_make = make_module
task_type_shell = "shell"
task_group_build = {
    "kind": "build",
    "isDefault": False
}
task_presentation_default = {
    "reveal": "always",
    "panel": "shared"
}
task_dependency_none = []
task_problem_matcher = []

# function that create a run task and a run debug task for the currentlich open file
def create_run_tasks():
    tasks = []
    run_task_name = "Run current simulation ini file"
    tasks.append(create_task(run_task_name, task_type_shell, run_command, run_args_default, run_group, 
                            task_presentation_default, omnetpp_task_env, run_cwd_currentFileDir, task_dependency_none))
    run_task_name_dbg = "Run debug current simulation ini file"
    tasks.append(create_task(run_task_name_dbg, task_type_shell, run_command_dbg, run_args_default, run_group, 
                            task_presentation_default, omnetpp_task_env, run_cwd_currentFileDir, task_dependency_none))
    return tasks

# function that creates a task that makes makefiles for a model
def create_makefile_release_task_name(model_name):
    return model_name + " - Make Makefiles Release"

def create_makefile_debug_task_name(model_name):
    return model_name + " - Make Makefiles Debug"

def create_build_release_task_name(model_name):
    return model_name + " - Build Release"

def create_build_debug_task_name(model_name):
    return model_name + " - Build Debug"

# function that creates task dependencies for a list of model names
def create_task_dependencies(model_name, build_mode, model_dependencies):
    task_dependencies = []
    if build_mode == "release":
        task_dependencies.append(create_makefile_release_task_name(model_name))
    elif build_mode == "debug":
        task_dependencies.append(create_makefile_debug_task_name(model_name))
    for model_dep in model_dependencies:
        if build_mode == "release":
            task_dependencies.append(create_build_release_task_name(model_dep))
        elif build_mode == "debug":
            task_dependencies.append(create_build_debug_task_name(model_dep))
    return task_dependencies


# function that creates all tasks for a model
# model_name: name of the model
# model_dependencies: list of model !NAMES! that this model depends on
def create_all_model_tasks(model_name, model_dependencies):
    tasks = []
    tasks.append(create_makefile_task(model_name, "release"))
    tasks.append(create_makefile_task(model_name, "debug"))
    tasks.append(create_build_task(model_name, "release",model_dependencies))
    tasks.append(create_build_task(model_name, "debug", model_dependencies))
    tasks.append(create_clean_task(model_name))
    return tasks

def create_makefile_task(model_name, build_mode):
    task_name = ""
    if build_mode == "release":
        task_name = create_makefile_release_task_name(model_name)
    elif build_mode == "debug":
        task_name = create_makefile_debug_task_name(model_name)
    task_args = [
        "makefiles",
        "MODE=" + build_mode
    ]
    task_env = omnetpp_task_env
    task_cwd = "${workspaceFolder}/" + model_name
    task = create_task(task_name, task_type_shell, task_command_make, task_args, task_group_build, task_presentation_default, task_env, task_cwd, task_dependency_none)
    return task

def create_clean_task(model_name):
    task_name = model_name + " - Clean"
    task_args = [
        "cleanall"
    ]
    task_env = omnetpp_task_env
    task_cwd = "${workspaceFolder}/" + model_name
    task_dependencies = []
    task_dependencies.append(create_makefile_release_task_name(model_name))
    task = create_task(task_name, task_type_shell, task_command_make, task_args, task_group_build, task_presentation_default, task_env, task_cwd, task_dependencies)
    return task

def create_build_task(model_name, build_mode, model_dependencies):
    task_name = create_build_release_task_name(model_name) if build_mode == "release" else create_build_debug_task_name(model_name)
    task_args = [
        "MODE="+build_mode,
        "-j$(nproc)",
        "all"
    ]
    task_env = omnetpp_task_env
    task_cwd = "${workspaceFolder}/" + model_name
    task_dependencies = create_task_dependencies(model_name, build_mode, model_dependencies)
    task = create_task(task_name, task_type_shell, task_command_make, task_args, task_group_build, task_presentation_default, task_env, task_cwd, task_dependencies)
    return task

def create_task_clean_all(model_names):
    task_dependencies = []
    for model_name in model_names:
        task_dependencies.append(model_name + " - Clean")
    task = OrderedDict([
        ("label", "Clean All"),
        ("presentation", task_presentation_default),
        ("dependsOrder", "sequence"),
        ("dependsOn", task_dependencies),
        ("problemMatcher", task_problem_matcher)
    ])
    return [task]

def create_task_build_all(model_names, build_mode):
    task_dependencies = []
    for model_name in model_names:
        if build_mode == "release":
            task_dependencies.append(model_name + " - Build Release")
        elif build_mode == "debug":
            task_dependencies.append(model_name + " - Build Debug")
    task = OrderedDict([
        ("label", "Build All " + build_mode.capitalize()),
        ("presentation", task_presentation_default),
        ("dependsOrder", "sequence"),
        ("dependsOn", task_dependencies),
        ("problemMatcher", task_problem_matcher)
    ])
    return [task]

def create_task(task_name, task_type, task_command, task_args, task_group, task_presentation, task_env, task_cwd, task_dependencies):
    task = OrderedDict([
        ("label", task_name),
        ("type", task_type),
        ("command", task_command),
        ("args", task_args),
        ("group", task_group),
        ("presentation", task_presentation),
        ("options", {
            "env": task_env,
            "cwd": task_cwd
        }),
        ("dependsOrder", "sequence"),
        ("dependsOn", task_dependencies),
        ("problemMatcher", task_problem_matcher)
    ])
    return task

##### DO STUFF #####

# check if .vscode folder exists
# if not os.path.exists(vscode_folder):
#     os.makedirs(vscode_folder)

# check if tasks.json file exists
if not os.path.exists(os.path.join(vscode_folder, tasks_file)):
    with open(os.path.join(vscode_folder, tasks_file), "w") as f:
        f.write("{}")
else:
    # move old tasks.json file to tasks.json.old
    old_file_path = os.path.join(vscode_folder, tasks_file + ".old")
    if os.path.exists(old_file_path):
        index = 1
        while os.path.exists(old_file_path + str(index)):
            index += 1
        old_file_path += str(index)
    shutil.move(os.path.join(vscode_folder, tasks_file), old_file_path)
    # create new tasks.json file
    with open(os.path.join(vscode_folder, tasks_file), "w") as f:
        inet = create_all_model_tasks("inet", [])
        core4inet = create_all_model_tasks("CoRE4INET", ["inet"])
        fico4omnet = create_all_model_tasks("FiCo4OMNeT", [])
        openflow = create_all_model_tasks("OpenFlow", ["inet"])
        signalsandgateways = create_all_model_tasks("SignalsAndGateways", ["CoRE4INET","FiCo4OMNeT"])
        soa4core = create_all_model_tasks("SOA4CoRE", ["SignalsAndGateways"])
        sdn4core = create_all_model_tasks("SDN4CoRE", ["OpenFlow","SOA4CoRE"])
        cleanall = create_task_clean_all(["inet", "CoRE4INET","FiCo4OMNeT", "OpenFlow", "SignalsAndGateways", "SOA4CoRE", "SDN4CoRE"])
        buildallrelease = create_task_build_all(["inet", "CoRE4INET","FiCo4OMNeT", "OpenFlow", "SignalsAndGateways", "SOA4CoRE", "SDN4CoRE"], "release")
        buildalldebug = create_task_build_all(["inet", "CoRE4INET","FiCo4OMNeT", "OpenFlow", "SignalsAndGateways", "SOA4CoRE", "SDN4CoRE"], "debug")
        runTasks = create_run_tasks()

        output = OrderedDict([
            ("version", "2.0.0"),
            ("tasks", inet + core4inet + fico4omnet + openflow + signalsandgateways + soa4core + sdn4core + cleanall + buildallrelease + buildalldebug + runTasks)
        ])
        #write to file
        f.write(json.dumps(output, indent=4, separators=(',', ': ')))
