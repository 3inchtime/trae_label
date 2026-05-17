#!/usr/bin/env python3
"""
便携工具平台 API 自动化测试脚本 (集成测试版本)
使用 FastAPI TestClient 进行测试，无需启动独立服务
"""

import sys
import os

# 添加 app 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from starlette.testclient import TestClient
from app.main import app
import time
from typing import List, Tuple

client = TestClient(app, raise_server_exceptions=False)


class Colors:
    """终端输出颜色"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


class TestResult:
    """测试结果统计"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests: List[Tuple[str, bool, str]] = []
    
    def add_test(self, name: str, passed: bool, message: str = ""):
        self.tests.append((name, passed, message))
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        print(f"\n{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}测试结果汇总{Colors.ENDC}")
        print(f"{'='*60}")
        print(f"总测试数: {len(self.tests)}")
        print(f"{Colors.GREEN}✓ 通过: {self.passed}{Colors.ENDC}")
        print(f"{Colors.RED}✗ 失败: {self.failed}{Colors.ENDC}")
        print(f"{'='*60}")
        
        if self.failed > 0:
            print(f"\n{Colors.RED}失败的测试:{Colors.ENDC}")
            for name, passed, msg in self.tests:
                if not passed:
                    print(f"  - {name}: {msg}")
        
        print(f"\n{Colors.BOLD}{'='*60}{Colors.ENDC}")


