"""
Clone and open a bunch of students' work by reading student IDs from stdin.
"""
from argparse import ArgumentParser
from markten import Recipe, parameters, actions
from pathlib import Path


term = "24T3"


def command_line():
    """Set up parameters from command line"""
    parser = ArgumentParser("clone_and_open.py")
    parser.add_argument("lab", nargs="+")

    return parameters.from_object(parser.parse_args(), ["lab"])


def setup(lab: str, zid: str):
    """Set up lab exercise"""
    directory = actions.git.clone(
        f"git@nw-syd-gitlab.cseunsw.tech:COMP2511/{
            term}/students/{zid}/{lab}.git",
        branch="marking",
    )
    return {
        "directory": directory,
    }


def open_code(directory: Path):
    """Open directory in VS Code"""
    return actions.editor.vs_code(directory)


def print_student_info(zid: str):
    """Look up student info"""
    return actions.process.run("ssh", "cse", "acc", zid)


marker = Recipe("COMP2511 Lab Marking")

marker.parameter("zid", parameters.stdin("zid"))
marker.parameters(command_line())

marker.step("setup repo", setup)
marker.step("view code", (open_code, print_student_info))

marker.run()
