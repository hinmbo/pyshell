# Standard Python Library
import os
import json
import shutil
import getpass

# Third Party Library
import bcrypt
import pwinput
from ctypes import windll
from rich.theme import Theme
from rich.markup import escape
from rich.console import Console

APPLICATION_VERSION = "Version 0.1b"
APPLICATION_DATE_VERSION = "2025.01"
USER_DATA_FOLDER = ".userdata"
USER_DATA_FILE = os.path.join(USER_DATA_FOLDER, "users.json")
is_logged_in = False
dir_show_on = False
cur_username = ""

pyshell_theme = Theme({
    "pygreen" : "bold #23d18b",
    "pyblue" : "bold blue",
    "warning" : "bold red"
})

console = Console(log_time=False, log_path=False, theme=pyshell_theme)
print = console.print
input = console.input
getusername = getpass.getuser
getpassword = pwinput.pwinput

esc_src_dest = escape("[source] [destination]")
esc_path = escape("[path]")
esc_filename = escape("[filename(s)]")
esc_file = escape("[file(s)]")
esc_dir = escape("[directory/ies]")
esc_ech = escape("[text] [> filename (optional)]")

command_help = {
    "ps": "\t\tResets the terminal.",
    "mv": "\t\tMove a file or directory.",
    "cp": "\t\tCopy a file or directory.",
    "cd": "\t\tChange the current directory.",
    "ls": "\t\tList files in a directory.",
    "dr": "\t\tDisplays the current working directory alongside.",
    "cls": "\t\tClears up the terminal",
    "pwd": "\t\tPrint the current working directory.",
    "rm": "\t\tRemove a file.",
    "rmdir": "\tRemove an empty directory.",
    "mkdir": "\tCreate a new directory.",
    "touch": "\tCreate an empty file or update its timestamp.",
    "echo": "\t\tPrint text or write to a file.",
    "cat": "\t\tDisplay the contents of a file.",
    "help": "\t\tList all available commands.",
    "exit": "\t\tExit the application.",
}
function_help = {

    "login": "\tLogin into local terminal account.",
    "signup": "\tSignup into local terminal account.",
    "pyfetch": "\tNeofetch look-alike contest, pyfetch lost.",
    "version": "\tDisplays the current version of Pyshell."

}

function_help_if_logged_in = {
    "logout" : "\tLogout of the local terminal account"
    
}

def _hide_folder():
    """Hide userdata folder"""
    folder_path = USER_DATA_FOLDER
    FILE_ATTRIBUTE_HIDDEN = 0x2
    
    # Check if the folder exists; create it if not
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Attempt to hide the folder
    result = windll.kernel32.SetFileAttributesW(folder_path, FILE_ATTRIBUTE_HIDDEN)
    if result == 0:
        print(f"[warning]Error: Failed to hide {folder_path}")

def _hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
 
def _load_users():
    """Load user data from the JSON file"""
    _hide_folder()

    if not os.path.exists(USER_DATA_FILE):
        # File doesn't exist; create an empty file with {}
        with open(USER_DATA_FILE, 'w') as file:
            file.write("{}")
        return {}    
    
    try:
        with open(USER_DATA_FILE, 'r') as file:
            content = file.read().strip()
            if not content:  # Check if the file is empty
                return {}
            return json.loads(content)
    except json.JSONDecodeError:
        print(f"[warning]Error: {USER_DATA_FILE} contains invalid JSON. Initializing empty user data.")
        return {}

def _save_users(users):
    """Save the user data to the JSON file"""
    _hide_folder()
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def print_intro():
    """Prints PyShell's introduction"""
    _ = os.system("cls")
    
    print(f"PyShell - Terminal Application [pygreen][{APPLICATION_VERSION}] [pyblue]{'<' + cur_username + '>' if is_logged_in else ''}")
    print("Copyright (C) PyShell Corporation. All rights reserved\n")
    print("[white]██████╗░██╗░░░██╗░██████╗██╗░░██╗███████╗██╗░░░░░██╗░░░░░")
    print("[white]██╔══██╗╚██╗░██╔╝██╔════╝██║░░██║██╔════╝██║░░░░░██║░░░░░")
    print("[white]██████╔╝░╚████╔╝░╚█████╗░███████║█████╗░░██║░░░░░██║░░░░░")
    print("[white]██╔═══╝░░░╚██╔╝░░░╚═══██╗██╔══██║██╔══╝░░██║░░░░░██║░░░░░")
    print("[white]██║░░░░░░░░██║░░░██████╔╝██║░░██║███████╗███████╗███████╗")
    print("[white]╚═╝░░░░░░░░╚═╝░░░╚═════╝░╚═╝░░╚═╝╚══════╝╚══════╝╚══════╝")

def help(args):
    """Lists all available commands and functions within PyShell"""
    if args:
        print("[pyblue]Usage: help")
        return

    print("[pygreen]Available Commands:")
    for command, description in command_help.items():
        print(f"  {command} {description}")

    print("\n[pygreen]Available Functions:")
    for function, description in function_help.items():
        print(f"  {function} {description}")  

