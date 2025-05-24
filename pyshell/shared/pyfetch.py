# Standard Python Library
import socket     # For getting hostname
import datetime   # For calculating uptime
import platform   # For general OS and kernel information

# Third Party Library
import GPUtil                   # For GPU information
import psutil                   # For system resource monitoring (CPU, Memory, Uptime)
from rich.table import Table    # For displaying information in a structured table
from screeninfo import get_monitors # For retrieving screen resolution

# Import the centralized console print function for consistent terminal output.
from terminal import ps_print

# Local Library
from shared.cputils import CPUtils # Custom utility for CPU brand information


def _get_os():
    """Retrieves detailed operating system information."""
    os_name = platform.system()
    os_version = platform.version()
    os_release = platform.release()
    return f"{os_name} {os_release} (v{os_version})"

def _get_hostname():
    """Retrieves the hostname of the current machine."""
    return socket.gethostname()

def _get_kernel():
    """Retrieves information about the operating system kernel."""
    uname_info = platform.uname()
    if uname_info.system == "Windows":
        return f"Windows NT Kernel" # Windows kernel doesn't typically have a simple version like Linux.
    elif uname_info.system == "Linux":
        return uname_info.release # This usually gives the kernel version (e.g., "5.15.0-101-generic").
    elif uname_info.system == "Darwin": # macOS
        return f"Darwin Kernel (Release: {uname_info.release})"
    else:
        return uname_info.system # Fallback for other less common OSes.

def _get_uptime():
    """Calculates and returns the system uptime as a timedelta object."""
    return datetime.timedelta(seconds=(psutil.time.time() - psutil.boot_time()))

def _get_screen_res():
    """
    Retrieves the screen resolution(s) of all connected monitors using screeninfo.
    Returns "Unavailable" if an error occurs during retrieval.
    """
    try:
        resolutions = []
        for monitor in get_monitors():
            resolutions.append(f"{monitor.width}x{monitor.height}")
        return ", ".join(resolutions)
    except Exception: # Broad exception catch for external library issues.
        return "Unavailable"

def _get_cpu():
    """Retrieves CPU brand, physical core count, and logical core (thread) count."""
    cpu_proc = CPUtils.get_cpu_brand()
    cpu_logical_cores = psutil.cpu_count(logical=True)
    cpu_physical_cores = psutil.cpu_count(logical=False)
    return f"{cpu_proc} ({cpu_physical_cores}C / {cpu_logical_cores}T)"

def _get_gpu():
    """
    Retrieves GPU information, including name and total VRAM, using GPUtil.
    Returns "GPU not detected" or "GPU information unavailable" if no GPUs are found or an error occurs.
    """
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return "GPU not detected."

        gpu_info_list = []
        for gpu in gpus:
            gpu_info_list.append(f"{gpu.name} (VRAM: {int(gpu.memoryTotal)}MB)")
        return ", ".join(gpu_info_list)
    except Exception as e:
        # It's good practice to log or print the actual exception for debugging purposes,
        # even if not shown to the end-user.
        # print(f"DEBUG: Error in _get_gpu: {e}")
        return "GPU information unavailable"

def _get_mem():
    """Retrieves current memory usage and total available memory in MB."""
    mem = psutil.virtual_memory()
    return f"{mem.used // (1024**2)}MB / {mem.total // (1024**2)}MB"


def pyfetch():
    """
    Gathers comprehensive system information and displays it in a neatly formatted table,
    mimicking the style of `neofetch`.
    It uses various internal helper functions to collect data and relies on `ps_print`
    for consistent terminal output.
    """
    # Collect all required system information from helper functions.
    os_info = _get_os()
    host_name = _get_hostname()
    kernel = _get_kernel()
    uptime = _get_uptime()
    shell = "pyshell" # The shell's name is fixed for pyfetch output.
    screen_res = _get_screen_res()
    cpu_info = _get_cpu()
    gpu_info = _get_gpu()
    memory = _get_mem()

    # Create a rich Table object to structure the system information.
    table = Table()
    table.add_column("pyfetch") # Column for the information type (e.g., "OS", "Host").
    table.add_column("System Information", style="bold #23d18b", no_wrap=False) # Column for the actual data.

    # Add rows to the table with collected system data.
    # 'end_section=True' adds a visual line after "Resolution" for better grouping.
    table.add_row(f"OS", os_info)
    table.add_row(f"Host", host_name)
    table.add_row(f"Kernel", kernel)
    table.add_row(f"Uptime", str(uptime))
    table.add_row(f"Shell", shell)
    table.add_row(f"Resolution", str(screen_res), end_section=True)
    table.add_row(f"CPU", cpu_info)
    table.add_row(f"GPU", gpu_info)
    table.add_row(f"Memory", memory)

    # Print the fully constructed table to the console using the shared ps_print function.
    ps_print(table)