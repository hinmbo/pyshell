# Standard Python Library
import socket
import datetime
import platform

# Third Party Library
import GPUtil
import psutil
from rich.live import Live
from rich.table import Table
from screeninfo import get_monitors

# Local Library
from shared.cputils import CPUtils

def _get_os():
    os_name = platform.system()
    os_version = platform.version()
    os_release = platform.release()
    return f"{os_name} {os_release} (Version: {os_version})"

def _get_hostname():
    return socket.gethostname()

def _get_kernel():
    kernel_v = platform.uname()
    if kernel_v != "95":
        return "Windows NT kernel"
    else:
        return kernel_v

def _get_uptime():
    return datetime.timedelta(seconds=(psutil.time.time() - psutil.boot_time()))

def _get_screen_res():
    """Get screen resolution using screeninfo"""
    try:
        resolutions = []
        for monitor in get_monitors():
            resolutions.append(f"{monitor.width}x{monitor.height}")
        return ", ".join(resolutions)
    except Exception:
        return "Unavailable"
    
def _get_cpu():
    cpu_proc = CPUtils.get_cpu_brand()
    cpu_threads = psutil.cpu_count(logical=True)
    cpu_cores = cpu_threads / 2
    return f"{cpu_proc} ({int(cpu_cores)}C / {cpu_threads}T)"

def _get_gpu():
    gpus = GPUtil.getGPUs()

    if not gpus:
        return f"GPU not detected."
    
    try:
        for i, gpu in enumerate(gpus):
            gpu_id = gpu.id
            gpu_name = gpu.name
            gpu_mem_total = gpu.memoryTotal
        return f"{gpu_name} (VRAM: {int(gpu_mem_total)}MB)"
    except Exception:
        return f"GPU information unavailable"
    

def _get_mem():
    mem = psutil.virtual_memory()
    return f"{mem.used // (1024**2)}MB / {mem.total // (1024**2)}MB"


def pyfetch():
    """
    Local pyfetch function that stores from the local pyfetch module and displays 
    the system information in neofetch-like way, but not nearly as well.
    """

    # OS
    os_info = _get_os()

    # Host
    host_name = _get_hostname()

    # Kernel
    kernel = _get_kernel()

    # Uptime
    uptime = _get_uptime()

    # Shell
    shell = "pyshell" # :)

    # Screen resolution
    screen_res = _get_screen_res()

    # CPU
    cpu_info = _get_cpu()
    
    # GPU
    gpu_info = _get_gpu()

    # Memory
    memory = _get_mem()

    # pyfetch table representation 
    table = Table()
    table.add_column("pyfetch")
    table.add_column("System Information", style="bold #23d18b", no_wrap=False)

    with Live(table, refresh_per_second=4):
        table.add_row(f"OS", os_info)
        table.add_row(f"Host", host_name)
        table.add_row(f"Kernel", kernel)
        table.add_row(f"Uptime", str(uptime))
        table.add_row(f"Shell", shell)
        table.add_row(f"Resolution", str(screen_res), end_section=True)
        table.add_row(f"CPU", cpu_info)
        table.add_row(f"GPU", gpu_info)
        table.add_row(f"Memory", memory)