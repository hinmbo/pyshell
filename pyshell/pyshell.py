# Standard Python Library
import os
import sys

# Third Party Library
from rich.theme import Theme
from rich.console import Console

# Local Library
try:
    from shared import utils, pyfetch
except ImportError:
    from shared import utils, pyfetch


pyshell_theme = Theme({
    "pygreen" : "bold #23d18b",
    "pyblue" : "bold blue",
    "warning" : "bold red"
})

console = Console(log_time=False, log_path=False, theme=pyshell_theme)
print = console.print
input = console.input

###################
# HELPER FUNCTION #
###################
def run_command(command, args):
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
        print(f"[bold red]'{command}' is not a recognized command.")


#################
# MAIN FUNCTION #
#################

def main():

    utils.print_intro()

    while True:
        if utils.dir_show_on:
            command_line = input(f"\n{os.getcwd()}> ").strip()
        else:
            command_line = input("\n> ").strip()

        if command_line.lower() in ["exit", "quit", "q"]:
            sys.exit(0)
        parts = command_line.lower().split()
        
        if not parts:
            continue
        command, *args = parts
        run_command(command, args)


if __name__ == "__main__":
    main()