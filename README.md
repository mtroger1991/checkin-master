# Checkin Master - 多平台自动签到工具

一个支持京东、美团、支付宝、拼多多等多个平台的自动签到工具。

## 支持平台

- 京东
- 美团
- 支付宝
- 拼多多

## 功能特性

- 多平台统一签到管理
- 定时任务自动执行
- 签到结果通知
- 配置灵活，易于扩展

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置

1. 复制 `config.example.json` 为 `config.json`
2. 填写各平台的登录凭证

### 运行

```bash
python main.py
```

## 项目结构

```
checkin-master/
├── config/          # 配置文件
├── core/            # 核心签到逻辑
├── platforms/       # 各平台实现
├── utils/           # 工具函数
├── logs/            # 日志文件
├── main.py          # 主入口
└── requirements.txt # 依赖列表
```

## 免责声明

本工具仅供学习交流使用，请遵守各平台的使用条款。使用本工具产生的任何后果由使用者自行承担。

## License

MIT License
