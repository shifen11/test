# 🚀 Zeabur 部署指南

## 部署前准备

### 1. 确保代码已推送到 Git 仓库

```bash
git add .
git commit -m "准备部署到 Zeabur"
git push origin main
```

## 在 Zeabur 中部署

### 步骤 1: 创建新项目

1. 登录 [Zeabur](https://zeabur.com)
2. 点击 "New Project"
3. 选择 "Deploy from Git Repository"
4. 连接你的 Git 仓库

### 步骤 2: 配置 MySQL 数据库

1. 在项目中点击 "Add Service"
2. 选择 "MySQL"
3. Zeabur 会自动创建 MySQL 服务
4. 记录数据库连接信息（会在环境变量中自动配置）

### 步骤 3: 配置环境变量

在项目设置中添加以下环境变量：

#### 必需的环境变量

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | `sk-xxxxx...` |
| `MYSQL_HOST` | MySQL 主机地址 | `sjc1.clusters.zeabur.com` |
| `MYSQL_PORT` | MySQL 端口 | `23645` |
| `MYSQL_USER` | MySQL 用户名 | `root` |
| `MYSQL_PASSWORD` | MySQL 密码 | `xxxxx` |
| `MYSQL_DATABASE` | MySQL 数据库名 | `zeabur` |

#### 可选的环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `FLASK_SECRET_KEY` | Flask Session 密钥 | 自动生成（建议设置） |
| `PORT` | 服务端口 | 自动分配（无需设置） |
| `FLASK_ENV` | Flask 环境 | `production` |

### 步骤 4: 部署

1. Zeabur 会自动检测到 `Procfile` 并开始构建
2. 构建完成后，应用会自动启动
3. 数据库表会在首次启动时自动创建

## 验证部署

### 1. 检查应用状态

在 Zeabur 控制台中查看应用状态，确保显示 "Running"

### 2. 访问应用

点击 Zeabur 提供的域名，访问应用首页

### 3. 测试功能

- 访问首页，查看界面是否正常加载
- 尝试发送一条消息，测试 API 是否正常
- 测试数据库连接（查询余额等功能）

## 常见问题

### 问题 1: 构建失败

**原因**: 依赖安装失败

**解决方案**:
- 检查 `requirements.txt` 是否包含所有依赖
- 查看构建日志，确认具体错误

### 问题 2: 应用启动失败

**原因**: 数据库连接失败

**解决方案**:
- 检查 MySQL 服务是否正常运行
- 验证环境变量是否正确配置
- 确认数据库连接信息是否正确

### 问题 3: 数据库表未创建

**原因**: 数据库初始化失败

**解决方案**:
- 查看应用日志，确认错误信息
- 手动运行数据库初始化（如果支持）
- 检查数据库权限

### 问题 4: 静态资源加载失败

**原因**: Tailwind CSS CDN 可能被阻止

**解决方案**:
- 检查网络连接
- 考虑使用本地构建的 Tailwind CSS（未来优化）

## 环境变量配置示例

如果使用 Zeabur 的 MySQL 服务，环境变量会自动配置。如果需要手动配置：

```bash
# 在 Zeabur 项目设置中添加
DEEPSEEK_API_KEY=sk-your-api-key-here
MYSQL_HOST=sjc1.clusters.zeabur.com
MYSQL_PORT=23645
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=zeabur
FLASK_SECRET_KEY=your-secret-key-here
```

## 监控和日志

### 查看日志

在 Zeabur 控制台中：
1. 进入项目
2. 点击应用服务
3. 查看 "Logs" 标签页

### 监控指标

Zeabur 会自动监控：
- CPU 使用率
- 内存使用率
- 网络流量
- 请求数量

## 更新部署

当代码更新后：

1. 推送到 Git 仓库
2. Zeabur 会自动检测更改
3. 自动重新构建和部署

## 回滚

如果需要回滚到之前的版本：

1. 在 Zeabur 控制台中找到 "Deployments"
2. 选择之前的部署版本
3. 点击 "Redeploy"

## 注意事项

1. **数据库连接**: 确保 MySQL 服务在应用之前启动
2. **环境变量**: 敏感信息（如 API Key）不要提交到代码仓库
3. **日志**: 定期查看日志，及时发现问题
4. **备份**: 定期备份数据库数据

## 支持

如遇到问题，可以：
- 查看 Zeabur 文档
- 检查应用日志
- 联系 Zeabur 支持团队

