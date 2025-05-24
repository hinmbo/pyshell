# Standard Python Library
import os
import json
import shutil
import getpass
from ctypes import windll # Used for Windows-specific file attribute manipulation (e.g., hiding folders)

# Third Party Library
import bcrypt # For password hashing
import pwinput # For masked password input (e.g., displaying '•' instead of hiding input)
from rich.markup import escape # For escaping text to be safely displayed by rich.

# Import the centralized console print and input functions for consistent terminal interaction.
from terminal import ps_print, ps_input


# --- Application Configuration and Global State ---
APPLICATION_VERSION = "Version 0.1b"
APPLICATION_DATE_VERSION = "2025.01"
USER_DATA_FOLDER = ".userdata" # Folder to store user data (e.g., hashed passwords)
USER_DATA_FILE = os.path.join(USER_DATA_FOLDER, "users.json") # Path to the user data JSON file

# Global flags and variables for PyShell's current state.
is_logged_in = False # Indicates if a user is currently authenticated.
dir_show_on = False # Controls whether the current directory is shown in the command prompt.
cur_username = "" # Stores the username of the currently logged-in user.

# System-level utility for getting the current username (not related to PyShell accounts).
getusername = getpass.getuser
# Alias for masked password input, specifically using pwinput to allow custom mask characters.
getpassword = pwinput.pwinput


# --- Rich Markup for Command Usage Examples ---
# Pre-defined escaped strings for consistent usage messages in help commands.
esc_src_dest = escape("[source] [destination]")
esc_path = escape("[path]")
esc_filename = escape("[filename(s)]")
esc_file = escape("[file(s)]")
esc_dir = escape("[directory/ies]")
esc_ech = escape("[text] [> filename (optional)]")


# --- Command and Function Help Descriptions ---
# Dictionaries mapping commands/functions to their brief descriptions for the 'help' command.
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
    "logout" : "\tLogout of the local terminal account" # This dictionary is currently unused.
}


# --- File System and User Management Helper Functions ---

def _hide_folder():
    """
    Hides the '.userdata' folder on Windows systems to prevent casual access.
    Creates the folder if it doesn't already exist.
    """
    folder_path = USER_DATA_FOLDER
    FILE_ATTRIBUTE_HIDDEN = 0x2

    # Ensure the folder exists; create it if not.
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Attempt to hide the folder using Windows API.
    # Error messages are printed using ps_print for consistent styling.
    result = windll.kernel32.SetFileAttributesW(folder_path, FILE_ATTRIBUTE_HIDDEN)
    if result == 0:
        ps_print(f"[warning]Error: Failed to hide {folder_path}")

