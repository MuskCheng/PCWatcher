# PCWatcher

Windows系统监控工具，实时监控CPU、内存、磁盘使用情况，支持通过PushMe发送桌面通知。

## 功能特性

- 实时监控CPU、内存、磁盘使用情况
- 超过阈值时通过PushMe发送桌面通知
- 系统托盘运行，支持后台监控
- GUI界面配置监控阈值
- 支持开机自启动

## 环境要求

- Python 3.8+
- Windows操作系统

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
python pcwatcher.py
```

## 配置说明

编辑 `config.json` 或使用内置GUI设置监控阈值：
- CPU使用率阈值 (%)
- 内存使用率阈值 (%)
- 磁盘使用率阈值 (%)
- 检查间隔（秒）
- PushMe API密钥

## 构建可执行文件

```bash
pyinstaller build.spec
```

## 许可证

MIT License
