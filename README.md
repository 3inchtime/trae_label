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
| **万年历** | 农历、节气、节假日查询，支持月份浏览 |
| **长度单位换算** | 支持公制、英制、市制单位换算 |
| **颜色选择器** | 可视化选择颜色，支持 HEX/RGB/HSL 格式转换、配色方案生成 |
| **URL 编解码** | URL 编码与解码，支持自定义安全字符，处理中文和特殊字符 |
| **YAML 格式校验** | 验证 YAML 格式正确性，支持格式化和错误行号、列号定位 |
| **反应速度测试** | 测试你的反应速度，颜色变绿时尽快点击，记录反应时间 |

### 🎨 界面特性

- 支持深色/浅色主题切换（本地存储持久化）
- 响应式设计，支持移动端
- 毛玻璃效果现代化 UI
- 流畅的动画过渡效果

## 🛠 技术栈

### 后端
- **框架**: FastAPI 0.109.0
- **ORM**: SQLAlchemy 2.0.25
- **数据库**: SQLite
- **数据验证**: Pydantic 2.5.3
- **加密库**: cryptography 41.0.7
- **ASGI 服务器**: Uvicorn 0.27.0
- **YAML 解析**: PyYAML 6.0.1
- **依赖**:
  - `fastapi`: Web 框架，高性能异步支持
  - `sqlalchemy`: ORM 数据持久化
  - `pydantic`: 数据验证与序列化
  - `cryptography`: 加密算法实现
  - `python-multipart`: 表单数据处理
  - `pyyaml`: YAML 格式解析与验证

### 前端
- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite 5.0.0
- **路由**: Vue Router 4.2.5
- **HTTP 客户端**: Axios 1.6.5
- **样式**: CSS 变量 + 毛玻璃设计系统

## 🏗 项目架构分析

### 整体架构

项目采用**前后端分离架构**，遵循 RESTful API 设计规范：

```
┌─────────────────────────────────────────────────────────┐
│                        客户端浏览器                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   首页视图     │  │  工具列表页   │  │  各工具页面    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│           │                     │                       │
│           └─────────────────────┼───────────────────────┘
│                                 │
├─────────────────────────────────┼─────────────────────────┤
│                                 ▼                         │
│           ┌──────────────────────────────────┐           │
│           │          Vue Router              │           │
│           └──────────────────────────────────┘           │
│                                 │                         │
│                                 ▼                         │
│           ┌──────────────────────────────────┐           │
│           │           Axios                 │           │
│           └──────────────────────────────────┘           │
│                                 │                         │
└─────────────────────────────────┼─────────────────────────┘
                                  │ HTTP/HTTPS
                                  │
┌─────────────────────────────────┼─────────────────────────┐
│                                 ▼                         │
│           ┌──────────────────────────────────┐           │
│           │         FastAPI (Uvicorn)        │           │
│           └──────────────────────────────────┘           │
│                                 │                         │
│           ┌──────────────────────────────────┐           │
│           │         API 路由层 (Routers)     │           │
│           │  - tools                         │           │
│           │  - timestamp, json, md5, etc.   │           │
│           └──────────────────────────────────┘           │
│                                 │                         │
│           ┌──────────────────────────────────┐           │
│           │       数据模型层 (Models)        │           │
│           │  - SQLAlchemy ORM                │           │
│           └──────────────────────────────────┘           │
│                                 │                         │
│           ┌──────────────────────────────────┐           │
│           │     数据验证层 (Schemas)         │           │
│           │  - Pydantic 请求/响应模型        │           │
│           └──────────────────────────────────┘           │
│                                 │                         │
│           ┌──────────────────────────────────┐           │
│           │         SQLite 数据库            │           │
│           └──────────────────────────────────┘           │
└───────────────────────────────────────────────────────────┘
```

### 后端架构设计

