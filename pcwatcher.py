import sys
import os
import threading
import time
import tkinter as tk
from tkinter import ttk

from config_manager import ConfigManager
from monitor import SystemMonitor
from notifier import PushMeClient
from tray import SystemTray
from gui import ConfigWindow


class PCWatcher:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.monitor = SystemMonitor()
        self.tray = None
        self.running = False
        self.monitor_thread = None
        self.last_alerts = {}
        self.root = None
        self.status_window = None
    
    def start(self):
        self.running = True
        
        self.root = tk.Tk()
        self.root.withdraw()
        
        self.tray = SystemTray(
            on_show_status=self.show_status,
            on_show_config=self.show_config,
            on_quit=self.quit,
            on_push_now=self.push_now
        )
        self.tray.start()
        
        if self.config_manager.is_first_run():
            self.show_config()
        
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        self.root.mainloop()
    
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
        
        cpu = self.monitor.get_cpu_percent()
        if cpu > cfg.get("cpu_threshold", 80):
            alerts.append(f"CPU使用率: {cpu:.1f}% (阈值: {cfg['cpu_threshold']}%)")
            status = "red"
        
        mem = self.monitor.get_memory()
        if mem["percent"] > cfg.get("memory_threshold", 85):
            alerts.append(f"内存使用率: {mem['percent']:.1f}% (阈值: {cfg['memory_threshold']}%)")
            status = "red"
        
        disks = self.monitor.get_disks()
        disk_thresholds = cfg.get("disk_thresholds", {})
        for disk in disks:
            mountpoint = disk["mountpoint"]
            threshold = disk_thresholds.get(mountpoint, 90)
            if disk["percent"] > threshold:
                alerts.append(f"磁盘 {mountpoint}: {disk['percent']:.1f}% (阈值: {threshold}%)")
                status = "red"
        
        iface = cfg.get("network_interface")
        if iface:
            net = self.monitor.get_network_info(iface)
            if net:
                up_limit = cfg.get("network_upload_threshold", 10485760)
                down_limit = cfg.get("network_download_threshold", 10485760)
                
                if net["upload_speed"] > up_limit:
                    alerts.append(f"上传速度: {net['upload_speed']/1048576:.1f}MB/s (阈值: {up_limit/1048576}MB/s)")
                    status = "red"
                if net["download_speed"] > down_limit:
                    alerts.append(f"下载速度: {net['download_speed']/1048576:.1f}MB/s (阈值: {down_limit/1048576}MB/s)")
                    status = "red"
        
        if self.tray:
            self.tray.update_status(status)
        
        if alerts:
            self._send_alerts(alerts)
    
    def _send_alerts(self, alerts):
        push_key = self.config_manager.config.get("push_key")
        if not push_key:
            return
        
        alert_key = "|".join(alerts)
        now = time.time()
        if alert_key in self.last_alerts:
            if now - self.last_alerts[alert_key] < 300:
                return
        
        self.last_alerts[alert_key] = now
        
        client = PushMeClient(push_key)
        client.send_alert(alerts)
    
    def push_now(self):
        cfg = self.config_manager.config
        push_key = cfg.get("push_key")
        if not push_key:
            return
        
        cpu = self.monitor.get_cpu_percent()
        mem = self.monitor.get_memory()
        disks = self.monitor.get_disks()
        iface = cfg.get("network_interface")
        net = self.monitor.get_network_info(iface) if iface else None
        
        client = PushMeClient(push_key)
        client.send_status(cpu, mem, disks, net)
    
    def show_status(self):
        if self.status_window and self.status_window.winfo_exists():
            self.status_window.lift()
            return
        
        self.status_window = tk.Toplevel()
        self.status_window.title("PCWatcher 当前状态")
        self.status_window.geometry("400x660")
        self.status_window.configure(bg='#f5f5f5')
        
        header_frame = tk.Frame(self.status_window, bg='#1E88E5', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text='PCWatcher 系统监控', font=('Microsoft YaHei', 14, 'bold'), bg='#1E88E5', fg='white')
        title_label.pack(side=tk.LEFT, padx=20, pady=12)
        
        refresh_label = tk.Label(header_frame, text='↻ 实时更新', font=('Microsoft YaHei', 9), bg='#1E88E5', fg='#BBDEFB')
        refresh_label.pack(side=tk.RIGHT, padx=20, pady=12)
        
        self.main_frame = tk.Frame(self.status_window, bg='#f5f5f5')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self._update_status_display()
        
        self.status_update_job = self.status_window.after(3000, self._auto_refresh_status)
        
        self.status_window.protocol("WM_DELETE_WINDOW", self._on_status_window_close)
        
        btn_frame = tk.Frame(self.status_window, bg='#f5f5f5')
        btn_frame.pack(fill=tk.X, padx=15, pady=10)
        tk.Button(btn_frame, text='关闭', command=self._on_status_window_close, bg='#757575', fg='white', relief=tk.FLAT, padx=20, pady=5).pack()
    
    def _on_status_window_close(self):
        if hasattr(self, 'status_update_job'):
            self.status_window.after_cancel(self.status_update_job)
        if self.status_window:
            self.status_window.destroy()
            self.status_window = None
    
    def _auto_refresh_status(self):
        if self.status_window and self.status_window.winfo_exists():
            self._update_status_display()
            self.status_update_job = self.status_window.after(3000, self._auto_refresh_status)
    
    def _update_status_display(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        cfg = self.config_manager.config
        
        try:
            cpu = self.monitor.get_cpu_percent()
        except:
            cpu = 0
        
        try:
            mem = self.monitor.get_memory()
        except:
            mem = {"used": 0, "total": 0, "percent": 0}
        
        try:
            disks = self.monitor.get_disks()
        except:
            disks = []
        
        iface = cfg.get("network_interface")
        net = None
        if iface:
            try:
                net = self.monitor.get_network_info(iface)
            except:
                net = None
        
        row = 0
        
        self._add_status_card(row, '💻', 'CPU 使用率', f'{cpu:.1f}%', '#FF9800' if cpu > 80 else '#4CAF50')
        row += 1
        
        self._add_status_card(row, '📊', '内存使用', f"{mem['used']:.1f} / {mem['total']:.1f} GB ({mem['percent']:.1f}%)", '#9C27B0' if mem['percent'] > 85 else '#4CAF50')
        row += 1
        
        for disk in disks:
            color = '#F44336' if disk['percent'] > 90 else '#FF9800' if disk['percent'] > 80 else '#4CAF50'
            self._add_status_card(row, '💾', f'磁盘 {disk["mountpoint"]}', f"{disk['used']:.1f} / {disk['total']:.1f} GB ({disk['percent']:.1f}%)", color)
            row += 1
        
        if net:
            upload_speed = net.get('upload_speed', 0) / 1024
            download_speed = net.get('download_speed', 0) / 1024
            self._add_status_card(row, '⬆️', '上传速度', f'{upload_speed:.1f} KB/s', '#2196F3')
            row += 1
            self._add_status_card(row, '⬇️', '下载速度', f'{download_speed:.1f} KB/s', '#2196F3')
            row += 1
            if net.get("ip"):
                self._add_status_card(row, '🌐', 'IP 地址', net['ip'], '#607D8B')
                row += 1
    
    def _add_status_card(self, row, icon, title, value, color):
        card = tk.Frame(self.main_frame, bg='white', relief=tk.RIDGE, borderwidth=1)
        card.grid(row=row, column=0, sticky='ew', pady=4)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        icon_label = tk.Label(card, text=icon, font=('Arial', 16), bg='white', width=3)
        icon_label.pack(side=tk.LEFT, padx=10, pady=8)
        
        text_frame = tk.Frame(card, bg='white')
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=8)
        
        tk.Label(text_frame, text=title, font=('Microsoft YaHei', 9), bg='white', fg='#757575').pack(anchor=tk.W)
        tk.Label(text_frame, text=value, font=('Microsoft YaHei', 11, 'bold'), bg='white', fg=color).pack(anchor=tk.W)
    
    def show_config(self):
        win = ConfigWindow(self.config_manager, on_save=self._on_config_save)
        interfaces = self.monitor.get_network_interfaces()
        win.set_network_interfaces(interfaces)
        win.show()
    
    def _on_config_save(self):
        pass
    
    def quit(self):
        self.running = False
        if self.tray:
            self.tray.stop()
        if self.root:
            self.root.quit()


def main():
    app = PCWatcher()
    app.start()


if __name__ == "__main__":
    main()