def print_section(title: str):
    """打印测试章节标题"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'━'*60}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}▶ {title}{Colors.ENDC}")
    print(f"{Colors.BLUE}{'━'*60}{Colors.ENDC}")


def print_test(name: str, passed: bool, message: str = ""):
    """打印单个测试结果"""
    status = f"{Colors.GREEN}✓ PASS{Colors.ENDC}" if passed else f"{Colors.RED}✗ FAIL{Colors.ENDC}"
    msg = f" - {message}" if message else ""
    print(f"  {status} {name}{msg}")


def test_health_check(result: TestResult):
    """测试健康检查接口"""
    print_section("健康检查测试")
    
    try:
        response = client.get("/api/health")
        passed = response.status_code == 200
        message = f"状态码: {response.status_code}"
        result.add_test("健康检查", passed, message)
        print_test("健康检查", passed, message)
    except Exception as e:
        result.add_test("健康检查", False, str(e))
        print_test("健康检查", False, str(e))


def test_root_endpoint(result: TestResult):
    """测试根路径接口"""
    try:
        response = client.get("/")
        passed = response.status_code == 200 and "message" in response.json()
        message = f"状态码: {response.status_code}"
        result.add_test("根路径", passed, message)
        print_test("根路径", passed, message)
    except Exception as e:
        result.add_test("根路径", False, str(e))
        print_test("根路径", False, str(e))


def test_timestamp(result: TestResult):
    """测试时间戳转换"""
    print_section("时间戳转换测试")
    
    # 测试获取当前时间戳
    try:
        response = client.get("/api/tools/timestamp/now")
        data = response.json()
        passed = response.status_code == 200 and "timestamp" in data and "datetime_str" in data
        message = f"当前时间戳: {data.get('timestamp')}"
        result.add_test("获取当前时间戳", passed, message)
        print_test("获取当前时间戳", passed, message)
    except Exception as e:
        result.add_test("获取当前时间戳", False, str(e))
        print_test("获取当前时间戳", False, str(e))
    
    # 测试时间戳转日期时间
    try:
        payload = {"timestamp": 1700000000, "format": "%Y-%m-%d %H:%M:%S"}
        response = client.post("/api/tools/timestamp/convert", json=payload)
        data = response.json()
        passed = response.status_code == 200 and "datetime_str" in data
        message = f"转换结果: {data.get('datetime_str')}"
        result.add_test("时间戳转日期时间", passed, message)
        print_test("时间戳转日期时间", passed, message)
    except Exception as e:
        result.add_test("时间戳转日期时间", False, str(e))
        print_test("时间戳转日期时间", False, str(e))
    
    # 测试日期时间转时间戳
    try:
        payload = {"datetime_str": "2024-01-01 00:00:00", "format": "%Y-%m-%d %H:%M:%S"}
        response = client.post("/api/tools/timestamp/convert", json=payload)
        data = response.json()
        passed = response.status_code == 200 and "timestamp" in data
        message = f"转换结果: {data.get('timestamp')}"
        result.add_test("日期时间转时间戳", passed, message)
        print_test("日期时间转时间戳", passed, message)
    except Exception as e:
        result.add_test("日期时间转时间戳", False, str(e))
        print_test("日期时间转时间戳", False, str(e))


def test_json_tools(result: TestResult):
    """测试JSON格式化工具"""
    print_section("JSON格式化测试")
    
    test_json = '{"name": "test", "value": 123}'
    
    # 测试格式化JSON
    try:
        payload = {"json_str": test_json, "indent": 2}
        response = client.post("/api/tools/json/format", json=payload)
        data = response.json()
        passed = response.status_code == 200 and data.get("valid") == True
        message = "格式化成功"
        result.add_test("格式化JSON", passed, message)
        print_test("格式化JSON", passed, message)
    except Exception as e:
        result.add_test("格式化JSON", False, str(e))
        print_test("格式化JSON", False, str(e))
    
    # 测试压缩JSON
    try:
        payload = {"json_str": test_json, "indent": 2}
        response = client.post("/api/tools/json/format", json=payload)
        data = response.json()
        passed = response.status_code == 200 and "minified" in data
        message = f"压缩结果: {str(data.get('minified'))[:30]}..."
        result.add_test("压缩JSON", passed, message)
        print_test("压缩JSON", passed, message)
    except Exception as e:
        result.add_test("压缩JSON", False, str(e))
        print_test("压缩JSON", False, str(e))
    
    # 测试验证有效JSON
    try:
        payload = {"json_str": test_json}
        response = client.post("/api/tools/json/validate", json=payload)
        data = response.json()
        passed = response.status_code == 200 and data.get("valid") == True
        message = "有效JSON验证通过"
        result.add_test("验证有效JSON", passed, message)
        print_test("验证有效JSON", passed, message)
    except Exception as e:
        result.add_test("验证有效JSON", False, str(e))
        print_test("验证有效JSON", False, str(e))
    
    # 测试验证无效JSON
    try:
        payload = {"json_str": '{"invalid": json}'}
        response = client.post("/api/tools/json/validate", json=payload)
        data = response.json()
        passed = response.status_code == 200 and data.get("valid") == False
        message = "无效JSON验证通过"
        result.add_test("验证无效JSON", passed, message)
        print_test("验证无效JSON", passed, message)
    except Exception as e:
        result.add_test("验证无效JSON", False, str(e))
        print_test("验证无效JSON", False, str(e))


def test_md5_tools(result: TestResult):
    """测试MD5加密工具"""
    print_section("MD5加密测试")
    
    test_text = "Hello, World!"
    
    # 测试MD5加密
    try:
        payload = {"text": test_text, "uppercase": False}
        response = client.post("/api/tools/md5/encrypt", json=payload)
        data = response.json()
        passed = response.status_code == 200 and "md5_hash" in data
        message = f"哈希值: {data.get('md5_hash')}"
        result.add_test("MD5加密(小写)", passed, message)
        print_test("MD5加密(小写)", passed, message)
    except Exception as e:
        result.add_test("MD5加密(小写)", False, str(e))
        print_test("MD5加密(小写)", False, str(e))
    
    # 测试MD5加密(大写)
    try:
        payload = {"text": test_text, "uppercase": True}
        response = client.post("/api/tools/md5/encrypt", json=payload)
        data = response.json()
        passed = response.status_code == 200 and data.get("md5_hash").isupper()
        message = f"哈希值: {data.get('md5_hash')}"
        result.add_test("MD5加密(大写)", passed, message)
        print_test("MD5加密(大写)", passed, message)
    except Exception as e:
        result.add_test("MD5加密(大写)", False, str(e))
        print_test("MD5加密(大写)", False, str(e))
    
    # 测试MD5校验(匹配)
    try:
        payload = {"text": test_text, "md5_hash": "65a8e27d8879283831b664bd8b7f0ad4"}
        response = client.post("/api/tools/md5/compare", json=payload)
        data = response.json()
        passed = response.status_code == 200 and data.get("match") == True
        message = "哈希匹配验证通过"
        result.add_test("MD5校验(匹配)", passed, message)
        print_test("MD5校验(匹配)", passed, message)
    except Exception as e:
        result.add_test("MD5校验(匹配)", False, str(e))
        print_test("MD5校验(匹配)", False, str(e))
    
    # 测试MD5校验(不匹配)
    try:
        payload = {"text": test_text, "md5_hash": "wrong_hash_value"}
        response = client.post("/api/tools/md5/compare", json=payload)
        data = response.json()
        passed = response.status_code == 200 and data.get("match") == False
        message = "哈希不匹配验证通过"
        result.add_test("MD5校验(不匹配)", passed, message)
        print_test("MD5校验(不匹配)", passed, message)
    except Exception as e:
        result.add_test("MD5校验(不匹配)", False, str(e))
        print_test("MD5校验(不匹配)", False, str(e))


def test_number_to_chinese(result: TestResult):
    """测试数字转中文工具"""
    print_section("数字转中文测试")
    
    # 测试整数转换
    try:
        payload = {"number": 12345}
        response = client.post("/api/tools/number-to-chinese", json=payload)
        data = response.json()
        passed = response.status_code == 200 and "chinese" in data
        message = f"转换结果: {data.get('chinese')}"
        result.add_test("整数转中文", passed, message)
        print_test("整数转中文", passed, message)
    except Exception as e:
        result.add_test("整数转中文", False, str(e))
        print_test("整数转中文", False, str(e))
    
    # 测试小数转换
    try:
        payload = {"number": 123.45}
        response = client.post("/api/tools/number-to-chinese", json=payload)
        data = response.json()
        passed = response.status_code == 200 and "chinese" in data
        message = f"转换结果: {data.get('chinese')}"
        result.add_test("小数转中文", passed, message)
        print_test("小数转中文", passed, message)
    except Exception as e:
        result.add_test("小数转中文", False, str(e))
        print_test("小数转中文", False, str(e))
    
    # 测试零转换
    try:
        payload = {"number": 0}
        response = client.post("/api/tools/number-to-chinese", json=payload)
        data = response.json()
        passed = response.status_code == 200 and "chinese" in data
        message = f"转换结果: {data.get('chinese')}"
        result.add_test("零转中文", passed, message)
        print_test("零转中文", passed, message)
    except Exception as e:
        result.add_test("零转中文", False, str(e))
        print_test("零转中文", False, str(e))


def test_rsa_tools(result: TestResult):
    """测试RSA加密解密工具"""
    print_section("RSA加密解密测试")
    
    public_key = None
    private_key = None
    
    # 测试生成RSA密钥对
    try:
        payload = {"key_size": 2048}
        response = client.post("/api/tools/rsa/generate-keys", json=payload)
        data = response.json()
        passed = response.status_code == 200 and "public_key" in data and "private_key" in data
        if passed:
            public_key = data.get("public_key")
            private_key = data.get("private_key")
        message = "密钥对生成成功"
        result.add_test("生成RSA密钥对(2048)", passed, message)
        print_test("生成RSA密钥对(2048)", passed, message)
    except Exception as e:
        result.add_test("生成RSA密钥对(2048)", False, str(e))
        print_test("生成RSA密钥对(2048)", False, str(e))
    
    # 测试RSA加密
    test_plaintext = "Hello, RSA Encryption!"
    ciphertext = None
    if public_key:
        try:
            payload = {"plaintext": test_plaintext, "public_key": public_key}
            response = client.post("/api/tools/rsa/encrypt", json=payload)
            data = response.json()
            passed = response.status_code == 200 and "ciphertext" in data
            if passed:
                ciphertext = data.get("ciphertext")
            message = "加密成功"
            result.add_test("RSA加密", passed, message)
            print_test("RSA加密", passed, message)
        except Exception as e:
            result.add_test("RSA加密", False, str(e))
            print_test("RSA加密", False, str(e))
    else:
        result.add_test("RSA加密", False, "没有可用的公钥")
        print_test("RSA加密", False, "没有可用的公钥")
    
    # 测试RSA解密
    if private_key and ciphertext:
        try:
            payload = {"ciphertext": ciphertext, "private_key": private_key}
            response = client.post("/api/tools/rsa/decrypt", json=payload)
            data = response.json()
            passed = response.status_code == 200 and data.get("plaintext") == test_plaintext
            message = f"解密结果: {data.get('plaintext')}"
            result.add_test("RSA解密", passed, message)
            print_test("RSA解密", passed, message)
        except Exception as e:
            result.add_test("RSA解密", False, str(e))
            print_test("RSA解密", False, str(e))
    else:
        result.add_test("RSA解密", False, "没有可用的私钥或密文")
        print_test("RSA解密", False, "没有可用的私钥或密文")


def test_timer(result: TestResult):
    """测试计时器工具"""
    print_section("计时器测试")
    
    timer_id = None
    
    # 测试创建计时器
    try:
        payload = {"name": "测试计时器", "duration": 60}
        response = client.post("/api/tools/timer/create", json=payload)
        data = response.json()
        passed = response.status_code == 200 and "id" in data
        if passed:
            timer_id = data.get("id")
        message = f"计时器ID: {timer_id}"
        result.add_test("创建计时器", passed, message)
        print_test("创建计时器", passed, message)
    except Exception as e:
        result.add_test("创建计时器", False, str(e))
        print_test("创建计时器", False, str(e))
    
    # 测试获取计时器状态
    if timer_id:
        try:
            response = client.get(f"/api/tools/timer/{timer_id}/status")
            data = response.json()
            passed = response.status_code == 200 and "status" in data
            message = f"状态: {data.get('status')}"
            result.add_test("获取计时器状态", passed, message)
            print_test("获取计时器状态", passed, message)
        except Exception as e:
            result.add_test("获取计时器状态", False, str(e))
            print_test("获取计时器状态", False, str(e))
    
    # 测试启动计时器
    if timer_id:
        try:
            response = client.post(f"/api/tools/timer/{timer_id}/start")
            data = response.json()
            passed = response.status_code == 200 and data.get("success") == True
            message = "计时器已启动"
            result.add_test("启动计时器", passed, message)
            print_test("启动计时器", passed, message)
        except Exception as e:
            result.add_test("启动计时器", False, str(e))
            print_test("启动计时器", False, str(e))
    
    # 等待1秒后暂停
    time.sleep(1)
    
    # 测试暂停计时器
    if timer_id:
        try:
            response = client.post(f"/api/tools/timer/{timer_id}/pause")
            data = response.json()
            passed = response.status_code == 200 and data.get("success") == True
            message = "计时器已暂停"
            result.add_test("暂停计时器", passed, message)
            print_test("暂停计时器", passed, message)
        except Exception as e:
            result.add_test("暂停计时器", False, str(e))
            print_test("暂停计时器", False, str(e))
    
    # 测试重置计时器
    if timer_id:
        try:
            response = client.post(f"/api/tools/timer/{timer_id}/reset")
            data = response.json()
            passed = response.status_code == 200 and data.get("success") == True
            message = "计时器已重置"
            result.add_test("重置计时器", passed, message)
            print_test("重置计时器", passed, message)
        except Exception as e:
            result.add_test("重置计时器", False, str(e))
            print_test("重置计时器", False, str(e))
    
    # 测试获取活跃计时器列表
    try:
        response = client.get("/api/tools/timer/active")
        data = response.json()
        passed = response.status_code == 200 and isinstance(data, list)
        message = f"活跃计时器数量: {len(data)}"
        result.add_test("获取活跃计时器列表", passed, message)
        print_test("获取活跃计时器列表", passed, message)
    except Exception as e:
        result.add_test("获取活跃计时器列表", False, str(e))
        print_test("获取活跃计时器列表", False, str(e))
    
    # 测试获取历史记录
    try:
        response = client.get("/api/tools/timer/history")
        data = response.json()
        passed = response.status_code == 200 and isinstance(data, list)
        message = f"历史记录数量: {len(data)}"
        result.add_test("获取计时器历史记录", passed, message)
        print_test("获取计时器历史记录", passed, message)
    except Exception as e:
        result.add_test("获取计时器历史记录", False, str(e))
        print_test("获取计时器历史记录", False, str(e))
    
    # 测试删除计时器
    if timer_id:
        try:
            response = client.delete(f"/api/tools/timer/{timer_id}")
            data = response.json()
            passed = response.status_code == 200 and data.get("success") == True
            message = "计时器已删除"
            result.add_test("删除计时器", passed, message)
            print_test("删除计时器", passed, message)
        except Exception as e:
            result.add_test("删除计时器", False, str(e))
            print_test("删除计时器", False, str(e))


def test_weight_convert(result: TestResult):
    """测试重量单位换算"""
    print_section("重量单位换算测试")
    
    # 测试克转千克
    try:
        payload = {"value": 1000, "from_unit": "g", "to_unit": "kg"}
        response = client.post("/api/tools/weight/convert", json=payload)
        data = response.json()
        passed = response.status_code == 200 and data.get("result") == 1.0
        message = f"1000g = {data.get('result')}kg"
        result.add_test("克转千克", passed, message)
        print_test("克转千克", passed, message)
    except Exception as e:
        result.add_test("克转千克", False, str(e))
        print_test("克转千克", False, str(e))
    
    # 测试千克转斤
    try:
        payload = {"value": 1, "from_unit": "kg", "to_unit": "jin"}
        response = client.post("/api/tools/weight/convert", json=payload)
        data = response.json()
        passed = response.status_code == 200 and data.get("result") == 2.0
        message = f"1kg = {data.get('result')}斤"
        result.add_test("千克转斤", passed, message)
        print_test("千克转斤", passed, message)
    except Exception as e:
        result.add_test("千克转斤", False, str(e))
        print_test("千克转斤", False, str(e))
    
    # 测试磅转克
    try:
        payload = {"value": 1, "from_unit": "lb", "to_unit": "g"}
        response = client.post("/api/tools/weight/convert", json=payload)
        data = response.json()
        passed = response.status_code == 200 and abs(data.get("result") - 453.592) < 0.01
        message = f"1lb = {data.get('result')}g"
        result.add_test("磅转克", passed, message)
        print_test("磅转克", passed, message)
    except Exception as e:
        result.add_test("磅转克", False, str(e))
        print_test("磅转克", False, str(e))


def test_time_difference(result: TestResult):
    """测试时间差计算"""
    print_section("时间差计算测试")
    
    # 测试计算时间差
    try:
        payload = {
            "start_time": "2024-01-01 00:00:00",
            "end_time": "2024-01-02 12:30:45",
            "format": "%Y-%m-%d %H:%M:%S"
        }
        response = client.post("/api/tools/time-difference/calculate", json=payload)
        data = response.json()
        passed = response.status_code == 200 and "total_days" in data
        message = f"总天数: {data.get('total_days')}, 总小时: {data.get('total_hours')}"
        result.add_test("计算时间差", passed, message)
        print_test("计算时间差", passed, message)
    except Exception as e:
        result.add_test("计算时间差", False, str(e))
        print_test("计算时间差", False, str(e))
    
    # 测试跨月时间差
    try:
        payload = {
            "start_time": "2024-01-31 00:00:00",
            "end_time": "2024-02-01 00:00:00",
            "format": "%Y-%m-%d %H:%M:%S"
        }
        response = client.post("/api/tools/time-difference/calculate", json=payload)
        data = response.json()
        passed = response.status_code == 200 and data.get("total_days") == 1
        message = f"跨月计算: {data.get('total_days')}天"
        result.add_test("跨月时间差计算", passed, message)
        print_test("跨月时间差计算", passed, message)
    except Exception as e:
        result.add_test("跨月时间差计算", False, str(e))
        print_test("跨月时间差计算", False, str(e))


def test_tools_crud(result: TestResult):
    """测试工具管理CRUD"""
    print_section("工具管理CRUD测试")
    
    tool_id = None
    
    # 测试创建工具
    try:
        payload = {"name": "测试工具", "description": "测试工具描述", "category": "测试"}
        response = client.post("/api/tools", json=payload)
        data = response.json()
        passed = response.status_code == 200 and "id" in data
        if passed:
            tool_id = data.get("id")
        message = f"工具ID: {tool_id}"
        result.add_test("创建工具", passed, message)
        print_test("创建工具", passed, message)
    except Exception as e:
        result.add_test("创建工具", False, str(e))
        print_test("创建工具", False, str(e))
    
    # 测试获取工具列表
    try:
        response = client.get("/api/tools")
        data = response.json()
        passed = response.status_code == 200 and isinstance(data, list)
        message = f"工具数量: {len(data)}"
        result.add_test("获取工具列表", passed, message)
        print_test("获取工具列表", passed, message)
    except Exception as e:
        result.add_test("获取工具列表", False, str(e))
        print_test("获取工具列表", False, str(e))
    
    # 测试获取单个工具
    if tool_id:
        try:
            response = client.get(f"/api/tools/{tool_id}")
            data = response.json()
            passed = response.status_code == 200 and data.get("id") == tool_id
            message = f"工具名称: {data.get('name')}"
            result.add_test("获取单个工具", passed, message)
            print_test("获取单个工具", passed, message)
        except Exception as e:
            result.add_test("获取单个工具", False, str(e))
            print_test("获取单个工具", False, str(e))


def test_calendar(result: TestResult):
    """测试日历工具"""
    print_section("日历工具测试")
    
    # 测试获取今日信息
    try:
        response = client.get("/api/tools/calendar/today")
        data = response.json()
        passed = response.status_code == 200 and "year" in data and "month" in data and "day" in data
        message = f"今日日期: {data.get('year')}-{data.get('month')}-{data.get('day')}"
        result.add_test("获取今日信息", passed, message)
        print_test("获取今日信息", passed, message)
    except Exception as e:
        result.add_test("获取今日信息", False, str(e))
        print_test("获取今日信息", False, str(e))
    
    # 测试获取指定月份日历
    try:
        payload = {"year": 2024, "month": 1}
        response = client.post("/api/tools/calendar/month", json=payload)
        data = response.json()
        passed = response.status_code == 200 and "days" in data and data.get("total_days") == 31
        message = f"2024年1月天数: {data.get('total_days')}"
        result.add_test("获取指定月份日历", passed, message)
        print_test("获取指定月份日历", passed, message)
    except Exception as e:
        result.add_test("获取指定月份日历", False, str(e))
        print_test("获取指定月份日历", False, str(e))
    
    # 测试获取当前月份日历（不传参数）
    try:
        payload = {}
        response = client.post("/api/tools/calendar/month", json=payload)
        data = response.json()
        passed = response.status_code == 200 and "year" in data and "month" in data
        message = f"当前年月: {data.get('year')}-{data.get('month')}"
        result.add_test("获取当前月份日历", passed, message)
        print_test("获取当前月份日历", passed, message)
    except Exception as e:
        result.add_test("获取当前月份日历", False, str(e))
        print_test("获取当前月份日历", False, str(e))


def test_length_convert(result: TestResult):
    """测试长度单位换算"""
    print_section("长度单位换算测试")
    
    # 测试米转千米
    try:
        payload = {"value": 1000, "from_unit": "m", "to_unit": "km"}
        response = client.post("/api/tools/length/convert", json=payload)
        data = response.json()
        passed = response.status_code == 200 and data.get("result") == 1.0
        message = f"1000m = {data.get('result')}km"
        result.add_test("米转千米", passed, message)
        print_test("米转千米", passed, message)
    except Exception as e:
        result.add_test("米转千米", False, str(e))
        print_test("米转千米", False, str(e))
    
    # 测试英尺转米
    try:
        payload = {"value": 1, "from_unit": "ft", "to_unit": "m"}
        response = client.post("/api/tools/length/convert", json=payload)
        data = response.json()
        passed = response.status_code == 200 and abs(data.get("result") - 0.3048) < 0.001
        message = f"1ft = {data.get('result')}m"
        result.add_test("英尺转米", passed, message)
        print_test("英尺转米", passed, message)
    except Exception as e:
        result.add_test("英尺转米", False, str(e))
        print_test("英尺转米", False, str(e))
    
    # 测试市里转米
    try:
        payload = {"value": 1, "from_unit": "li", "to_unit": "m"}
        response = client.post("/api/tools/length/convert", json=payload)
        data = response.json()
        passed = response.status_code == 200 and data.get("result") == 500.0
        message = f"1里 = {data.get('result')}m"
        result.add_test("市里转米", passed, message)
        print_test("市里转米", passed, message)
    except Exception as e:
        result.add_test("市里转米", False, str(e))
        print_test("市里转米", False, str(e))
    
    # 测试无效单位
    try:
        payload = {"value": 1, "from_unit": "invalid", "to_unit": "m"}
        response = client.post("/api/tools/length/convert", json=payload)
        passed = response.status_code == 400
        message = f"状态码: {response.status_code}"
        result.add_test("无效单位处理", passed, message)
        print_test("无效单位处理", passed, message)
    except Exception as e:
        result.add_test("无效单位处理", False, str(e))
        print_test("无效单位处理", False, str(e))


def test_url_tools(result: TestResult):
    """测试URL编码解码工具"""
    print_section("URL编码解码测试")
    
    test_url = "https://example.com/path?name=测试&value=123"
    
    # 测试URL编码
    try:
        payload = {"url": test_url, "safe": "/"}
        response = client.post("/api/tools/url/encode", json=payload)
        data = response.json()
        passed = response.status_code == 200 and "encoded" in data
        message = f"编码结果: {str(data.get('encoded'))[:50]}..."
        result.add_test("URL编码", passed, message)
        print_test("URL编码", passed, message)
    except Exception as e:
        result.add_test("URL编码", False, str(e))
        print_test("URL编码", False, str(e))
    
    # 测试URL解码
    try:
        encoded_url = "https%3A%2F%2Fexample.com%2Fpath%3Fname%3D%E6%B5%8B%E8%AF%95%26value%3D123"
        payload = {"url": encoded_url}
        response = client.post("/api/tools/url/decode", json=payload)
        data = response.json()
        passed = response.status_code == 200 and "decoded" in data
        message = f"解码结果: {str(data.get('decoded'))[:50]}..."
        result.add_test("URL解码", passed, message)
        print_test("URL解码", passed, message)
    except Exception as e:
        result.add_test("URL解码", False, str(e))
        print_test("URL解码", False, str(e))
    
    # 测试空URL处理
    try:
        payload = {"url": ""}
        response = client.post("/api/tools/url/encode", json=payload)
        passed = response.status_code == 400
        message = f"空URL状态码: {response.status_code}"
        result.add_test("空URL处理", passed, message)
        print_test("空URL处理", passed, message)
    except Exception as e:
        result.add_test("空URL处理", False, str(e))
        print_test("空URL处理", False, str(e))


def test_yaml_tools(result: TestResult):
    """测试YAML验证格式化工具"""
    print_section("YAML验证格式化测试")
    
    valid_yaml = """