#### 1. 模块化路由设计
```
backend/app/
├── main.py              # 应用入口，CORS 配置，路由注册
├── database.py          # 数据库连接配置，Session 管理
├── models.py            # SQLAlchemy ORM 数据模型
├── schemas.py           # Pydantic 数据验证模型
└── routers/             # API 路由模块（每个工具独立路由文件）
    ├── tools.py         # 工具管理 API
    ├── timestamp.py     # 时间戳转换 API
    ├── json_tools.py    # JSON 格式化 API
    ├── md5_tools.py     # MD5 加密 API
    ├── number_chinese.py # 数字转中文 API
    ├── rsa_tools.py     # RSA 加密解密 API
    ├── timer.py         # 计时器 API
    ├── weight_convert.py # 重量换算 API
    ├── time_difference.py # 时间差计算 API
    ├── calendar.py      # 万年历 API
    ├── length_convert.py # 长度换算 API
    ├── url_tools.py     # URL 编解码 API
    └── yaml_tools.py    # YAML 验证格式化 API
```

**设计亮点**:
- **单一职责原则**: 每个路由文件只负责一个工具功能
- **易于扩展**: 新增工具只需创建新的路由文件并注册
- **清晰的分层**: 路由层只负责 HTTP 协议处理，业务逻辑内聚

#### 2. 数据模型与验证分层
- **Models 层** (`models.py`): 定义数据库表结构，使用 SQLAlchemy ORM
- **Schemas 层** (`schemas.py`): 定义 API 请求/响应数据结构，使用 Pydantic 进行数据验证
- **关注点分离**: 数据库模型与 API 模型分离，便于独立演进

#### 3. 数据库设计
```python
# Tool 模型 - 工具元数据管理
- id: Integer (主键)
- name: String (工具名称)
- description: String (工具描述)
- category: String (工具分类)
- created_at: DateTime (创建时间)
- updated_at: DateTime (更新时间)
```

**当前局限**: 仅定义了基础工具元数据，尚未充分利用

### 前端架构设计

#### 1. 组件化架构
```
frontend/src/
├── main.js              # 应用入口
├── App.vue              # 根组件（布局、主题切换）
├── style.css            # 全局样式与设计系统
├── config/
│   └── toolsConfig.js   # 工具配置文件
├── router/
│   └── index.js         # 路由配置
├── api/
│   └── index.js         # API 请求封装
├── components/
│   └── Icon.vue         # 图标组件
└── views/               # 页面视图组件
    ├── Home.vue         # 首页
    ├── Tools.vue        # 工具列表页
    ├── TimestampTool.vue
    ├── JsonTool.vue
    ├── Md5Tool.vue
    ├── NumberToChinese.vue
    ├── RsaTool.vue
    ├── TimerTool.vue
    ├── WeightConverter.vue
    ├── TimeDifferenceTool.vue
    ├── CalendarTool.vue
    ├── LengthConverter.vue
    ├── ColorPicker.vue
    ├── UrlTool.vue
    ├── YamlTool.vue
    └── ReactionTest.vue
```

#### 2. 设计系统
- **CSS 变量驱动**: 使用 CSS 自定义属性定义完整的设计令牌（颜色、间距、阴影、圆角、过渡）
- **主题切换**: 支持深色/浅色模式，通过 `:root` 和 `.dark` 类切换
- **毛玻璃效果**: 统一的 `backdrop-filter` 毛玻璃风格
- **动画系统**: 预定义的渐入、悬浮、脉冲等动画效果

#### 3. 响应式布局
- 桌面端: 侧边导航 + 主内容区
- 平板端: 简化侧边栏
- 移动端: 隐藏侧边栏，顶部导航精简

### 核心设计模式

#### 1. 工厂模式 (启动脚本)
`run.py` 实现了完整的开发环境自动化：
- 虚拟环境自动创建
- 依赖自动安装
- 前后端服务并发启动
- 优雅的信号处理与退出

#### 2. 依赖注入 (FastAPI)
- 数据库 Session 依赖注入
- 路由依赖分层管理

#### 3. 观察者模式 (Vue 响应式)
- `watch` 监听主题变化，自动持久化到 localStorage
- `ref` 响应式状态管理

