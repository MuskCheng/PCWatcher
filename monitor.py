import psutil
import time
import socket
import platform
import winreg

class SystemMonitor:
    def __init__(self):
        self._last_net_io = None
        self._last_time = None
    
    def get_cpu_percent(self):
        return psutil.cpu_percent(interval=0)
    
    def get_memory(self):
        mem = psutil.virtual_memory()
        return {
            "used": round(mem.used / (1024**3), 2),
            "total": round(mem.total / (1024**3), 2),
            "percent": mem.percent
        }
    
    def get_disks(self):
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "used": round(usage.used / (1024**3), 2),
                    "total": round(usage.total / (1024**3), 2),
                    "percent": usage.percent
                })
            except:
                pass
        return disks
    
    def get_network_info(self, interface_name=None):
        addrs = psutil.net_if_addrs()
        stats = psutil.net_io_counters(pernic=True)
        
        if interface_name and interface_name in addrs:
            ip = None
            for addr in addrs[interface_name]:
                if addr.family.name == 'AF_INET':
                    ip = addr.address
                    break
            
            current_time = time.time()
            current_stats = stats[interface_name]
            
            speed = {"upload": 0, "download": 0}
            if self._last_net_io and self._last_time:
                time_diff = current_time - self._last_time
                upload_diff = current_stats.bytes_sent - self._last_net_io.bytes_sent
                download_diff = current_stats.bytes_recv - self._last_net_io.bytes_recv
                speed["upload"] = int(upload_diff / time_diff)
                speed["download"] = int(download_diff / time_diff)
            
            self._last_net_io = current_stats
            self._last_time = current_time
            
            return {
                "interface": interface_name,
                "ip": ip,
                "upload_speed": speed["upload"],
                "download_speed": speed["download"]
            }
        return None
    
    def get_network_interfaces(self):
        return list(psutil.net_if_addrs().keys())
    
    def get_device_info(self):
        hostname = socket.gethostname()
        
        device_model = ""
        try:
            if platform.system() == "Windows":
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\BIOS")
                try:
                    system_name = winreg.QueryValueEx(key, "SystemProductName")
                    if system_name and system_name[0]:
                        device_model = system_name[0]
                except:
                    pass
                try:
                    manufacturer = winreg.QueryValueEx(key, "SystemManufacturer")
                    if manufacturer and manufacturer[0] and manufacturer[0] != "System manufacturer":
                        device_model = f"{manufacturer[0]} {device_model}".strip()
                except:
                    pass
                winreg.CloseKey(key)
        except:
            pass
        
        return {
            "hostname": hostname,
            "device_model": device_model
        }