name: 测试
version: 1.0
features:
  - 功能1
  - 功能2
    """
    
    invalid_yaml = """
name: 测试
version: 1.0
features:
  - 功能1
  - 功能2
: invalid
    """
    
    # 测试验证有效YAML
    try:
        payload = {"yaml_str": valid_yaml}
        response = client.post("/api/tools/yaml/validate", json=payload)
        data = response.json()
        passed = response.status_code == 200 and data.get("valid") == True
        message = "有效YAML验证通过"
        result.add_test("验证有效YAML", passed, message)
        print_test("验证有效YAML", passed, message)
    except Exception as e:
        result.add_test("验证有效YAML", False, str(e))
        print_test("验证有效YAML", False, str(e))
    
    # 测试验证无效YAML
    try:
        payload = {"yaml_str": invalid_yaml}
        response = client.post("/api/tools/yaml/validate", json=payload)
        data = response.json()
        passed = response.status_code == 200 and data.get("valid") == False
        message = "无效YAML验证通过"
        result.add_test("验证无效YAML", passed, message)
        print_test("验证无效YAML", passed, message)
    except Exception as e:
        result.add_test("验证无效YAML", False, str(e))
        print_test("验证无效YAML", False, str(e))
    
    # 测试格式化YAML
    try:
        payload = {"yaml_str": valid_yaml}
        response = client.post("/api/tools/yaml/format", json=payload)
        data = response.json()
        passed = response.status_code == 200 and data.get("valid") == True and "formatted" in data
        message = "YAML格式化成功"
        result.add_test("格式化YAML", passed, message)
        print_test("格式化YAML", passed, message)
    except Exception as e:
        result.add_test("格式化YAML", False, str(e))
        print_test("格式化YAML", False, str(e))
    
    # 测试格式化无效YAML
    try:
        payload = {"yaml_str": invalid_yaml}
        response = client.post("/api/tools/yaml/format", json=payload)
        data = response.json()
        passed = response.status_code == 200 and data.get("valid") == False
        message = "无效YAML格式化处理正确"
        result.add_test("格式化无效YAML", passed, message)
        print_test("格式化无效YAML", passed, message)
    except Exception as e:
        result.add_test("格式化无效YAML", False, str(e))
        print_test("格式化无效YAML", False, str(e))


def main():
    """主函数"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}便携工具平台 API 自动化测试 (集成测试版本){Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"测试方式: FastAPI TestClient")
    print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    result = TestResult()
    
    # 运行所有测试
    test_root_endpoint(result)
    test_health_check(result)
    test_timestamp(result)
    test_json_tools(result)
    test_md5_tools(result)
    test_number_to_chinese(result)
    test_rsa_tools(result)
    test_timer(result)
    test_weight_convert(result)
    test_time_difference(result)
    test_tools_crud(result)
    test_calendar(result)
    test_length_convert(result)
    test_url_tools(result)
    test_yaml_tools(result)
    
    # 打印结果
    result.print_summary()
    
    # 根据测试结果返回退出码
    sys.exit(0 if result.failed == 0 else 1)


if __name__ == "__main__":
    main()