#### 4. 策略模式 (单位换算)
- 重量/长度换算使用字典存储单位换算因子
- 统一的转换算法，支持多种单位策略

#### 5. 配置驱动模式 (工具管理)
- 使用 `toolsConfig.js` 统一配置所有工具的元数据
- 新增工具只需在配置文件中添加条目，自动在列表中显示
- 工具名称、描述、图标、路由等信息集中管理

### 代码质量评估

| 维度 | 评分 | 说明 |
|------|------|------|
| **架构设计** | ⭐⭐⭐⭐ | 分层清晰，模块化良好，易于扩展 |
| **代码风格** | ⭐⭐⭐⭐ | 命名规范，结构清晰 |
| **错误处理** | ⭐⭐⭐ | 基础 HTTP 异常处理，缺少业务异常 |
| **测试覆盖** | ⭐⭐⭐ | 49个集成测试用例，覆盖所有后端API |
| **文档完整性** | ⭐⭐⭐⭐ | API 文档自动生成，README 完善 |
| **类型安全** | ⭐⭐⭐⭐ | Pydantic 提供完整类型验证 |

## 📁 项目结构

```
trae_label/
├── backend/                    # 后端 FastAPI 项目
│   ├── app/
│   │   ├── routers/           # API 路由（14个工具模块）
│   │   │   ├── __init__.py
│   │   │   ├── tools.py       # 工具管理 API
│   │   │   ├── timestamp.py   # 时间戳转换 API
│   │   │   ├── json_tools.py  # JSON 格式化 API
│   │   │   ├── md5_tools.py   # MD5 加密 API
│   │   │   ├── number_chinese.py # 数字转中文 API
│   │   │   ├── rsa_tools.py   # RSA 加密解密 API
│   │   │   ├── timer.py       # 计时器 API
│   │   │   ├── weight_convert.py # 重量换算 API
│   │   │   ├── time_difference.py # 时间差计算 API
│   │   │   ├── calendar.py    # 万年历 API
│   │   │   ├── length_convert.py # 长度换算 API
│   │   │   ├── url_tools.py   # URL 编解码 API
│   │   │   └── yaml_tools.py  # YAML 验证格式化 API
│   │   ├── __init__.py
│   │   ├── main.py            # 应用入口
│   │   ├── database.py        # 数据库配置
│   │   ├── models.py          # SQLAlchemy 数据模型
│   │   └── schemas.py         # Pydantic 数据模式（25+ 数据模型）
│   ├── requirements.txt       # Python 依赖
│   ├── test_api.py           # API 测试脚本
│   ├── test_api_integration.py # 集成测试脚本
│   └── TESTING.md            # 测试说明文档
├── frontend/                   # 前端 Vue 项目
│   ├── src/
│   │   ├── views/             # 页面视图（16个页面组件）
│   │   │   ├── Home.vue       # 首页
│   │   │   ├── Tools.vue      # 工具列表页
│   │   │   ├── TimestampTool.vue  # 时间戳转换页
│   │   │   ├── JsonTool.vue       # JSON 格式化页
│   │   │   ├── Md5Tool.vue        # MD5 加密页
│   │   │   ├── NumberToChinese.vue # 数字转中文页
│   │   │   ├── RsaTool.vue        # RSA 加密解密页
│   │   │   ├── TimerTool.vue      # 计时器页
│   │   │   ├── WeightConverter.vue # 重量换算页
│   │   │   ├── TimeDifferenceTool.vue # 时间差计算页
│   │   │   ├── CalendarTool.vue    # 万年历页
│   │   │   ├── LengthConverter.vue # 长度换算页
│   │   │   ├── ColorPicker.vue     # 颜色选择器页
│   │   │   ├── UrlTool.vue         # URL 编解码页
│   │   │   ├── YamlTool.vue        # YAML 验证页
│   │   │   └── ReactionTest.vue    # 反应速度测试页
│   │   ├── components/        # 通用组件
│   │   │   └── Icon.vue       # 图标组件
│   │   ├── config/            # 配置文件
│   │   │   └── toolsConfig.js # 工具列表配置
│   │   ├── router/            # 路由配置
│   │   │   └── index.js
│   │   ├── api/               # API 封装
│   │   │   └── index.js
│   │   ├── App.vue            # 根组件
│   │   ├── main.js            # 应用入口
│   │   └── style.css          # 全局样式与设计系统
│   ├── index.html
│   ├── vite.config.js
│   ├── package-lock.json
│   └── package.json
├── scripts/                    # 启动脚本
│   ├── start.sh               # macOS/Linux 启动脚本
│   └── start.bat              # Windows 启动脚本
├── run.py                     # 主启动脚本（跨平台）
├── .gitignore
└── README.md                  # 项目文档
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

## 🧪 自动化测试

项目包含完整的后端 API 自动化测试，覆盖 14 个功能模块，共 49 个测试用例。

### 运行测试

**集成测试（推荐，无需启动服务）:**
```bash
cd backend
source venv/bin/activate
python test_api_integration.py
```

**API 测试（需要启动后端服务）:**
```bash
cd backend
python test_api.py
```

详细测试说明请参考 [TESTING.md](backend/TESTING.md)

## 📚 API 文档

### 基础服务
- `GET /` - 根路径欢迎信息
- `GET /api/health` - 健康检查

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

### 万年历
- `POST /api/tools/calendar/month` - 获取指定月份日历信息
- `GET /api/tools/calendar/today` - 获取今日详细信息

### 长度单位换算
- `POST /api/tools/length/convert` - 长度单位转换

### 颜色选择器
- *注：纯前端工具，无需后端API*

### URL 编解码
- `POST /api/tools/url/encode` - URL 编码
- `POST /api/tools/url/decode` - URL 解码

### YAML 格式校验
- `POST /api/tools/yaml/validate` - 验证 YAML 格式
- `POST /api/tools/yaml/format` - 格式化 YAML

### 反应速度测试
- *注：纯前端工具，无需后端API*

## 🔧 开发说明

### 后端开发

- API 文档自动生成，访问 `/docs` 查看 Swagger UI
- 数据库文件自动创建在 `backend/tools.db`
- 添加新工具请在 `backend/app/routers/` 目录下创建新的路由文件，并在 `main.py` 中注册
- 数据模型定义在 `models.py`，Pydantic 模式定义在 `schemas.py`

**新增工具开发流程**:
1. 在 `schemas.py` 中定义请求/响应模型（如需要后端支持）
2. 在 `routers/` 下创建新的路由文件，实现业务逻辑（如需要后端支持）
3. 在 `main.py` 中注册新路由
4. 在前端 `src/config/toolsConfig.js` 中添加工具配置
5. 在前端 `router/index.js` 中添加路由配置
6. 创建对应的 Vue 视图组件
7. 如需要后端支持，在 `test_api_integration.py` 中添加集成测试用例

### 前端开发

- 前端已配置代理，所有 `/api` 请求会转发到后端
- 页面组件放在 `src/views/` 目录
- API 封装在 `src/api/index.js`
- 路由配置在 `src/router/index.js`
- 全局样式和 CSS 变量定义在 `src/style.css`
- 工具配置统一在 `src/config/toolsConfig.js` 中管理

### 开发规范

#### Python 后端规范
- 遵循 PEP 8 代码风格
- 使用类型注解（Type Hints）
- 所有 API 必须定义 Pydantic 模型进行输入输出验证
- 错误处理使用 `HTTPException`，提供明确的状态码和错误信息
- 新增功能必须添加对应的集成测试用例

#### Vue 前端规范
- 使用 Composition API（`<script setup>` 语法）
- 组件命名使用 PascalCase
- Props 定义必须包含类型和默认值
- 使用 CSS 变量，避免硬编码颜色、尺寸
- 新增工具必须更新 `toolsConfig.js` 配置文件

## 🗺 功能迭代计划

### 🎯 短期规划 (v1.1 - v1.2, 1-2个月)

#### v1.1: 核心功能增强
- [ ] **二维码工具**
  - 二维码生成（支持自定义内容、尺寸、颜色）
  - 二维码解析（上传图片识别）
  - 支持 Logo 嵌入

- [ ] **密码生成器**
  - 可配置密码长度、字符类型（大小写、数字、特殊字符）
  - 密码强度实时评估
  - 密码历史记录（本地存储）

- [ ] **Base64 编解码**
  - 文本编码/解码
  - 图片编码/解码
  - 文件编码/解码

#### v1.2: 用户体验优化
- [ ] **工具收藏功能**
  - 点击收藏常用工具
  - 首页展示收藏工具列表
  - 本地存储持久化

- [ ] **使用历史记录**
  - 每个工具自动保存最近使用记录
  - 一键重新使用历史输入
  - 历史记录搜索和清理

- [ ] **工具搜索**
  - 顶部全局搜索框
  - 支持按名称、功能描述搜索
  - 搜索结果快速跳转

- [ ] **键盘快捷键**
  - 常用操作快捷键支持
  - 快捷键帮助面板

### 🚀 中期规划 (v1.3 - v1.5, 3-6个月)

#### v1.3: 数据持久化与用户系统
- [ ] **用户注册/登录**
  - JWT 认证系统
  - 邮箱验证
  - 密码重置

- [ ] **云端数据同步**
  - 收藏夹云端同步
  - 使用历史云端存储
  - 跨设备数据同步

- [ ] **工具使用统计**
  - 个人使用统计看板
  - 各工具使用频率
  - 使用热力图

#### v1.4: 更多实用工具
- [ ] **图片处理工具集**
  - 图片压缩（支持质量调节）
  - 图片格式转换（JPG, PNG, WebP）
  - 图片尺寸调整
  - 图片旋转/翻转
  - 图片滤镜

- [ ] **文本处理工具集**
  - 文本去重
  - 文本排序
  - 大小写转换
  - 去除空格/空行
  - 正则表达式测试器

#### v1.5: 高级功能
- [ ] **批量处理**
  - 支持批量文件上传处理
  - 批量图片压缩
  - 批量格式转换

- [ ] **自定义工作流**
  - 多个工具串联使用
  - 保存常用处理流程
  - 一键执行工作流

- [ ] **工具快捷键配置**
  - 自定义全局快捷键
  - 导入/导出快捷键配置

### 🌟 长期规划 (v2.0+, 6个月以上)

#### v2.0: 平台化升级
- [ ] **插件系统**
  - 第三方开发者可以开发工具插件
  - 插件市场
  - 插件审核与安全检查

- [ ] **工具模板**
  - 快速开发新工具的模板
  - 可视化工具配置
  - 无需编码创建简单工具

- [ ] **团队协作**
  - 团队空间
  - 共享工具收藏
  - 协作处理任务

#### v2.1: AI 增强
- [ ] **AI 智能助手**
  - 自然语言描述需求，智能推荐工具
  - 工具使用指导
  - 常见问题解答

- [ ] **AI 内容处理**
  - AI 文本润色
  - AI 图片增强
  - AI 代码解释

#### v2.2: 生态扩展
- [ ] **桌面应用**
  - Electron 打包
  - 离线使用
  - 系统级集成

- [ ] **移动端 App**
  - iOS/Android 原生应用
  - 触摸优化界面
  - 移动端专属功能

- [ ] **浏览器扩展**
  - Chrome/Firefox 扩展
  - 右键菜单工具
  - 网页内容快速处理

## 📊 版本历史

| 版本 | 发布日期 | 主要功能 |
|------|----------|----------|
| v1.0 | 2024-01 | 初始版本，10个核心工具 |
| v1.1 | 2024-02 | 新增4个工具：颜色选择器、URL编解码、YAML验证、反应速度测试 |

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 贡献流程
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码审查标准
- 代码风格符合项目规范
- 包含必要的测试（后端工具需添加集成测试）
- 更新相关文档（README.md 等）
- 不破坏现有功能

## 📄 许可证

MIT License

---

**如果这个项目对你有帮助，欢迎 Star ⭐ 支持！**
