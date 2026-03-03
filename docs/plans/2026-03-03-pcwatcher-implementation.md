# PCWatcher Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现一个 Windows 系统托盘监控工具，监控 CPU/内存/硬盘/网络状态，通过 PushMe 推送告警

**Architecture:** 
- 主程序入口创建系统托盘，后台运行监控循环
- 配置使用 JSON 文件持久化，首次启动引导配置
- 监控模块定时采集系统信息，阈值比对后触发通知
- 使用 pystray 实现托盘图标和菜单，tkinter 实现配置窗口

**Tech Stack:** Python 3.x + pystray + tkinter + psutil + requests

---

## Task 1: 项目基础结构搭建

**Files:**
- Create: `D:\repositories\PCWatcher\requirements.txt`
- Create: `D:\repositories\PCWatcher\pcwatcher.py`
- Create: `D:\repositories\PCWatcher\config.json`

**Step 1: 创建 requirements.txt**

```txt
pystray>=0.19.3
psutil>=5.9.0
Pillow>=9.0.0
requests>=2.28.0
```

**Step 2: 创建基础程序入口 pcwatcher.py**

```python
import sys
import os

def main():
    print("PCWatcher starting...")
    # TODO: 实现托盘逻辑
    
if __name__ == "__main__":
    main()
```

**Step 3: 创建默认配置 config.json**

```json
{
  "push_key": "",
  "cpu_threshold": 80,
  "cpu_temp_threshold": 70,
  "memory_threshold": 85,
  "disk_thresholds": {},
  "network_interface": "",
  "network_upload_threshold": 10485760,
  "network_download_threshold": 10485760,
  "interval": 30,
  "first_run": true
}
```

**Step 4: 测试运行**

Run: `cd D:\repositories\PCWatcher && python pcwatcher.py`
Expected: 输出 "PCWatcher starting..."

**Step 5: Commit**

```bash
git add requirements.txt pcwatcher.py config.json
git commit -m "chore: init PCWatcher project structure"
```

---

## Task 2: 配置管理模块

**Files:**
- Create: `D:\repositories\PCWatcher\config_manager.py`
- Create: `D:\repositories\PCWatcher\tests\test_config_manager.py`

**Step 1: 编写测试**

```python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_load_config():
    from config_manager import ConfigManager
    cm = ConfigManager()
    assert "cpu_threshold" in cm.config
    assert cm.config["cpu_threshold"] == 80

def test_save_config():
    from config_manager import ConfigManager
    cm = ConfigManager()
    cm.config["cpu_threshold"] = 90
    cm.save()
    
    cm2 = ConfigManager()
    assert cm2.config["cpu_threshold"] == 90
```

**Step 2: 运行测试验证失败**

Run: `python -m pytest tests/test_config_manager.py -v`
Expected: FAIL (模块不存在)

**Step 3: 实现配置管理模块**

```python
import json
import os

class ConfigManager:
    def __init__(self):
        self.config_dir = os.path.join(os.environ.get('APPDATA', '.'), 'PCWatcher')
        self.config_path = os.path.join(self.config_dir, 'config.json')
        self._ensure_config_dir()
        self.config = self._load()
    
    def _ensure_config_dir(self):
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def _load(self):
        default_config = {
            "push_key": "",
            "cpu_threshold": 80,
            "cpu_temp_threshold": 70,
            "memory_threshold": 85,
            "disk_thresholds": {},
            "network_interface": "",
            "network_upload_threshold": 10485760,
            "network_download_threshold": 10485760,
            "interval": 30,
            "first_run": True
        }
        
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return {**default_config, **config}
        return default_config
    
    def save(self):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def is_first_run(self):
        return self.config.get("first_run", True)
    
    def mark_configured(self):
        self.config["first_run"] = False
        self.save()
```

**Step 4: 运行测试验证通过**

Run: `python -m pytest tests/test_config_manager.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add config_manager.py tests/test_config_manager.py
git commit -m "feat: add config manager module"
```

---

## Task 3: 系统监控模块

**Files:**
- Create: `D:\repositories\PCWatcher\monitor.py`
- Create: `D:\repositories\PCWatcher\tests\test_monitor.py`

**Step 1: 编写测试**

```python
def test_get_cpu_percent():
    from monitor import SystemMonitor
    m = SystemMonitor()
    cpu = m.get_cpu_percent()
    assert 0 <= cpu <= 100

def test_get_memory():
    from monitor import SystemMonitor
    m = SystemMonitor()
    mem = m.get_memory()
    assert "percent" in mem
    assert 0 <= mem["percent"] <= 100
```

