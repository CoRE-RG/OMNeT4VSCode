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

run_command = "${config:omnetppInstallDir}/bin/opp_run"
run_command_dbg = "${config:omnetppInstallDir}/bin/opp_run_dbg"
run_group = {
    "kind": "test",
    "isDefault": False
}
run_presentation_default = task_presentation_default
# run_args = [
#     "-n",
#     ".",
#     "--image-path=" + imagesPath,
#     "--ned-path=" + nedPath,
#     "-l",
#     libPath
# ]

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

        output = OrderedDict([
            ("version", "2.0.0"),
            ("tasks", inet + core4inet + fico4omnet + openflow + signalsandgateways + soa4core + sdn4core + cleanall + buildallrelease + buildalldebug)
        ])
        #write to file
        f.write(json.dumps(output, indent=4, separators=(',', ': ')))
