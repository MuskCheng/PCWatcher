import requests

class PushMeClient:
    def __init__(self, push_key):
        self.push_key = push_key
        self.api_url = "https://push.i-i.me"
    
    def send(self, title, content, msg_type="markdown"):
        if not self.push_key:
            return False, "push_key is empty"
        
        data = {
            "push_key": self.push_key,
            "title": title,
            "content": content,
            "type": msg_type
        }
        
        try:
            resp = requests.post(self.api_url, data=data, timeout=10)
            result = resp.text
            if result == "success":
                return True, "success"
            return False, result
        except Exception as e:
            return False, str(e)
    
    def _get_device_display(self, device_info):
        device_name = device_info.get("device_name", "")
        hostname = device_info.get("hostname", "")
        
        if device_name:
            return f"({device_name}) [{hostname}]"
        else:
            return f"[{hostname}]"
    
    def send_status(self, cpu, mem, disks, net, device_info):
        device_display = self._get_device_display(device_info)
        title = f"{device_display} PCWatcher 系统状态"
        
        content = f"## 📊 系统状态 - {device_display}\n\n"
        
        content += "| 项目 | 数值 |\n"
        content += "|------|------|\n"
        
        content += f"| 💻 CPU | **{cpu:.1f}%**\n"
        
        content += f"| 📊 内存 | **{mem['used']:.1f}GB** / {mem['total']:.1f}GB (**{mem['percent']:.1f}%**)\n"
        
        for disk in disks:
            content += f"| 💾 磁盘{disk['mountpoint']} | **{disk['used']:.1f}GB** / {disk['total']:.1f}GB (**{disk['percent']:.1f}%**)\n"
        
        if net:
            upload = net.get('upload_speed', 0) / 1024
            download = net.get('download_speed', 0) / 1024
            content += f"| ⬆️ 上传 | **{upload:.1f} KB/s**\n"
            content += f"| ⬇️ 下载 | **{download:.1f} KB/s**\n"
            if net.get('ip'):
                content += f"| 🌐 IP | **{net['ip']}**\n"
        
        return self.send(title, content)
    
    def send_alert(self, alerts, device_info):
        device_display = self._get_device_display(device_info)
        title = f"{device_display} PCWatcher 告警通知"
        
        content = f"## ⚠️ 监控告警 - {device_display}\n\n"
        
        content += "| 项目 | 状态 |\n"
        content += "|------|------|\n"
        
        for alert in alerts:
            content += f"| 🔴 | **{alert}**\n"
        
        return self.send(title, content)
    
    def test_connection(self, device_info=None):
        device_info = device_info or {}
        device_display = self._get_device_display(device_info)
        title = f"{device_display} PCWatcher 连接测试"
        content = "## ✅ 连接成功\n\n"
        content += "| 项目 | 状态 |\n"
        content += "|------|------|\n"
        content += "| 🔔 PushMe | **已连接** |\n"
        content += "| 📡 PCWatcher | **运行正常** |\n"
        return self.send(title, content)