**Step 2: 运行测试验证失败**

Run: `python -m pytest tests/test_monitor.py -v`
Expected: FAIL

**Step 3: 实现监控模块**

```python
import psutil
import time

class SystemMonitor:
    def __init__(self):
        self._last_net_io = None
        self._last_time = None
    
    def get_cpu_percent(self):
        return psutil.cpu_percent(interval=1)
    
    def get_cpu_temp(self):
        try:
            import wmi
            w = wmi.WMI()
            for temp in w.Win32_TemperatureProbe():
                if temp.CurrentReading:
                    return float(temp.CurrentReading) / 10.0
        except:
            pass
        return None
    
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
```

**Step 4: 运行测试验证通过**

Run: `python -m pytest tests/test_monitor.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add monitor.py tests/test_monitor.py
git commit -m "feat: add system monitor module"
```

---

## Task 4: PushMe 通知模块

**Files:**
- Create: `D:\repositories\PCWatcher\notifier.py`
- Create: `D:\repositories\PCWatcher\tests\test_notifier.py`

**Step 1: 编写测试**

```python
def test_pushme_client_init():
    from notifier import PushMeClient
    client = PushMeClient("test_key")
    assert client.push_key == "test_key"
```

**Step 2: 运行测试验证失败**

Run: `python -m pytest tests/test_notifier.py -v`
Expected: FAIL

**Step 3: 实现 PushMe 客户端**

```python
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
    
    def send_warning(self, title, alerts):
        content = "\n".join([f"- {alert}" for alert in alerts])
        return self.send(f"[w] {title}", content)
    
    def test_connection(self):
        return self.send("PCWatcher", "测试连接成功！")
```

**Step 4: 运行测试验证通过**

Run: `python -m pytest tests/test_notifier.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add notifier.py tests/test_notifier.py
git commit -m "feat: add PushMe notification module"
```

---

## Task 5: 系统托盘模块

**Files:**
- Create: `D:\repositories\PCWatcher\tray.py`
- Create: `D:\repositories\PCWatcher\tests\test_tray.py`

**Step 1: 编写测试**

```python
def test_tray_icon_creation():
    # pystray 需要图形环境，跳过实际创建
    from tray import create_icon
    assert create_icon is not None
```

**Step 2: 运行测试**

Run: `python -m pytest tests/test_tray.py -v`
Expected: PASS (跳过或基本检查)

**Step 3: 实现托盘模块**

```python
import pystray
from PIL import Image, ImageDraw
import threading

def create_icon_image(color="green"):
    colors = {
        "green": (0, 200, 0),
        "yellow": (255, 200, 0),
        "red": (255, 0, 0)
    }
    rgb = colors.get(color, colors["green"])
    
    image = Image.new('RGB', (64, 64), color=rgb)
    draw = ImageDraw.Draw(image)
    draw.ellipse([8, 8, 56, 56], fill='white')
    draw.text((20, 25), "PC", fill=rgb)
    return image

class SystemTray:
    def __init__(self, on_show_status, on_show_config, on_quit):
        self.on_show_status = on_show_status
        self.on_show_config = on_show_config
        self.on_quit = on_quit
        self.icon = None
        self.current_status = "green"
    
    def create_menu(self):
        return pystray.Menu(
            pystray.MenuItem("当前状态", self._on_show_status),
            pystray.MenuItem("配置设置", self._on_show_config),
            pystray.MenuItem("立即推送", self._on_push_now),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("退出", self._on_quit)
        )
    
    def _on_show_status(self, icon, item):
        if self.on_show_status:
            self.on_show_status()
    
    def _on_show_config(self, icon, item):
        if self.on_show_config:
            self.on_show_config()
    
    def _on_push_now(self, icon, item):
        pass  # 后续实现
    
    def _on_quit(self, icon, item):
        if self.on_quit:
            self.on_quit()
    
    def start(self):
        image = create_icon_image(self.current_status)
        self.icon = pystray.Icon(
            "PCWatcher",
            image,
            "PCWatcher",
            self.create_menu()
        )
        self.icon.run_detached()
    
    def stop(self):
        if self.icon:
            self.icon.stop()
    
    def update_status(self, status):
        self.current_status = status
        if self.icon:
            self.icon.icon = create_icon_image(status)
```

**Step 4: Commit**

```bash
git add tray.py
git commit -m "feat: add system tray module"
```

---

## Task 6: 配置窗口 GUI

