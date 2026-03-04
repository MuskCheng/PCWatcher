# 🖥️ PCWatcher

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows-green.svg)](https://github.com/MuskCheng/PCWatcher)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/MuskCheng/PCWatcher?style=social)](https://github.com/MuskCheng/PCWatcher/stargazers)

> Windows 系统监控工具，实时监控 CPU、内存、磁盘使用情况，支持通过 PushMe 发送桌面通知。

## ✨ 功能特性

| 功能 | 描述 |
|------|------|
| 🔍 实时监控 | 实时监控 CPU、内存、磁盘使用情况 |
| 🔔 桌面通知 | 超过阈值时通过 PushMe 发送桌面通知 |
| 🖥️ 系统托盘 | 系统托盘运行，支持后台监控 |
| ⚙️ GUI 配置 | 图形界面轻松配置监控阈值 |
| 🚀 开机自启 | 支持开机自动启动 |

## 📋 环境要求

- **Python**: 3.8+
- **操作系统**: Windows

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行程序

```bash
python pcwatcher.py
```

## ⚙️ 配置说明

编辑 `config.json` 或使用内置 GUI 设置监控阈值：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `cpu_threshold` | CPU 使用率阈值 (%) | 80 |
| `memory_threshold` | 内存使用率阈值 (%) | 85 |
| `disk_thresholds` | 磁盘使用率阈值 | {} |
| `interval` | 检查间隔（秒） | 30 |
| `push_key` | PushMe API 密钥 | - |

## 📦 构建可执行文件

```bash
pyinstaller build.spec
```

构建完成后，可执行文件位于 `dist/` 目录下。

## 📁 项目结构

```
PCWatcher/
├── pcwatcher.py       # 主程序入口
├── config_manager.py  # 配置管理
├── monitor.py         # 系统监控模块
├── notifier.py        # 通知模块
├── tray.py            # 系统托盘
├── gui.py             # GUI 界面
├── version.py         # 版本管理
├── config.json        # 配置文件
├── requirements.txt   # 依赖列表
├── build.spec         # PyInstaller 配置
└── LICENSE            # 许可证
```

## 📄 许可证

本项目基于 [MIT](LICENSE) 许可证开源。

---

⭐ 如果对你有帮助，欢迎 Star！
