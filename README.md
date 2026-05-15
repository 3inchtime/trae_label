# 便携工具平台

基于 FastAPI + Vue 3 的前后端分离便携工具平台。

## 技术栈

- **后端**: FastAPI + SQLAlchemy + SQLite
- **前端**: Vue 3 + Vite + Vue Router + Axios
- **数据库**: SQLite

## 项目结构

```
trae_label/
├── backend/              # 后端 FastAPI 项目
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py      # API 主入口
│   │   ├── database.py  # 数据库配置
│   │   ├── models.py    # 数据模型
│   │   └── schemas.py   # Pydantic 模式
│   └── requirements.txt # Python 依赖
├── frontend/             # 前端 Vue 项目
│   ├── src/
│   │   ├── views/       # 页面组件
│   │   ├── router/      # 路由配置
│   │   ├── api/         # API 封装
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── scripts/              # 启动脚本
│   ├── start.sh         # macOS/Linux 启动脚本
│   └── start.bat        # Windows 启动脚本
├── run.py               # 主启动脚本
└── README.md
```

## 快速开始

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

## 访问地址

- **前端页面**: http://localhost:5173
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs

## 开发说明

### 后端开发

- API 文档自动生成，访问 `/docs` 查看 Swagger UI
- 数据库文件自动创建在 `backend/tools.db`
- 添加新工具请在 `backend/app/` 目录下扩展

### 前端开发

- 前端已配置代理，所有 `/api` 请求会转发到后端
- 页面组件放在 `src/views/`
- API 封装在 `src/api/index.js`

## 许可证

MIT