def mv(args):
    if len(args) < 2:
        print(f"[pyblue]Usage: mv {esc_src_dest}")
        return
    
    source, destination = args
    try:
        shutil.move(source, destination)
    except Exception:
        print(f"[warning]Error moving {source}: {Exception}")

def cp(args):
    if len(args) < 2:
        print(f"[pyblue]Usage: cp {esc_src_dest}")
        return

    source, destination = args
    try:
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy(source, destination)
    except Exception:
        print(f"[warning]Error copying '{source}': {Exception}")

def cd(args):
    if len(args) < 1:
        print(f"[pyblue]Usage: cd {esc_path}")
        return
    
    path = args[0]
    try:
        os.chdir(path)
    except Exception:
        print(f"[warning]Error changing directory: {Exception}")
    
def ls(args):

    path = args[0] if args else "."
    try:
        items = os.listdir(path)
        for items in items:
            print(f"[pyblue]{items}", end=" ")
        print("")
    except Exception:
        print(f"[warning]Error listing directory '{path}': {Exception}")

def dr(args):
    global dir_show_on
    dir_show_on = not dir_show_on
    print("[pygreen]Directory shown has been turned", end='')
    print(f"[pygreen] {'on.' if dir_show_on else 'off.'}")
    

def pwd(args):
    if args:
        print(f"[pyblue]Usage: pwd")
        return
    print(os.getcwd())  

def rm(args):
    if len(args) < 1:
        print(f"[pyblue]Usage: rm {esc_file}")
        return
    
    for file in args:
        try:
            os.remove(file)
        except Exception:
            print(f"[warning]Error removing '{file}': {Exception}")

def rmdir(args):
    if len(args) < 1:
        print(f"[pyblue]Usage: rmdir {esc_dir}")
        return
    
    for directory in args:
        try:
            os.rmdir(directory)
        except Exception:
            print(f"[warning]Error removing directory '{directory}: {Exception}")

def mkdir(args):
    if len(args) < 1:
        print(f"[pyblue]Usage: mkdir {esc_dir}")
        return

    for directory in args:
        try:
            os.makedirs(directory, exist_ok=True)
        except Exception:
            print(f"[warning]Error creating directory '{directory}': {Exception}")

def touch(args):
    if len(args) < 1:
        print(f"[pyblue]Usage: touch {esc_filename}")
        return
    

    for filename in args:
        try:
            with open(filename, 'a'):
                os.utime(filename, None)
        except Exception:
            print(f"[warning]Error creating '{filename}': {Exception}")

def echo(args):
    if len(args) < 1:
        print(f"[pyblue]Usage: echo {esc_ech}")
        return

    if ">" in args:
        file_index = args.index(">")
        if file_index + 1 >= len(args):  # To ensure there's a filename after ">"
            print("[warning]Error: No filename provided after '>'")
            return

        text = " ".join(args[:file_index])
        filename = args[file_index + 1]

        try:
            with open(filename, 'w') as f:  # Replace 'w' with 'a' for appending instead of overwriting
                f.write(text + '\n')  # Proper concatenation
        except Exception as e:
            print(f"[warning]Error in echo: {e}")
    else:
        print(" ".join(args))

def cat(args):
    if len(args) < 1:
        print(f"[pyblue]Usage: cat {esc_filename}")
        return
    filename = args[0]
    try:
        with open(filename, 'r') as f:
            print(f.read())
    except Exception:
        print(f"[warning]Error reading '{filename}: {Exception}")

def ps(args):
    if args:
        print("[pyblue]Usage: ps")
    _ = os.system("cls")
    print_intro()

def cls(args):
    if args:
        print("[pyblue]Usage: cls")
    _ = os.system("cls")

        
def version():
    
    print(f"[bold white]PyShell — [pygreen]{APPLICATION_VERSION} ({APPLICATION_DATE_VERSION})")

def login():
    """Log in into a existing user"""
    global cur_username
    global is_logged_in
    users = _load_users()
    
    username = input("[bold]Username: ").strip()
    if username not in users:
        print("[warning]Error: User does not exist.")
        return
    
    print("[bold]Password: ", end=""); password = getpassword("", mask="•")
    
    # Validate user credentials
    stored_hash = users[username].encode() # Convert stored hash to bytes
    if bcrypt.checkpw(password.encode(), stored_hash):
        cur_username = username
        is_logged_in = True
        print("[pygreen]<> Logged in successfully!")
    else:
        print("[warning]Error: Incorrect password.")

def signup():
    """Register a new user"""
    users = _load_users()

    username = input("[bold]Username: ").strip()
    if username in users:
        print("[warning]Error: Username already exists!")
        return

    print("[bold]Password: ", end=""); password = getpassword("", mask="•")
    print("[bold]Retype password: ", end=""); confirm_password = getpassword("", "•")

    if password != confirm_password:
        print("[warning]Error: Passwords do not match.")
        return
    
    hashed_password = _hash_password(password)
    users[username] = hashed_password
    _save_users(users)
    print(f"[bold]<> '{username}' has been created successfully")