**Files:**
- Create: `D:\repositories\PCWatcher\gui.py`

**Step 1: 实现 tkinter 配置窗口**

```python
import tkinter as tk
from tkinter import ttk, messagebox
from config_manager import ConfigManager

class ConfigWindow:
    def __init__(self, config_manager: ConfigManager, on_save=None):
        self.config_manager = config_manager
        self.on_save = on_save
        self.window = None
    
    def show(self):
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
        
        self.window = tk.Toplevel()
        self.window.title("PCWatcher 配置")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        
        self._create_widgets()
        self._load_config()
    
    def _create_widgets(self):
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # PushMe 配置
        ttk.Label(main_frame, text="PushMe Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.push_key_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.push_key_var, width=40).grid(row=0, column=1, pady=5)
        ttk.Button(main_frame, text="测试", command=self._test_pushme).grid(row=0, column=2, padx=5)
        
        # CPU 阈值
        ttk.Label(main_frame, text="CPU 使用率阈值 (%):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cpu_threshold_var = tk.IntVar(value=80)
        ttk.Entry(main_frame, textvariable=self.cpu_threshold_var, width=15).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 内存阈值
        ttk.Label(main_frame, text="内存使用率阈值 (%):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.memory_threshold_var = tk.IntVar(value=85)
        ttk.Entry(main_frame, textvariable=self.memory_threshold_var, width=15).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # 网络配置
        ttk.Label(main_frame, text="网卡选择:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.network_interface_var = tk.StringVar()
        self.network_combo = ttk.Combobox(main_frame, textvariable=self.network_interface_var, width=37)
        self.network_combo.grid(row=3, column=1, pady=5)
        
        ttk.Label(main_frame, text="上传速度阈值 (MB/s):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.upload_threshold_var = tk.IntVar(value=10)
        ttk.Entry(main_frame, textvariable=self.upload_threshold_var, width=15).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="下载速度阈值 (MB/s):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.download_threshold_var = tk.IntVar(value=10)
        ttk.Entry(main_frame, textvariable=self.download_threshold_var, width=15).grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # 按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=6, column=0, columnspan=3, pady=20)
        ttk.Button(btn_frame, text="保存", command=self._save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
    
    def _load_config(self):
        cfg = self.config_manager.config
        self.push_key_var.set(cfg.get("push_key", ""))
        self.cpu_threshold_var.set(cfg.get("cpu_threshold", 80))
        self.memory_threshold_var.set(cfg.get("memory_threshold", 85))
        self.network_interface_var.set(cfg.get("network_interface", ""))
        self.upload_threshold_var.set(cfg.get("network_upload_threshold", 10485760) // 1048576)
        self.download_threshold_var.set(cfg.get("network_download_threshold", 10485760) // 1048576)
    
    def _test_pushme(self):
        from notifier import PushMeClient
        key = self.push_key_var.get()
        if not key:
            messagebox.showwarning("警告", "请输入 PushMe Key")
            return
        
        client = PushMeClient(key)
        success, msg = client.test_connection()
        if success:
            messagebox.showinfo("成功", "连接测试成功！")
        else:
            messagebox.showerror("失败", f"连接失败: {msg}")
    
    def _save_config(self):
        cfg = self.config_manager.config
        cfg["push_key"] = self.push_key_var.get()
        cfg["cpu_threshold"] = self.cpu_threshold_var.get()
        cfg["memory_threshold"] = self.memory_threshold_var.get()
        cfg["network_interface"] = self.network_interface_var.get()
        cfg["network_upload_threshold"] = self.upload_threshold_var.get() * 1048576
        cfg["network_download_threshold"] = self.download_threshold_var.get() * 1048576
        cfg["first_run"] = False
        
        self.config_manager.save()
        
        if self.on_save:
            self.on_save()
        
        messagebox.showinfo("成功", "配置已保存")
        self.window.destroy()
    
    def set_network_interfaces(self, interfaces):
        self.network_combo['values'] = interfaces
        if interfaces:
            self.network_combo.current(0)
```

**Step 2: Commit**

```bash
git add gui.py
git commit -m "feat: add config window GUI"
```

---

## Task 7: 主程序整合

**Files:**
- Modify: `D:\repositories\PCWatcher\pcwatcher.py`

**Step 1: 实现主程序**

