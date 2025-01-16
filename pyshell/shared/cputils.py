import platform
import subprocess

"""
Description: A lighter version of 'cpuinfo'.
• Windows: Fetches ProcessorNameString from the Windows registry.
• Linux: Parses /proc/cpuinfo for model name.
• macOS: Executes sysctl for machdep.cpu.brand_string.
"""
class CPUtils:
    @staticmethod
    def get_cpu_brand():
        """
        Get the CPU brand name using a lightweight approach.
        """
        system = platform.system().lower()

        if system == "windows":
            return CPUtils._get_cpu_brand_windows()
        elif system == "linux":
            return CPUtils._get_cpu_brand_linux()
        elif system == "darwin":  # macOS
            return CPUtils._get_cpu_brand_macos()
        else:
            return "Unknown CPU"

    @staticmethod
    def _get_cpu_brand_windows():
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0")
            processor_brand, _ = winreg.QueryValueEx(key, "ProcessorNameString")
            winreg.CloseKey(key)
            return processor_brand.strip()
        except Exception as e:
            return f"Error fetching CPU info on Windows: {e}"

    @staticmethod
    def _get_cpu_brand_linux():
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line.lower():
                        return line.split(":")[1].strip()
            return "Unknown CPU"
        except Exception as e:
            return f"Error fetching CPU info on Linux: {e}"

    @staticmethod
    def _get_cpu_brand_macos():
        try:
            output = subprocess.check_output([
                "sysctl", "-n", "machdep.cpu.brand_string"
            ], text=True)
            return output.strip()
        except Exception as e:
            return f"Error fetching CPU info on macOS: {e}"

