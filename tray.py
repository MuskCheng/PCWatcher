import pystray
from PIL import Image, ImageDraw
import threading

def create_icon_image(color="green"):
    colors = {
        "green": (30, 136, 229),
        "yellow": (255, 152, 0),
        "red": (244, 67, 54)
    }
    rgb = colors.get(color, colors["green"])
    
    image = Image.new('RGB', (64, 64), color='white')
    draw = ImageDraw.Draw(image)
    
    draw.ellipse([4, 4, 60, 60], fill=rgb, outline=rgb, width=2)
    
    draw.rectangle([18, 20, 28, 44], fill='white')
    draw.rectangle([30, 20, 40, 44], fill='white')
    draw.rectangle([42, 20, 46, 44], fill='white')
    
    draw.rectangle([18, 32, 46, 36], fill='white')
    
    return image

class SystemTray:
    def __init__(self, on_show_status, on_show_config, on_quit, on_push_now=None):
        self.on_show_status = on_show_status
        self.on_show_config = on_show_config
        self.on_quit = on_quit
        self.on_push_now = on_push_now
        self.icon = None
        self.current_status = "green"
    
    def create_menu(self):
        items = [
            pystray.MenuItem("当前状态", self._on_show_status),
            pystray.MenuItem("配置设置", self._on_show_config),
        ]
        if self.on_push_now:
            items.append(pystray.MenuItem("立即推送", self._on_push_now))
        items.extend([
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("退出", self._on_quit)
        ])
        return pystray.Menu(*items)
    
    def _on_show_status(self, icon, item):
        if self.on_show_status:
            self.on_show_status()
    
    def _on_show_config(self, icon, item):
        if self.on_show_config:
            self.on_show_config()
    
    def _on_push_now(self, icon, item):
        if self.on_push_now:
            self.on_push_now()
    
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
