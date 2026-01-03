# 🏦 银行智能体应用

一个基于 AI 的银行智能助手应用，使用 DeepSeek API 实现多轮对话和智能银行业务处理。

## ✨ 功能特性

### 🤖 智能对话
- **多轮对话支持**：智能体能够记住对话历史，理解上下文和指代关系
- **自然语言交互**：支持自然语言查询，无需记忆特定命令格式
- **智能意图识别**：自动识别用户意图并调用相应的银行功能

### 💼 银行业务功能
- **查询余额**：快速查询账户余额和基本信息
- **账户信息**：查看完整的账户详细信息
- **转账功能**：支持账户间转账，包含完整的验证机制
- **交易记录**：查询历史交易记录
- **账户列表**：查看系统中所有账户信息
- **理财咨询**：提供理财建议和金融知识咨询

### 🎨 用户界面
- **现代化设计**：使用 Tailwind CSS 构建，美观的渐变背景和圆角设计
- **响应式布局**：完美适配桌面端、平板和移动端
- **快捷问题**：提供常用问题快捷按钮，一键开始对话
- **实时反馈**：加载动画和错误提示
- **消息时间戳**：每条消息显示发送时间
- **Tailwind CSS**：使用实用优先的 CSS 框架，快速构建现代化界面

## 🛠️ 技术栈

- **后端框架**：Flask (Python)
- **AI 模型**：DeepSeek Chat API
- **数据库**：MySQL (通过 SQLAlchemy ORM)
- **前端技术**：HTML5, Tailwind CSS, JavaScript (原生)
- **UI 框架**：Tailwind CSS (CDN)
- **部署**：支持 Zeabur、Heroku 等平台

## 📋 项目结构

```
.
├── app.py                 # Flask 应用主文件
├── init_db.py             # 数据库初始化脚本
├── main.py                # 测试脚本
├── requirements.txt        # Python 依赖
├── Procfile               # 部署配置
├── README.md              # 项目说明
├── backend/               # 后端代码
│   ├── __init__.py
│   ├── config.py          # 配置文件
│   ├── database.py        # 数据库连接和初始化
│   ├── api/               # API 路由层
│   │   ├── chat_api.py    # 聊天 API
│   │   └── health_api.py  # 健康检查 API
│   ├── service/           # 业务逻辑层
│   │   ├── account_service.py      # 账户服务
│   │   ├── banking_service.py      # 银行业务服务
│   │   ├── conversation_service.py # 对话服务
│   │   └── ai_service.py          # AI 服务
│   └── model/             # 数据模型层
│       ├── account.py      # 账户模型
│       ├── transaction.py # 交易记录模型
│       ├── conversation.py # 对话历史模型
│       └── base.py         # 模型基类
└── frontend/              # 前端代码
    └── index.html         # 前端页面（Tailwind CSS）
```

## 🚀 快速开始

### 环境要求

- Python 3.7+
- DeepSeek API Key

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd codes
```

2. **安装依赖**
```bash
# 使用 pip 安装
pip install -r requirements.txt

# 或使用 python -m pip（推荐）
python -m pip install -r requirements.txt
```

3. **配置环境变量**
```bash
# 设置 DeepSeek API Key
export DEEPSEEK_API_KEY="your-api-key-here"

# 设置 Flask Secret Key（可选，用于生产环境）
export FLASK_SECRET_KEY="your-secret-key-here"

# MySQL 数据库配置（如果使用 MySQL）
export MYSQL_HOST="your-mysql-host"
export MYSQL_PORT="3306"
export MYSQL_USER="your-mysql-user"
export MYSQL_PASSWORD="your-mysql-password"
export MYSQL_DATABASE="your-database-name"
```

4. **初始化数据库**（首次运行）
```bash
python init_db.py
```

5. **运行应用**
```bash
python app.py
```

应用将在 `http://localhost:8080` 启动（或使用环境变量 `PORT` 指定的端口）。

### 本地开发

```bash
# 开发模式（带调试）
export FLASK_ENV=development
python app.py
```

## 🌐 部署

### Zeabur 部署

1. 将代码推送到 Git 仓库
2. 在 Zeabur 中创建新项目
3. 连接 Git 仓库
4. 设置环境变量：
   - `DEEPSEEK_API_KEY`: 你的 DeepSeek API Key
   - `FLASK_SECRET_KEY`: Flask Session 密钥（可选）
   - `MYSQL_HOST`: MySQL 主机地址
   - `MYSQL_PORT`: MySQL 端口
   - `MYSQL_USER`: MySQL 用户名
   - `MYSQL_PASSWORD`: MySQL 密码
   - `MYSQL_DATABASE`: MySQL 数据库名
5. 部署完成后，数据库表会自动创建

### Heroku 部署

