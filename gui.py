import tkinter as tk
from tkinter import ttk, messagebox
from version import __version__

class ConfigWindow:
    def __init__(self, config_manager, on_save=None):
        self.config_manager = config_manager
        self.on_save = on_save
        self.window = None
        self.network_combo = None
        self._pending_interfaces = None
    
    def show(self):
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
        
        self.window = tk.Toplevel()
        self.window.title(f"PCWatcher 配置 v{__version__}")
        self.window.geometry("500x550")
        self.window.resizable(False, False)
        
        self._create_widgets()
        self._load_config()
        
        if self._pending_interfaces:
            self.set_network_interfaces(self._pending_interfaces)
    
    def _create_widgets(self):
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        row = 0
        
        ttk.Label(main_frame, text="PushMe Key:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.push_key_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.push_key_var, width=40).grid(row=row, column=1, pady=5)
        ttk.Button(main_frame, text="测试", command=self._test_pushme).grid(row=row, column=2, padx=5)
        
        row += 1
        ttk.Label(main_frame, text="CPU 使用率阈值 (%):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.cpu_threshold_var = tk.IntVar(value=80)
        ttk.Entry(main_frame, textvariable=self.cpu_threshold_var, width=15).grid(row=row, column=1, sticky=tk.W, pady=5)
        
        row += 1
        ttk.Label(main_frame, text="内存使用率阈值 (%):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.memory_threshold_var = tk.IntVar(value=85)
        ttk.Entry(main_frame, textvariable=self.memory_threshold_var, width=15).grid(row=row, column=1, sticky=tk.W, pady=5)
        
        row += 1
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky='ew', pady=10)
        
        row += 1
        ttk.Label(main_frame, text="网卡选择:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.network_interface_var = tk.StringVar()
        self.network_combo = ttk.Combobox(main_frame, textvariable=self.network_interface_var, width=37)
        self.network_combo.grid(row=row, column=1, pady=5)
        
        row += 1
        ttk.Label(main_frame, text="上传速度阈值 (MB/s):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.upload_threshold_var = tk.IntVar(value=10)
        ttk.Entry(main_frame, textvariable=self.upload_threshold_var, width=15).grid(row=row, column=1, sticky=tk.W, pady=5)
        
        row += 1
        ttk.Label(main_frame, text="下载速度阈值 (MB/s):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.download_threshold_var = tk.IntVar(value=10)
        ttk.Entry(main_frame, textvariable=self.download_threshold_var, width=15).grid(row=row, column=1, sticky=tk.W, pady=5)
        
        row += 1
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky='ew', pady=10)
        
        row += 1
        ttk.Label(main_frame, text="监控间隔 (秒):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.interval_var = tk.IntVar(value=30)
        ttk.Entry(main_frame, textvariable=self.interval_var, width=15).grid(row=row, column=1, sticky=tk.W, pady=5)
        
        row += 1
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row, column=0, columnspan=3, pady=20)
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
        self.interval_var.set(cfg.get("interval", 30))
    
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
        cfg["interval"] = self.interval_var.get()
        cfg["first_run"] = False
        
        self.config_manager.save()
        
        if self.on_save:
            self.on_save()
        
        messagebox.showinfo("成功", "配置已保存")
        self.window.destroy()
    
    def set_network_interfaces(self, interfaces):
        self._pending_interfaces = interfaces
        if self.network_combo:
            self.network_combo['values'] = interfaces
            if interfaces:
                self.network_combo.current(0)
