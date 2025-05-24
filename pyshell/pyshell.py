# Standard Python Library
import os
import sys

# Third Party Library
# Import the centralized rich.Console instance and its convenient aliases
# from the 'terminal' module, which handles all console-related operations.
from terminal import console, ps_print, ps_input

# Local Library
# Import application-specific utility modules.
# This 'try-except ImportError' block is usually used when there are
# alternative import paths or optional dependencies. If 'shared' always
# comes from the same place, this can be simplified to a single import.
try:
    from shared import utils, pyfetch
except ImportError:
    from shared import utils, pyfetch


def run_command(command, args):
    """
    Executes a command or function based on user input.

    This function acts as a dispatcher, mapping string commands to their
    corresponding utility functions within the 'utils' and 'pyfetch' modules.
    All terminal output for unrecognized commands uses the application's
    standardized 'ps_print' function for consistent styling.
    """
    commands = {
        "ps": utils.ps,
        "reset" : utils.ps,
        "mv": utils.mv,
        "cp": utils.cp,
        "cd": utils.cd,
        "ls": utils.ls,
        "dr": utils.dr,
        "dir": utils.dr,
        "cls": utils.cls,
        "clear": utils.cls,
        "pwd": utils.pwd,
        "rm": utils.rm,
        "rmdir": utils.rmdir,
        "mkdir": utils.mkdir,
        "touch": utils.touch,
        "echo": utils.echo,
        "cat": utils.cat,
        "help": utils.help,
    }
    functions = {
        "log": utils.login,
        "login": utils.login,
        "signin": utils.login,
        "signup": utils.signup,
        "sign": utils.signup,
        "pyfetch" : pyfetch.pyfetch,
        "pf" : pyfetch.pyfetch,
        "ver": utils.version,
        "version": utils.version,
    }

    if command in functions:
        functions[command]()
    elif command in commands:
        commands[command](args)
    else:
        # Use ps_print for all terminal output to maintain consistent styling.
        ps_print(f"[bold red]'{command}' is not a recognized command.")


def main():
    """
    The main entry point for the PyShell application.

    Initializes the terminal interface, displays the intro message, and
    enters a continuous loop to accept and process user commands. It handles
    exiting the application and parsing user input.
    """
    # Display the PyShell introduction message using standardized console output.
    utils.print_intro()

    while True:
        # Prompt the user for a command, displaying the current directory if 'dir_show_on' is enabled.
        # All user input is handled via 'ps_input' for consistent styling.
        if utils.dir_show_on:
            command_line = ps_input(f"\n{os.getcwd()}> ").strip()
        else:
            command_line = ps_input("\n> ").strip()

        # Handle application exit commands.
        if command_line.lower() in ["exit", "quit", "q"]:
            sys.exit(0)

        # Parse the command and its arguments.
        # If the command line is empty, continue to the next loop iteration.
        parts = command_line.lower().split()
        if not parts:
            continue

        command, *args = parts
        run_command(command, args)


if __name__ == "__main__":
    main()