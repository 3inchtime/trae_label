# 便携工具平台

基于 FastAPI + Vue 3 的前后端分离便携工具平台，提供多种实用的在线工具。

## ✨ 功能特性

### 🔧 已实现工具

| 工具名称 | 功能描述 |
|---------|---------|
| **时间戳转换** | 时间戳与日期时间格式互相转换，支持自定义格式 |
| **JSON格式化** | JSON 格式化、压缩、验证，支持自定义缩进 |
| **MD5加密** | MD5 哈希加密，支持大小写输出，哈希值校验 |
| **数字转中文** | 数字金额转中文大写金额，支持小数 |
| **RSA加密解密** | RSA 密钥生成、加密、解密，支持多种密钥长度 |
| **在线计时器** | 创建、启动、暂停、重置计时器，查看历史记录 |
| **重量单位换算** | 支持毫克、克、千克、吨、盎司、磅、斤、两等单位 |
| **时间差计算** | 计算两个时间的年、月、日、时、分、秒差值 |

### 🎨 界面特性

- 支持深色/浅色主题切换
- 响应式设计，支持移动端
- 简洁美观的现代化UI

## 🛠 技术栈

### 后端
- **框架**: FastAPI
- **ORM**: SQLAlchemy
- **数据库**: SQLite
- **依赖**:
  - `fastapi`: Web 框架
  - `uvicorn`: ASGI 服务器
  - `sqlalchemy`: ORM
  - `cryptography`: 加密库
  - `pydantic`: 数据验证

### 前端
- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **路由**: Vue Router
- **HTTP 客户端**: Axios

## 📁 项目结构

```
trae_label/
├── backend/                    # 后端 FastAPI 项目
│   ├── app/
│   │   ├── routers/           # API 路由
│   │   │   ├── __init__.py
│   │   │   ├── tools.py       # 工具管理 API
│   │   │   ├── timestamp.py   # 时间戳转换 API
│   │   │   ├── json_tools.py  # JSON 格式化 API
│   │   │   ├── md5_tools.py   # MD5 加密 API
│   │   │   ├── number_chinese.py # 数字转中文 API
│   │   │   ├── rsa_tools.py   # RSA 加密解密 API
│   │   │   ├── timer.py       # 计时器 API
│   │   │   ├── weight_convert.py # 重量换算 API
│   │   │   └── time_difference.py # 时间差计算 API
│   │   ├── __init__.py
│   │   ├── main.py            # 应用入口
│   │   ├── database.py        # 数据库配置
│   │   ├── models.py          # SQLAlchemy 数据模型
│   │   └── schemas.py         # Pydantic 数据模式
│   └── requirements.txt       # Python 依赖
├── frontend/                   # 前端 Vue 项目
│   ├── src/
│   │   ├── views/             # 页面组件
│   │   │   ├── Home.vue       # 首页
│   │   │   ├── Tools.vue      # 工具列表页
│   │   │   ├── TimestampTool.vue  # 时间戳转换页
│   │   │   ├── JsonTool.vue       # JSON 格式化页
│   │   │   ├── Md5Tool.vue        # MD5 加密页
│   │   │   ├── NumberToChinese.vue # 数字转中文页
│   │   │   ├── RsaTool.vue        # RSA 加密解密页
│   │   │   ├── TimerTool.vue      # 计时器页
│   │   │   ├── WeightConverter.vue # 重量换算页
│   │   │   └── TimeDifferenceTool.vue # 时间差计算页
│   │   ├── components/        # 通用组件
│   │   │   └── Icon.vue       # 图标组件
│   │   ├── router/            # 路由配置
│   │   │   └── index.js
│   │   ├── api/               # API 封装
│   │   │   └── index.js
│   │   ├── App.vue            # 根组件
│   │   ├── main.js            # 应用入口
│   │   └── style.css          # 全局样式
│   ├── index.html
│   ├── vite.config.js
│   ├── package-lock.json
│   └── package.json
├── scripts/                    # 启动脚本
│   ├── start.sh               # macOS/Linux 启动脚本
│   └── start.bat              # Windows 启动脚本
├── run.py                     # 主启动脚本
└── README.md
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+

### 启动方式

#### 方式一：使用主启动脚本（推荐）

```bash
# 同时启动前后端服务
python3 run.py

# 或仅启动后端
python3 run.py --backend-only

# 或仅启动前端
python3 run.py --frontend-only

# 仅安装依赖，不启动服务
python3 run.py --install-only
```

#### 方式二：使用平台专用脚本

**macOS/Linux:**
```bash
./scripts/start.sh
```

**Windows:**
```cmd
scripts\start.bat
```

#### 方式三：手动启动

**启动后端:**
```bash
cd backend
python -m venv venv

# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**启动前端:**
```bash
cd frontend
npm install
npm run dev
```

## 🌐 访问地址

- **前端页面**: http://localhost:5173
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs (Swagger UI)
- **ReDoc 文档**: http://localhost:8000/redoc

## 📚 API 文档

### 时间戳转换
- `POST /api/tools/timestamp/convert` - 时间戳与日期时间互转
- `GET /api/tools/timestamp/now` - 获取当前时间戳

### JSON 格式化
- `POST /api/tools/json/format` - 格式化和压缩 JSON
- `POST /api/tools/json/validate` - 验证 JSON 有效性

### MD5 加密
- `POST /api/tools/md5/encrypt` - MD5 加密
- `POST /api/tools/md5/compare` - 校验 MD5 哈希

### 数字转中文
- `POST /api/tools/number-to-chinese` - 数字转中文大写金额

### RSA 加密解密
- `POST /api/tools/rsa/generate-keys` - 生成 RSA 密钥对
- `POST /api/tools/rsa/encrypt` - RSA 加密
- `POST /api/tools/rsa/decrypt` - RSA 解密

### 在线计时器
- `POST /api/tools/timer/create` - 创建计时器
- `POST /api/tools/timer/{id}/start` - 启动计时器
- `POST /api/tools/timer/{id}/pause` - 暂停计时器
- `POST /api/tools/timer/{id}/reset` - 重置计时器
- `GET /api/tools/timer/{id}/status` - 获取计时器状态
- `DELETE /api/tools/timer/{id}` - 删除计时器
- `GET /api/tools/timer/active` - 获取所有活跃计时器
- `GET /api/tools/timer/history` - 获取历史记录

### 重量单位换算
- `POST /api/tools/weight/convert` - 重量单位转换

### 时间差计算
- `POST /api/tools/time-difference/calculate` - 计算时间差

## 🔧 开发说明

### 后端开发

- API 文档自动生成，访问 `/docs` 查看 Swagger UI
- 数据库文件自动创建在 `backend/tools.db`
- 添加新工具请在 `backend/app/routers/` 目录下创建新的路由文件，并在 `main.py` 中注册
- 数据模型定义在 `models.py`，Pydantic 模式定义在 `schemas.py`

### 前端开发

- 前端已配置代理，所有 `/api` 请求会转发到后端
- 页面组件放在 `src/views/` 目录
- API 封装在 `src/api/index.js`
- 路由配置在 `src/router/index.js`
- 全局样式和 CSS 变量定义在 `src/style.css`

## 📝 开发计划

- [ ] 添加更多实用工具（如二维码生成、密码生成器等）
- [ ] 工具使用统计
- [ ] 用户收藏功能
- [ ] 工具历史记录
- [ ] 更多主题支持

## 📄 许可证

MIT
