<div align="center">

# 🖥️ PCWatcher

**轻量级 Windows 系统监控工具**

实时监控 CPU、内存、磁盘、网络，通过 PushMe 推送告警通知

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=flat-square&logo=windows&logoColor=white)](https://github.com/MuskCheng/PCWatcher)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/MuskCheng/PCWatcher?style=flat-square)](https://github.com/MuskCheng/PCWatcher/releases)

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [使用指南](#-使用指南) • [截图预览](#-截图预览)

</div>

---

## ✨ 功能特性

| 功能 | 描述 |
|:----:|------|
| 🖥️ **实时监控** | CPU、内存、磁盘、网络使用率实时监控 |
| 🔔 **告警推送** | 超过阈值时通过 PushMe 推送消息到手机 |
| 📊 **状态查看** | 图形化界面实时显示系统状态 |
| 🏷️ **设备备注** | 支持设置设备备注名，多设备管理更清晰 |
| 🎨 **消息分组** | PushMe 消息自动分组，支持颜色标签分类 |
| ⚙️ **灵活配置** | 图形界面配置各项监控阈值 |
| 🚀 **开机自启** | 支持开机自动启动，后台静默运行 |
| 📦 **单文件运行** | 打包为单个 exe，无需安装 Python 环境 |

## 🚀 快速开始

### 方式一：下载可执行文件（推荐）

前往 [Releases](https://github.com/MuskCheng/PCWatcher/releases) 页面下载最新版本的 `PCWatcher.exe`，双击运行即可。

### 方式二：源码运行

```bash
# 克隆仓库
git clone https://github.com/MuskCheng/PCWatcher.git
cd PCWatcher

# 安装依赖
pip install -r requirements.txt

# 运行程序
python pcwatcher.py
```

## 📖 使用指南

### 1. 首次运行

首次运行时会自动弹出配置窗口：

1. **设备备注名**：设置设备名称（如"公司电脑"、"家用主机"），便于多设备管理
2. **PushMe Key**：在 [PushMe App](https://push.i-i.me/) 中获取推送密钥
3. **监控阈值**：设置 CPU、内存、磁盘的使用率阈值
4. **网卡选择**：选择要监控的网络接口
5. **监控间隔**：设置检查间隔时间（秒）

### 2. 系统托盘

程序启动后会在系统托盘显示图标：

- 🟢 **绿色图标**：系统状态正常
- 🔴 **红色图标**：存在告警项

**右键菜单功能：**

| 菜单项 | 功能 |
|--------|------|
| 查看状态 | 打开实时状态窗口 |
| 推送状态 | 立即推送当前系统状态到手机 |
| 配置设置 | 打开配置窗口 |
| 退出 | 退出程序 |

### 3. 消息推送效果

PushMe 消息会按类型自动分组并添加颜色标签：

| 消息类型 | 颜色标签 | 分组头像 |
|----------|----------|----------|
| 系统状态 | ⬜️ 白色 | 📊 |
| 告警通知 | 🟨 黄色 | ⚠️ |
| 连接测试 | 🟩 绿色 | ✅ |

### 4. 配置项说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `device_name` | 设备备注名 | 空 |
| `push_key` | PushMe 推送密钥 | 空 |
| `cpu_threshold` | CPU 使用率阈值 (%) | 80 |
| `memory_threshold` | 内存使用率阈值 (%) | 85 |
| `disk_thresholds` | 各磁盘阈值 (%) | 90 |
| `network_interface` | 监控网卡 | 空 |
| `network_upload_threshold` | 上传速度阈值 (MB/s) | 10 |
| `network_download_threshold` | 下载速度阈值 (MB/s) | 10 |
| `interval` | 监控间隔 (秒) | 30 |

## 📸 截图预览

<details>
<summary>点击展开</summary>

> 状态窗口和配置窗口截图（待补充）

</details>

## 🔧 自定义构建

```bash
# 安装构建工具
pip install pyinstaller

# 构建
pyinstaller build.spec

# 输出文件位于 dist/PCWatcher.exe
```

## 📁 项目结构

```
PCWatcher/
├── pcwatcher.py       # 主程序入口
├── config_manager.py  # 配置管理模块
├── monitor.py         # 系统监控模块
├── notifier.py        # PushMe 推送模块
├── gui.py             # GUI 界面
├── tray.py            # 系统托盘模块
├── version.py         # 版本管理
├── VERSION            # 版本号文件
├── build.spec         # PyInstaller 配置
├── requirements.txt   # Python 依赖
└── README.md          # 说明文档
```

## 🤝 参与贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目基于 [MIT](LICENSE) 许可证开源。

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐ Star 支持一下！**

</div>