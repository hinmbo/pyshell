"""
This module centralizes the configuration and instantiation of the rich.Console
object and its associated Theme for the PyShell application.

By defining these core terminal interaction components here, we ensure:
- A single, consistent source for all terminal output and input styling.
- Avoidance of redundant code and potential inconsistencies across modules.
- Easy modification of the application's visual theme and console behavior
  from a single, authoritative location.

Other modules throughout PyShell should import the 'console', 'ps_print',
or 'ps_input' objects from this module to ensure all terminal interactions
are styled and managed consistently.
"""

from rich.console import Console
from rich.theme import Theme

# Define PyShell's custom theme for rich console output
pyshell_theme = Theme({
    "pygreen" : "bold #23d18b",
    "pyblue" : "bold blue",
    "warning" : "bold red"
})

# Create the main rich.Console instance for PyShell
# This console will be used for all styled printing and input throughout the application.
console = Console(log_time=False, log_path=False, theme=pyshell_theme)

# Expose convenient aliases for print and input using the centralized console
ps_print = console.print
ps_input = console.input