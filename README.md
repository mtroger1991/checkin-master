# Checkin Master 🔥

> 多平台自动签到工具 - 京东、美团、支付宝、拼多多一键签到

[![GitHub stars](https://img.shields.io/github/stars/mtroger1991/checkin-master?style=social)](https://github.com/mtroger1991/checkin-master)
[![GitHub forks](https://img.shields.io/github/forks/mtroger1991/checkin-master?style=social)](https://github.com/mtroger1991/checkin-master)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)

---

## ✨ 功能特性

- 🛒 **京东签到** - 自动签到领京豆
- 🍔 **美团签到** - 自动签到领红包
- 💰 **支付宝签到** - 蚂蚁森林/庄园自动签到
- 🛍️ **拼多多签到** - 果园签到领水滴
- 📱 **多渠道通知** - Server酱/Bark/PushPlus/邮件
- ⏰ **定时执行** - 支持GitHub Actions自动运行
- 🔧 **灵活配置** - 按需启用平台

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/mtroger1991/checkin-master.git
cd checkin-master
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置账号

```bash
# 复制配置模板
cp config/config.json.example config/config.json

# 编辑配置文件，填入你的Cookie/Token
# 详见下方「获取Cookie」部分
```

### 4. 运行签到

```bash
# 批量签到所有平台
python main.py

# 单个平台签到
python main.py -p jd
python main.py -p meituan
python main.py -p alipay
python main.py -p pdd
```

---

## 🍪 获取Cookie教程

### 京东Cookie

1. 打开浏览器，访问 https://plogin.m.jd.com/login/login
2. 登录京东账号
3. 按F12打开开发者工具 → Application → Cookies
4. 找到 `pt_key` 和 `pt_pin` 的值

### 美团Token

1. 打开手机美团App
2. 使用抓包工具（如Charles/Fiddler）
3. 找到请求头中的 `token` 和 `userId`

### 支付宝Cookie

1. 打开浏览器，访问 https://www.alipay.com
2. 登录支付宝账号
3. 按F12打开开发者工具 → Application → Cookies
4. 复制所有Cookie

### 拼多多Cookie

1. 打开浏览器，访问 https://mobile.yangkeduo.com
2. 登录拼多多账号
3. 按F12打开开发者工具 → Application → Cookies
4. 找到 `PDDAccessToken` 的值

---

## ⏰ GitHub Actions 定时执行

### 1. 设置Secrets

在仓库的 Settings → Secrets and variables → Actions 中添加：

| Secret名称 | 说明 |
|------------|------|
| `CHECKIN_CONFIG` | 完整的config.json内容 |

### 2. 启用Workflow

项目已内置 `.github/workflows/checkin.yml`，默认每天早上7:00自动执行签到。

可以修改 `checkin.yml` 中的 cron 表达式调整执行时间：

```yaml
schedule:
  - cron: '0 23 * * *'  # UTC 23:00 = 北京时间 7:00
```

---

## 📁 项目结构

```
checkin-master/
├── .github/
│   └── workflows/
│       └── checkin.yml          # GitHub Actions定时任务
├── config/
│   ├── config.json.example      # 配置模板
│   └── cookies/                 # Cookie存储目录
├── platforms/
│   ├── __init__.py
│   ├── jd.py                    # 京东签到
│   ├── meituan.py               # 美团签到
│   ├── alipay.py                # 支付宝签到
│   └── pdd.py                   # 拼多多签到
├── utils/
│   ├── __init__.py
│   ├── logger.py                # 日志工具
│   └── notifier.py              # 通知工具
├── main.py                      # 主入口
├── requirements.txt             # 依赖
└── README.md                    # 使用说明
```

---

## 📱 通知配置

### Server酱（推荐）

1. 访问 https://sct.ftqq.com/ 注册账号
2. 获取 SendKey
3. 填入配置文件的 `serverchan_key`

### PushPlus

1. 访问 https://www.pushplus.plus/ 关注公众号
2. 获取 Token
3. 填入配置文件的 `pushplus_token`

### Bark（iOS用户）

1. App Store 下载 Bark
2. 获取推送 Key
3. 填入配置文件的 `bark_key`

---

## ⚠️ 免责声明

- 本项目仅供学习交流使用
- 请勿用于商业用途
- 使用本工具产生的任何问题由使用者自行承担
- 建议合理使用，避免频繁请求导致账号异常

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/new-platform`)
3. 提交更改 (`git commit -m 'Add new platform'`)
4. 推送到分支 (`git push origin feature/new-platform`)
5. 创建 Pull Request

---

## 📄 License

[MIT License](LICENSE)

---

## 💰 支持作者

如果觉得有用，请给个 ⭐ Star！

也欢迎通过 [GitHub Sponsors](https://github.com/sponsors/mtroger1991) 赞助支持 ❤️