def _hash_password(password):
    """
    Hashes a given password using bcrypt for secure storage.
    Returns the hashed password as a UTF-8 decoded string.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def _load_users():
    """
    Loads user data (usernames and hashed passwords) from the users.json file.
    Handles initial file creation if it doesn't exist and gracefully manages JSON decoding errors.
    Prints error messages using ps_print.
    """
    _hide_folder() # Ensure the user data folder is set up and hidden.

    if not os.path.exists(USER_DATA_FILE):
        # If the file doesn't exist, create an empty JSON object to initialize.
        with open(USER_DATA_FILE, 'w') as file:
            file.write("{}")
        return {}

    try:
        with open(USER_DATA_FILE, 'r') as file:
            content = file.read().strip()
            if not content: # If file is empty or only whitespace, treat as empty JSON.
                return {}
            return json.loads(content)
    except json.JSONDecodeError:
        # Log JSON parsing errors using ps_print and return an empty dict to prevent application crashes.
        ps_print(f"[warning]Error: {USER_DATA_FILE} contains invalid JSON. Initializing empty user data.")
        return {}

def _save_users(users):
    """
    Saves the current user data dictionary to the users.json file.
    Ensures the user data folder is properly set up before writing.
    """
    _hide_folder() # Ensure the user data folder is set up and hidden.
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4) # Use indent for readable JSON formatting.


# --- Core PyShell Functions ---

def print_intro():
    """
    Prints the PyShell application's introduction ASCII art and version information.
    Uses 'ps_print' for all console output to apply consistent styling defined in 'terminal.py'.
    """
    _ = os.system("cls") # Clears the terminal screen (Windows command).

    ps_print(f"PyShell - Terminal Application [pygreen][{APPLICATION_VERSION}] [pyblue]{'<' + cur_username + '>' if is_logged_in else ''}")
    ps_print("Copyright (C) PyShell Corporation. All rights reserved\n")
    ps_print("[white]██████╗░██╗░░░██╗░██████╗██╗░░██╗███████╗██╗░░░░░██╗░░░░░")
    ps_print("[white]██╔══██╗╚██╗░██╔╝██╔════╝██║░░██║██╔════╝██║░░░░░██║░░░░░")
    ps_print("[white]██████╔╝░╚████╔╝░╚█████╗░███████║█████╗░░██║░░░░░██║░░░░░")
    ps_print("[white]██╔═══╝░░░╚██╔╝░░░╚═══██╗██╔══██║██╔══╝░░██║░░░░░██║░░░░░")
    ps_print("[white]██║░░░░░░░░██║░░░██████╔╝██║░░██║███████╗███████╗███████╗")
    ps_print("[white]╚═╝░░░░░░░░╚═╝░░░╚═════╝░╚═╝░░╚═╝╚══════╝╚══════╝╚══════╝")

def help(args):
    """
    Lists all available commands and functions within PyShell.
    Displays usage information if unexpected arguments are provided.
    All output uses 'ps_print' for consistent styling.
    """
    if args:
        ps_print(f"[pyblue]Usage: help")
        return

    ps_print("[pygreen]Available Commands:")
    for command, description in command_help.items():
        ps_print(f"  {command} {description}")

    ps_print("\n[pygreen]Available Functions:")
    for function, description in function_help.items():
        ps_print(f"  {function} {description}")

def mv(args):
    """
    Moves a file or directory from a source to a destination.
    Handles insufficient arguments and catches general file system errors.
    """
    if len(args) < 2:
        ps_print(f"[pyblue]Usage: mv {esc_src_dest}")
        return

    source, destination = args
    try:
        shutil.move(source, destination)
    except Exception as e: # Catch the actual exception for more informative error messages.
        ps_print(f"[warning]Error moving {source}: {e}")

def cp(args):
    """
    Copies a file or directory from a source to a destination.
    Handles copying of both files and directories, and catches general file system errors.
    """
    if len(args) < 2:
        ps_print(f"[pyblue]Usage: cp {esc_src_dest}")
        return

    source, destination = args
    try:
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy(source, destination)
    except Exception as e:
        ps_print(f"[warning]Error copying '{source}': {e}")

def cd(args):
    """
    Changes the current working directory.
    Handles insufficient arguments and invalid paths by catching OS-related exceptions.
    """
    if len(args) < 1:
        ps_print(f"[pyblue]Usage: cd {esc_path}")
        return

    path = args[0]
    try:
        os.chdir(path)
    except Exception as e: # Catches common OS errors (e.g., FileNotFoundError, NotADirectoryError).
        ps_print(f"[warning]Error changing directory: {e}")

def ls(args):
    """
    Lists files and directories in a specified path, or the current directory if no path is given.
    Displays items in blue and handles directory listing errors.
    """
    path = args[0] if args else "."
    try:
        items = os.listdir(path)
        for item in items:
            ps_print(f"[pyblue]{item}", end=" ") # Prints items on the same line.
        ps_print("") # Prints a newline after listing all items for cleaner output.
    except Exception as e:
        ps_print(f"[warning]Error listing directory '{path}': {e}")

def dr(args):
    """
    Toggles the display of the current working directory in the command prompt.
    Notifies the user whether the display is turned on or off.
    """
    global dir_show_on
    dir_show_on = not dir_show_on
    ps_print("[pygreen]Directory shown has been turned", end='')
    ps_print(f"[pygreen] {'on.' if dir_show_on else 'off.'}")

def pwd(args):
    """
    Prints the current working directory (Print Working Directory).
    Handles extraneous arguments by showing usage.
    """
    if args:
        ps_print(f"[pyblue]Usage: pwd")
        return
    ps_print(os.getcwd())

def rm(args):
    """
    Removes specified files.
    Handles insufficient arguments and catches file removal errors.
    """
    if len(args) < 1:
        ps_print(f"[pyblue]Usage: rm {esc_file}")
        return

    for file_to_remove in args:
        try:
            os.remove(file_to_remove)
        except Exception as e:
            ps_print(f"[warning]Error removing '{file_to_remove}': {e}")

def rmdir(args):
    """
    Removes empty directories.
    Handles insufficient arguments and catches directory removal errors (e.g., if not empty).
    """
    if len(args) < 1:
        ps_print(f"[pyblue]Usage: rmdir {esc_dir}")
        return

    for directory_to_remove in args:
        try:
            os.rmdir(directory_to_remove)
        except Exception as e:
            ps_print(f"[warning]Error removing directory '{directory_to_remove}': {e}")

def mkdir(args):
    """
    Creates new directories.
    Handles insufficient arguments and ensures parent directories are created if needed.
    """
    if len(args) < 1:
        ps_print(f"[pyblue]Usage: mkdir {esc_dir}")
        return

    for directory_to_create in args:
        try:
            os.makedirs(directory_to_create, exist_ok=True) # `exist_ok=True` prevents error if dir already exists.
        except Exception as e:
            ps_print(f"[warning]Error creating directory '{directory_to_create}': {e}")

def touch(args):
    """
    Creates empty files or updates the timestamp of existing files.
    Handles insufficient arguments and file creation/update errors.
    """
    if len(args) < 1:
        ps_print(f"[pyblue]Usage: touch {esc_filename}")
        return

    for filename_to_touch in args:
        try:
            # Open in append mode ('a') to create if not exists, then close.
            # os.utime then updates access/modification times to current without changing content.
            with open(filename_to_touch, 'a'):
                os.utime(filename_to_touch, None)
        except Exception as e:
            ps_print(f"[warning]Error creating '{filename_to_touch}': {e}")

def echo(args):
    """
    Prints text to the console or redirects it to a file.
    Supports basic redirection using the '>' operator.
    """
    if len(args) < 1:
        ps_print(f"[pyblue]Usage: echo {esc_ech}")
        return

    if ">" in args:
        file_index = args.index(">")
        if file_index + 1 >= len(args): # Ensure a filename is provided after '>'.
            ps_print("[warning]Error: No filename provided after '>'")
            return

        text = " ".join(args[:file_index])
        filename = args[file_index + 1]

        try:
            with open(filename, 'w') as f: # Use 'w' to overwrite, 'a' to append.
                f.write(text + '\n') # Add newline for clarity in the file.
        except Exception as e:
            ps_print(f"[warning]Error in echo: {e}")
    else:
        ps_print(" ".join(args)) # Print to console directly if no redirection.

def cat(args):
    """
    Displays the contents of a specified file.
    Handles insufficient arguments and file reading errors.
    """
    if len(args) < 1:
        ps_print(f"[pyblue]Usage: cat {esc_filename}")
        return
    filename = args[0]
    try:
        with open(filename, 'r') as f:
            ps_print(f.read()) # Reads and prints the entire file content.
    except Exception as e:
        ps_print(f"[warning]Error reading '{filename}': {e}")

def ps(args):
    """
    Resets (clears) the terminal screen and redisplays the PyShell introduction.
    Handles extraneous arguments by showing usage.
    """
    if args:
        ps_print("[pyblue]Usage: ps")
        return
    _ = os.system("cls") # Clear screen (platform-dependent, e.g., 'cls' for Windows).
    print_intro() # Redisplay the introductory message.

def cls(args):
    """
    Clears the terminal screen.
    Handles extraneous arguments by showing usage.
    """
    if args:
        ps_print("[pyblue]Usage: cls")
        return # Added return here to prevent clearing if usage is printed.
    _ = os.system("cls") # Clear screen (platform-dependent).


def version():
    """
    Displays the current version details of the PyShell application.
    """
    ps_print(f"[bold white]PyShell — [pygreen]{APPLICATION_VERSION} ({APPLICATION_DATE_VERSION})")

def login():
    """
    Allows a user to log in to an existing PyShell account.
    Validates credentials against stored hashed passwords and updates global login state.
    """
    global cur_username
    global is_logged_in
    users = _load_users()

    username = ps_input("[bold]Username: ").strip()
    if username not in users:
        ps_print("[warning]Error: User does not exist.")
        return

    # Use pwinput.pwinput for masked password input with a specific character (e.g., '•').
    ps_print("[bold]Password: ", end=""); password = getpassword("", mask="•")

    # Validate user credentials using bcrypt.
    stored_hash = users[username].encode() # Convert stored hash to bytes for bcrypt comparison.
    if bcrypt.checkpw(password.encode(), stored_hash):
        cur_username = username
        is_logged_in = True
        ps_print("[pygreen]<> Logged in successfully!")
    else:
        ps_print("[warning]Error: Incorrect password.")

def signup():
    """
    Registers a new user account for PyShell.
    Handles checks for existing usernames, password mismatches, and securely hashes passwords for storage.
    """
    users = _load_users()

    username = ps_input("[bold]Username: ").strip()
    if username in users:
        ps_print("[warning]Error: Username already exists!")
        return

    # Use pwinput.pwinput for masked password input with a specific character (e.g., '•').
    ps_print("[bold]Password: ", end=""); password = getpassword("", mask="•")
    ps_print("[bold]Retype password: ", end=""); confirm_password = getpassword("", mask="•") # Added mask here too.

    if password != confirm_password:
        ps_print("[warning]Error: Passwords do not match.")
        return

    hashed_password = _hash_password(password)
    users[username] = hashed_password
    _save_users(users)
    ps_print(f"[bold]<> '{username}' has been created successfully")