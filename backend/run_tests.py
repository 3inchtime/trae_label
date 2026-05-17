#!/usr/bin/env python3
"""
测试运行脚本 - 在后台启动服务并运行测试
"""

import subprocess
import time
import sys
import os

def main():
    print("启动后端服务...")
    proc = subprocess.Popen(
        [sys.executable, '-m', 'uvicorn', 'app.main:app', '--port', '8888'],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # 等待服务启动
    time.sleep(3)
    
    try:
        import requests
        
        # 修改 test_api.py 中的端口并运行
        with open('test_api.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace('http://localhost:8000', 'http://localhost:8888')
        
        with open('test_api_temp.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 运行测试
        result = subprocess.run(
            [sys.executable, 'test_api_temp.py'],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        # 清理临时文件
        os.remove('test_api_temp.py')
        
        sys.exit(result.returncode)
        
    finally:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    main()
