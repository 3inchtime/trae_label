#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import platform
import signal
import argparse

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

OS = platform.system()


def run_command(cmd, cwd, shell=False):
    if OS == "Windows" and not shell:
        return subprocess.Popen(cmd, cwd=cwd, shell=True)
    return subprocess.Popen(cmd, cwd=cwd, shell=shell)


def check_python():
    try:
        subprocess.run(["python3", "--version"], capture_output=True)
        return "python3"
    except FileNotFoundError:
        try:
            subprocess.run(["python", "--version"], capture_output=True)
            return "python"
        except FileNotFoundError:
            print("错误: 未找到 Python，请先安装 Python 3.8+")
            sys.exit(1)


def check_node():
    try:
        subprocess.run(["node", "--version"], capture_output=True)
        return True
    except FileNotFoundError:
        print("错误: 未找到 Node.js，请先安装 Node.js")
        sys.exit(1)


def install_backend_deps(python_cmd):
    req_file = os.path.join(BACKEND_DIR, "requirements.txt")
    venv_dir = os.path.join(BACKEND_DIR, "venv")
    
    if not os.path.exists(venv_dir):
        print("创建 Python 虚拟环境...")
        subprocess.run([python_cmd, "-m", "venv", "venv"], cwd=BACKEND_DIR, check=True)
    
    if OS == "Windows":
        pip_cmd = os.path.join(venv_dir, "Scripts", "pip")
    else:
        pip_cmd = os.path.join(venv_dir, "bin", "pip")
    
    print("安装后端依赖...")
    subprocess.run([pip_cmd, "install", "-r", req_file], cwd=BACKEND_DIR, check=True)
    return venv_dir


def install_frontend_deps():
    node_modules = os.path.join(FRONTEND_DIR, "node_modules")
    if not os.path.exists(node_modules):
        print("安装前端依赖...")
        subprocess.run(["npm", "install"], cwd=FRONTEND_DIR, check=True)


def start_backend(venv_dir):
    print("启动后端服务 (端口: 8000)...")
    if OS == "Windows":
        python_exe = os.path.join(venv_dir, "Scripts", "python")
    else:
        python_exe = os.path.join(venv_dir, "bin", "python")
    
    cmd = [python_exe, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
    return run_command(cmd, BACKEND_DIR)


def start_frontend():
    print("启动前端服务 (端口: 5173)...")
    cmd = ["npm", "run", "dev"]
    return run_command(cmd, FRONTEND_DIR)


def main():
    parser = argparse.ArgumentParser(description="便携工具平台启动脚本")
    parser.add_argument("--backend-only", action="store_true", help="仅启动后端")
    parser.add_argument("--frontend-only", action="store_true", help="仅启动前端")
    parser.add_argument("--install-only", action="store_true", help="仅安装依赖，不启动服务")
    args = parser.parse_args()

    print("=" * 50)
    print("便携工具平台 - 启动脚本")
    print("=" * 50)

    python_cmd = check_python()
    check_node()

    venv_dir = install_backend_deps(python_cmd)
    install_frontend_deps()

    if args.install_only:
        print("\n依赖安装完成！")
        sys.exit(0)

    processes = []

    try:
        if args.backend_only:
            p = start_backend(venv_dir)
            processes.append(p)
        elif args.frontend_only:
            p = start_frontend()
            processes.append(p)
        else:
            p1 = start_backend(venv_dir)
            processes.append(p1)
            time.sleep(2)
            p2 = start_frontend()
            processes.append(p2)

        print("\n" + "=" * 50)
        print("服务启动成功！")
        print("后端 API: http://localhost:8000")
        print("API 文档: http://localhost:8000/docs")
        print("前端页面: http://localhost:5173")
        print("=" * 50)
        print("\n按 Ctrl+C 停止所有服务\n")

        while True:
            time.sleep(1)
            for p in processes:
                if p.poll() is not None:
                    print(f"服务意外退出，退出码: {p.returncode}")
                    sys.exit(1)

    except KeyboardInterrupt:
        print("\n正在停止所有服务...")
        for p in processes:
            if p.poll() is None:
                if OS == "Windows":
                    p.terminate()
                else:
                    p.send_signal(signal.SIGINT)
        for p in processes:
            p.wait()
        print("所有服务已停止")


if __name__ == "__main__":
    main()