```bash
# 登录 Heroku
heroku login

# 创建应用
heroku create your-app-name

# 设置环境变量
heroku config:set DEEPSEEK_API_KEY=your-api-key-here
heroku config:set FLASK_SECRET_KEY=your-secret-key-here

# 部署
git push heroku main
```

## 📖 使用说明

### 基本使用

1. 打开应用后，在输入框中输入问题或点击快捷问题按钮
2. 智能体会自动识别你的意图并执行相应操作
3. 支持多轮对话，可以基于之前的对话继续提问

### 示例对话

**查询余额**
```
用户：查询张三的余额
AI：✅ 账户信息查询成功
    账户名称：张三
    账户号码：6222010012345678
    账户类型：储蓄账户
    当前余额：¥10,000.00元
```

**转账**
```
用户：从张三转账200元给李四
AI：✅ 转账成功！
    交易编号：TXN1001
    转出账户：张三 (6222010012345678)
    转入账户：李四 (6222020012345679)
    转账金额：¥200.00元
    转出账户余额：¥9,800.00元
```

**多轮对话**
```
用户：查询张三的余额
AI：✅ 账户信息查询成功...（显示余额）

用户：再转100元给李四
AI：✅ 转账成功！...（AI 知道是指从张三转出）

用户：现在还有多少钱？
AI：✅ 账户信息查询成功...（AI 知道是指张三的余额）
```

### 快捷问题

点击输入框上方的快捷问题按钮，可以快速开始以下操作：
- 💰 查询余额
- 📋 账户信息
- 💸 转账
- 📝 交易记录
- 👥 账户列表
- 💡 理财建议

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 必需 | 默认值 |
|--------|------|------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | 是 | - |
| `FLASK_SECRET_KEY` | Flask Session 密钥 | 否 | 默认值（生产环境建议设置） |
| `PORT` | 服务端口 | 否 | 8080 |
| `MYSQL_HOST` | MySQL 主机地址 | 是 | - |
| `MYSQL_PORT` | MySQL 端口 | 否 | 3306 |
| `MYSQL_USER` | MySQL 用户名 | 是 | - |
| `MYSQL_PASSWORD` | MySQL 密码 | 是 | - |
| `MYSQL_DATABASE` | MySQL 数据库名 | 是 | - |

### 数据库

应用使用 MySQL 数据库存储数据，包括：
- **账户信息**：账户名称、账户号码、余额等
- **交易记录**：所有转账和交易历史
- **对话历史**：用户与 AI 的对话记录

首次运行时会自动创建数据表并初始化默认账户数据：
- **张三**：余额 10,000 元（储蓄账户）
- **李四**：余额 500 元（储蓄账户）
- **王五**：余额 50,000 元（理财账户）

## 🎯 核心功能实现

### 架构设计

项目采用分层架构设计：

- **API 层** (`backend/api/`): 处理 HTTP 请求和响应
- **Service 层** (`backend/service/`): 业务逻辑处理
- **Model 层** (`backend/model/`): 数据模型定义
- **Frontend 层** (`frontend/`): 用户界面（Tailwind CSS）

### 多轮对话机制

应用使用 MySQL 数据库存储对话历史，每次请求时将完整的对话历史发送给 DeepSeek API，实现上下文记忆。

```python
# 获取对话历史（从数据库）
messages = conversation_service.get_messages(session_id)

# 构建完整消息列表
api_messages = [
    {"role": "system", "content": system_prompt},
    ...历史消息...,
    {"role": "user", "content": user_input}
]

# 调用 API
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=api_messages
)
```

### 函数调用机制

智能体通过解析 AI 返回的特殊格式指令来调用银行功能函数：

```
CALL:get_balance(name="张三")
CALL:transfer_money(from_name="张三", to_name="李四", amount=200)
```

### 前端技术

- **Tailwind CSS**: 使用 CDN 方式引入，通过实用类快速构建界面
- **响应式设计**: 使用 Tailwind 的响应式断点类实现移动端适配
- **原生 JavaScript**: 无需构建工具，直接使用现代 JavaScript 特性

## 🐛 故障排除

### 常见问题

1. **API 调用失败**
   - 检查 `DEEPSEEK_API_KEY` 是否正确设置
   - 确认网络连接正常
   - 查看控制台错误日志

2. **数据库连接失败**
   - 检查 MySQL 环境变量是否正确配置
   - 确认数据库服务是否运行
   - 验证网络连接和防火墙设置

3. **模块导入错误**
   - 确保已安装所有依赖：`python -m pip install -r requirements.txt`
   - 检查 Python 版本是否符合要求（Python 3.7+）

4. **端口冲突**
   - 修改环境变量 `PORT` 或代码中的默认端口

## 📝 开发计划

- [ ] 支持持久化存储优化（Redis 缓存）
- [ ] 添加用户认证系统
- [ ] 支持更多银行业务功能
- [ ] 添加消息导出功能
- [ ] 优化移动端体验
- [ ] 添加暗色模式
- [ ] Tailwind CSS 本地构建优化


