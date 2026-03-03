# PCWatcher 技术档案

> 项目名称：PCWatcher (电脑守护者)  
> 创建日期：2026-03-03  
> 最后更新：2026-03-03

---

## 一、项目概述

PCWatcher 是一款运行在 Windows 系统托盘中的后台监控工具，用于实时监控系统状态并通过 PushMe 推送告警通知。

### 核心功能
- 系统托盘后台运行，启动时最小化
- 实时监控 CPU、内存、磁盘、网络
- 超过阈值时自动推送 PushMe 告警
- 首次启动引导配置

---

## 二、项目结构

```
PCWatcher/
├── pcwatcher.py          # 主程序入口
├── config_manager.py     # 配置管理
├── monitor.py           # 系统监控模块
├── notifier.py          # PushMe 通知模块
├── tray.py              # 系统托盘模块
├── gui.py               # 配置窗口 GUI
├── build.spec           # PyInstaller 打包配置
├── requirements.txt     # 依赖清单
├── config.json          # 默认配置文件
├── tests/               # 单元测试
│   ├── test_config_manager.py
│   ├── test_monitor.py
│   ├── test_notifier.py
│   └── test_tray.py
└── docs/plans/          # 设计文档
    ├── 2026-03-03-pcwatcher-design.md
    └── 2026-03-03-pcwatcher-implementation.md
```

---

## 三、模块说明

### 3.1 pcwatcher.py - 主程序入口

**职责：** 协调各模块，负责主循环和事件处理

**核心类：**
- `PCWatcher`: 主应用程序类

**主要方法：**
| 方法 | 功能 |
|------|------|
| `start()` | 初始化托盘、启动监控线程 |
| `_monitor_loop()` | 后台监控循环 |
| `_check_metrics()` | 检查各项指标是否超阈值 |
| `_send_alerts()` | 发送告警通知（带去重） |
| `show_status()` | 显示当前状态窗口 |
| `show_config()` | 显示配置窗口 |
| `push_now()` | 立即推送当前状态 |
| `quit()` | 退出程序 |

**托盘菜单：**
- 当前状态：显示实时监控数据（3秒自动刷新）
- 配置设置：打开配置窗口
- 立即推送：手动推送状态到 PushMe
- 退出：关闭程序

---

### 3.2 config_manager.py - 配置管理

**职责：** 配置文件的加载、保存和默认值管理

**配置项：**

| 配置键 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `push_key` | string | "" | PushMe 推送密钥 |
| `cpu_threshold` | int | 80 | CPU 使用率告警阈值 (%) |
| `memory_threshold` | int | 85 | 内存使用率告警阈值 (%) |
| `disk_thresholds` | dict | {} | 各分区告警阈值，格式: `{"C:\\": 90}` |
| `network_interface` | string | "" | 监控的网卡名称 |
| `network_upload_threshold` | int | 10485760 | 上传速度告警阈值 (B/s)，默认 10MB/s |
| `network_download_threshold` | int | 10485760 | 下载速度告警阈值 (B/s)，默认 10MB/s |
| `interval` | int | 30 | 监控间隔 (秒) |
| `first_run` | bool | true | 是否首次运行 |

**配置文件位置：** `%APPDATA%/PCWatcher/config.json`

---

### 3.3 monitor.py - 系统监控

**职责：** 采集系统各项指标数据

**主要方法：**

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `get_cpu_percent()` | float | CPU 使用率 (%) |
| `get_memory()` | dict | 内存信息，包含 `used`(GB), `total`(GB), `percent`(%) |
| `get_disks()` | list[dict] | 磁盘分区列表，每项包含 `mountpoint`, `used`, `total`, `percent` |
| `get_network_info(interface_name)` | dict | 网络信息，包含 `interface`, `ip`, `upload_speed`, `download_speed` |
| `get_network_interfaces()` | list | 所有网卡名称列表 |

**注意：**
- 首次调用 `get_network_info()` 返回的速度为 0（需要两次调用计算差值）
- 网络速度单位为 B/s

---

