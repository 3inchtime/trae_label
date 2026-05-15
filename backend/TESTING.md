# API 自动化测试说明

本文档说明如何运行后端 API 自动化测试脚本。

## 📋 测试覆盖范围

测试脚本覆盖以下所有 API 功能：

| 功能模块 | 测试用例数量 |
|---------|------------|
| **基础服务** | 2 |
| **时间戳转换** | 3 |
| **JSON格式化** | 4 |
| **MD5加密** | 4 |
| **数字转中文** | 3 |
| **RSA加密解密** | 3 |
| **在线计时器** | 8 |
| **重量单位换算** | 3 |
| **时间差计算** | 2 |
| **工具管理CRUD** | 3 |
| **总计** | **35** |

## 🚀 运行测试

### 前置条件

1. 确保后端服务已启动并运行在 `http://localhost:8000`
2. 确保已安装依赖（包括 `requests` 库）

### 启动后端服务

```bash
cd backend

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 运行测试脚本

在另一个终端窗口：

```bash
cd backend
python test_api.py
```

## 📊 测试输出说明

测试脚本会输出彩色的测试结果，包括：

- ✓ **PASS** (绿色) - 测试通过
- ✗ **FAIL** (红色) - 测试失败

每个测试模块会有详细的输出信息，例如：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▶ 健康检查测试
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✓ PASS 健康检查 - 状态码: 200
```

### 测试结果汇总

测试完成后会显示汇总信息：

```
============================================================
测试结果汇总
============================================================
总测试数: 35
✓ 通过: X
✗ 失败: X
============================================================
```

如果有失败的测试，会列出失败的测试名称和原因。

## 🔧 测试脚本功能

### 1. 基础服务测试

- **根路径**: 测试 `/` 端点是否正常响应
- **健康检查**: 测试 `/api/health` 端点

### 2. 时间戳转换测试

- 获取当前时间戳
- 时间戳转日期时间
- 日期时间转时间戳

### 3. JSON格式化测试

- 格式化JSON
- 压缩JSON
- 验证有效JSON
- 验证无效JSON

### 4. MD5加密测试

- MD5加密（小写）
- MD5加密（大写）
- MD5校验（匹配）
- MD5校验（不匹配）

### 5. 数字转中文测试

- 整数转中文
- 小数转中文
- 零转中文

### 6. RSA加密解密测试

- 生成RSA密钥对（2048位）
- RSA加密
- RSA解密

### 7. 在线计时器测试

- 创建计时器
- 获取计时器状态
- 启动计时器
- 暂停计时器
- 重置计时器
- 获取活跃计时器列表
- 获取历史记录
- 删除计时器

### 8. 重量单位换算测试

- 克转千克
- 千克转斤
- 磅转克

### 9. 时间差计算测试

- 计算时间差
- 跨月时间差计算

### 10. 工具管理CRUD测试

- 创建工具
- 获取工具列表
- 获取单个工具

## 💡 故障排除

### 问题：无法连接到后端服务

```
错误: 无法连接到后端服务!
请确保后端服务已启动: http://localhost:8000
启动命令: cd backend && uvicorn app.main:app --reload --port 8000
```

**解决方案**:
1. 确认后端服务是否启动
2. 确认端口是否为8000
3. 检查防火墙设置

### 问题：缺少requests库未安装

```
ModuleNotFoundError: No module named 'requests'
```

**解决方案**:
```bash
pip install requests==2.31.0
```

或安装所有依赖：
```bash
pip install -r requirements.txt
```

### 问题：部分测试失败

检查后端日志，查看详细的错误信息，然后根据错误信息排查问题。

## 📝 扩展测试

要添加新的测试用例，可以在 `test_api.py` 中添加新的测试函数：

```python
def test_new_feature(result: TestResult):
    """测试新功能"""
    print_section("新功能测试")
    
    try:
        response = requests.get(f"{BASE_URL}/api/tools/new-feature")
        passed = response.status_code == 200
        message = "新功能测试通过"
        result.add_test("新功能测试", passed, message)
        print_test("新功能测试", passed, message)
    except Exception as e:
        result.add_test("新功能测试", False, str(e))
        print_test("新功能测试", False, str(e))
```

然后在 `main()` 函数中调用新的测试函数。

## 🎯 CI/CD 集成

此测试脚本可以轻松集成到 CI/CD 流程中：

```bash
# 启动后端服务（后台运行）
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# 等待服务启动
sleep 10

# 运行测试
python test_api.py

# 检查测试结果
if [ $? -eq 0 ]; then
    echo "所有测试通过！"
else
    echo "有测试失败！"
    exit 1
fi
```

## 📄 许可证

MIT License