```python
import sys
import os
import threading
import time
import tkinter as tk

from config_manager import ConfigManager
from monitor import SystemMonitor
from notifier import PushMeClient
from tray import SystemTray, create_icon_image
from gui import ConfigWindow

class PCWatcher:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.monitor = SystemMonitor()
        self.tray = None
        self.running = False
        self.monitor_thread = None
        self.last_alerts = {}  # 去重
    
    def start(self):
        self.running = True
        
        # 启动托盘
        self.tray = SystemTray(
            on_show_status=self.show_status,
            on_show_config=self.show_config,
            on_quit=self.quit
        )
        self.tray.start()
        
        # 检查首次运行
        if self.config_manager.is_first_run():
            self.show_config()
        
        # 启动监控线程
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def _monitor_loop(self):
        interval = self.config_manager.config.get("interval", 30)
        
        while self.running:
            try:
                self._check_metrics()
            except Exception as e:
                print(f"Monitor error: {e}")
            
            time.sleep(interval)
    
    def _check_metrics(self):
        cfg = self.config_manager.config
        alerts = []
        status = "green"
        
        # CPU
        cpu = self.monitor.get_cpu_percent()
        if cpu > cfg.get("cpu_threshold", 80):
            alerts.append(f"CPU使用率: {cpu:.1f}% (阈值: {cfg['cpu_threshold']}%)")
            status = "red"
        
        # Memory
        mem = self.monitor.get_memory()
        if mem["percent"] > cfg.get("memory_threshold", 85):
            alerts.append(f"内存使用率: {mem['percent']:.1f}% (阈值: {cfg['memory_threshold']}%)")
            status = "red"
        
        # Network
        iface = cfg.get("network_interface")
        if iface:
            net = self.monitor.get_network_info(iface)
            if net:
                up_limit = cfg.get("network_upload_threshold", 10485760)
                down_limit = cfg.get("network_download_threshold", 10485760)
                
                if net["upload_speed"] > up_limit:
                    alerts.append(f"上传速度: {net['upload_speed']/1048576:.1f}MB/s")
                    status = "red"
                if net["download_speed"] > down_limit:
                    alerts.append(f"下载速度: {net['download_speed']/1048576:.1f}MB/s")
                    status = "red"
        
        # 更新托盘状态
        if self.tray:
            self.tray.update_status(status)
        
        # 发送通知
        if alerts:
            self._send_alerts(alerts)
    
    def _send_alerts(self, alerts):
        push_key = self.config_manager.config.get("push_key")
        if not push_key:
            return
        
        # 去重检查
        alert_key = "|".join(alerts)
        now = time.time()
        if alert_key in self.last_alerts:
            if now - self.last_alerts[alert_key] < 300:  # 5分钟
                return
        
        self.last_alerts[alert_key] = now
        
        client = PushMeClient(push_key)
        client.send_warning("PCWatcher 告警", alerts)
    
    def show_status(self):
        pass  # TODO: 实现状态弹窗
    
    def show_config(self):
        root = tk.Tk()
        root.withdraw()
        
        win = ConfigWindow(self.config_manager)
        interfaces = self.monitor.get_network_interfaces()
        win.set_network_interfaces(interfaces)
        win.show()
        
        root.mainloop()
    
    def quit(self):
        self.running = False
        if self.tray:
            self.tray.stop()

def main():
    app = PCWatcher()
    app.start()
    
    # 保持主线程
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
```

**Step 2: 运行测试**

Run: `cd D:\repositories\PCWatcher && python pcwatcher.py`
Expected: 托盘图标出现

**Step 3: Commit**

```bash
git add pcwatcher.py
git commit -m "feat: integrate main application"
```

---

## Task 8: 状态显示弹窗

**Files:**
- Modify: `D:\repositories\PCWatcher\tray.py`
- Modify: `D:\repositories\PCWatcher\pcwatcher.py`

**Step 1: 添加状态弹窗功能**

在 tray.py 添加 StatusWindow 类

**Step 2: 测试**

Run: `python pcwatcher.py` 并点击托盘菜单"当前状态"

**Step 3: Commit**

```bash
git add tray.py pcwatcher.py
git commit -m "feat: add status display popup"
```

---

## Task 9: 打包为 exe

**Files:**
- Create: `D:\repositories\PCWatcher\build.spec`

**Step 1: 创建打包配置**

```python
from pystray import _win32

a = Analysis(
    ['pcwatcher.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PCWatcher',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PCWatcher',
)
```

**Step 2: 打包**

Run: `pyinstaller build.spec`

**Step 3: Commit**

```bash
git add build.spec
git commit -m "chore: add pyinstaller config"
```

---

## 执行方式

**Plan complete and saved to `docs/plans/2026-03-03-pcwatcher-implementation.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**