### 3.4 notifier.py - PushMe 通知

**职责：** 通过 PushMe API 发送通知

**主要方法：**

| 方法 | 参数 | 功能 |
|------|------|------|
| `send()` | title, content, msg_type | 发送原始消息 |
| `send_status()` | cpu, mem, disks, net | 发送格式化状态消息 |
| `send_alert()` | alerts | 发送告警消息 |
| `test_connection()` | - | 测试连接 |

**消息格式：**
- 使用 Markdown 表格格式
- 支持消息分组：`[#PCWatcher!图标]`
- 告警使用 `[w]` 前缀

---

### 3.5 tray.py - 系统托盘

**职责：** 管理系统托盘图标和右键菜单

**主要方法：**

| 方法 | 功能 |
|------|------|
| `start()` | 启动托盘图标 |
| `stop()` | 停止托盘图标 |
| `update_status(status)` | 更新图标状态 |

**状态颜色：**
| 状态 | 颜色 | 含义 |
|------|------|------|
| `green` | 蓝色 (#1E88E5) | 正常 |
| `yellow` | 橙色 (#FF9800) | 警告 |
| `red` | 红色 (#F44336) | 异常 |

---

### 3.6 gui.py - 配置窗口

**职责：** 提供配置界面

**配置项：**
1. PushMe Key + 测试连接按钮
2. CPU 使用率阈值
3. 内存使用率阈值
4. 网卡选择（下拉框）
5. 上传/下载速度阈值
6. 监控间隔

**窗口大小：** 500x550

---

## 四、技术栈

| 组件 | 技术选型 | 版本要求 |
|------|----------|----------|
| 开发语言 | Python | 3.x |
| GUI | tkinter | 内置 |
| 系统托盘 | pystray | >=0.19.3 |
| 系统监控 | psutil | >=5.9.0 |
| 图片处理 | Pillow | >=9.0.0 |
| HTTP 请求 | requests | >=2.28.0 |
| 打包工具 | PyInstaller | >=6.0 |

---

## 五、数据流

```
用户启动
    │
    ▼
pcwatcher.py: start()
    │
    ├──▶ tray.py: 启动托盘图标
    │
    ├──▶ config_manager.py: 检查是否首次运行
    │        └──▶ gui.py: 显示配置窗口
    │
    └──▶ 后台监控线程 (每30秒)
             │
             ├──▶ monitor.py: 采集数据
             │
             ├──▶ 比对阈值
             │
             └──▶ notifier.py: 推送告警
```

---

## 六、PushMe API 集成

**接口地址：** `https://push.i-i.me`

**请求方式：** POST

**参数：**
| 参数 | 说明 |
|------|------|
| push_key | 推送密钥（必填） |
| title | 消息标题（必填） |
| content | 消息内容（必填） |
| type | 消息类型，默认 markdown |

**消息分组格式：** `[#分组名!图标]`

---

## 七、打包与部署

### 开发模式
```bash
python pcwatcher.py
```

### 打包为 EXE
```bash
pyinstaller build.spec --clean
```

输出目录：`dist/PCWatcher.exe`

---

## 八、注意事项

1. **首次运行**：程序会弹出配置窗口引导用户设置
2. **托盘图标**：程序运行后图标显示在系统托盘区
3. **网络速度**：首次获取为 0，需要等待一个监控周期后才能获取准确值
4. **告警去重**：同一告警内容 5 分钟内不重复推送

---

## 九、后续开发指南

### 添加新监控项

1. 在 `monitor.py` 添加采集方法
2. 在 `pcwatcher.py` 的 `_check_metrics()` 添加阈值比对
3. 在 `show_status()` 和 `notifier.py` 添加展示逻辑

### 修改托盘菜单

编辑 `tray.py` 的 `create_menu()` 方法

### 修改告警去重时间

编辑 `pcwatcher.py` 中的时间判断：
```python
if now - self.last_alerts[alert_key] < 300:  # 5分钟
```

---

## 十、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2026-03-03 | 初始版本 |

---

*档案创建人：PCWatcher Team*
