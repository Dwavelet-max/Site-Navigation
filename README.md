# Site Navigation - 站点导航

一个功能强大的站点管理系统，支持统一管理收藏的站点URL，并提供完整的离线保存功能。

## 项目简介

Site Navigation 是一个基于 Python Flask 的 Web 应用程序，帮助用户管理和收藏常用的网站链接，并提供一键离线保存功能，确保重要网页内容永不丢失。

## 核心功能

### 站点管理
- 添加站点（URL、标题、分类、备注）
- 编辑站点信息
- 删除站点
- 站点列表展示（支持分类筛选、搜索）
- 站点分类管理

### 离线保存
- 一键保存页面 HTML（包含CSS、图片等静态资源）
- 页面截图保存
- 离线内容查看（离线浏览保存的页面）
- 离线内容下载

### 数据统计
- 站点总数统计
- 各分类站点数量
- 保存率统计
- 分类分布图表展示

### Excel 导出
- 一键导出所有站点信息到 Excel 文件
- 包含标题、URL、分类、备注、时间等信息
- 支持离线备份和数据迁移

## 技术架构

### 后端技术
- **Python 3.11+** - 主要编程语言
- **Flask 3.0.0** - Web 框架
- **SQLAlchemy 2.0.23** - ORM 框架
- **SQLite** - 轻量级数据库
- **Gunicorn** - WSGI 服务器

### 前端技术
- **Vue 3** - 前端框架（CDN 引入）
- **ECharts 5.4.3** - 图表库
- **原生 CSS** - 样式设计

### 离线保存
- **requests** - HTML 内容下载
- **BeautifulSoup4** - HTML 解析
- **lxml** - XML/HTML 解析器
- **playwright** - 页面截图

### 其他依赖
- **Flask-Session** - 会话管理
- **openpyxl** - Excel 文件生成

## 项目结构

```
sitevault/
├── app.py              # Flask 主应用文件
├── models.py           # 数据模型定义
├── snapshot.py         # 离线保存逻辑
├── requirements.txt    # Python 依赖包
├── static/
│   └── uploads/       # 保存的离线内容
├── templates/
│   └── index.html     # 前端页面
└── instance/
    └── sitevault.db   # SQLite 数据库文件
```

## 数据模型

### Site (站点)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| user_id | Integer | 用户ID |
| url | String | 站点URL |
| title | String | 站点标题 |
| category_id | Integer | 分类ID（外键） |
| note | String | 备注 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |
| snapshot_path | String | 离线HTML路径 |
| screenshot_path | String | 截图路径 |

### Category (分类)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| user_id | Integer | 用户ID |
| name | String | 分类名称 |

### User (用户)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| username | String | 用户名 |
| password_hash | String | 密码哈希 |
| created_at | DateTime | 创建时间 |

## API 接口

### 认证相关
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/logout` - 用户登出
- `GET /api/auth/check` - 检查登录状态
- `PUT /api/auth/password` - 修改密码
- `GET /api/auth/user` - 获取用户信息

### 站点管理
- `GET /api/sites` - 获取站点列表（支持分类筛选、搜索）
- `POST /api/sites` - 添加站点
- `PUT /api/sites/{id}` - 更新站点
- `DELETE /api/sites/{id}` - 删除站点
- `POST /api/sites/{id}/snapshot` - 保存离线快照
- `GET /api/sites/{id}/view` - 查看离线内容
- `GET /api/sites/export` - 导出站点列表为 Excel

### 分类管理
- `GET /api/categories` - 获取分类列表
- `POST /api/categories` - 添加分类
- `DELETE /api/categories/{id}` - 删除分类

### 统计数据
- `GET /api/stats` - 获取统计数据

## 快速开始

### 使用 Docker Compose（推荐）

1. 克隆项目
```bash
git clone <repository-url>
cd zhandian
```

2. 启动服务
```bash
docker-compose up -d
```

3. 访问应用
```
http://localhost:5000
```

### 手动安装

1. 安装依赖
```bash
pip install -r sitevault/requirements.txt
```

2. 初始化数据库
```bash
cd sitevault
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

3. 启动应用
```bash
gunicorn --bind 0.0.0.0:5000 sitevault.app:app
```

## 默认账户

系统初始化时会创建默认管理员账户：
- 用户名：`admin`
- 密码：`admin123`

**注意：首次登录后请立即修改密码！**


## 功能特性

- 用户认证系统（注册、登录、登出）
- 数据隔离（每个用户只能访问自己的数据）
- 响应式设计（支持移动端访问）
- 实时搜索和筛选
- 数据统计可视化
- Excel 导出功能
- 离线内容保存和查看

## 开发说明

### 添加新功能
1. 在 `app.py` 中添加 API 路由
2. 在 `templates/index.html` 中添加前端界面
3. 在 `models.py` 中定义数据模型（如需要）
4. 在 `requirements.txt` 中添加新依赖（如需要）

### 数据库迁移
项目使用 SQLAlchemy ORM，修改数据模型后需要重新创建数据库表。

## 部署说明

### Docker 部署
项目包含 `Dockerfile` 和 `docker-compose.yml`，可以直接使用 Docker 部署。

### 生产环境建议
- 使用环境变量管理敏感配置
- 配置 HTTPS 证书
- 设置适当的日志级别
- 配置数据库备份策略
- 使用专业的 WSGI 服务器（如 Gunicorn + Nginx）

## 许可证

本项目仅供学习和个人使用。

## 贡献

欢迎提交 Issue 和 Pull Request！
