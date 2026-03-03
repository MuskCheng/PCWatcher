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
    
    def send_status(self, cpu, mem, disks, net):
        title = "[#PCWatcher!监控]系统状态"
        
        content = "## 📊 系统状态\n\n"
        
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
    
    def send_alert(self, alerts):
        title = "[w][#PCWatcher!警告]告警通知"
        
        content = "## ⚠️ 监控告警\n\n"
        
        content += "| 项目 | 状态 |\n"
        content += "|------|------|\n"
        
        for alert in alerts:
            content += f"| 🔴 | **{alert}**\n"
        
        return self.send(title, content)
    
    def test_connection(self):
        title = "[s][#PCWatcher!成功]连接测试"
        content = "## ✅ 连接成功\n\n"
        content += "| 项目 | 状态 |\n"
        content += "|------|------|\n"
        content += "| 🔔 PushMe | **已连接** |\n"
        content += "| 📡 PCWatcher | **运行正常** |\n"
        return self.send(title, content)
