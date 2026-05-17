#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import platform
import signal
import argparse
import socket
import json
from typing import Optional, List

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
PID_FILE = os.path.join(PROJECT_ROOT, ".services.pid")

OS = platform.system()
BACKEND_PORT = 8000
FRONTEND_PORT = 5173


class ServiceManager:
    """服务管理器，确保同一时间只有一个后端和一个前端服务运行"""
    
    def __init__(self):
        self.backend_pid: Optional[int] = None
        self.frontend_pid: Optional[int] = None
        self._load_pids()
    
    def _load_pids(self):
        """从PID文件加载已运行的服务PID"""
        if os.path.exists(PID_FILE):
            try:
                with open(PID_FILE, 'r') as f:
                    data = json.load(f)
                    self.backend_pid = data.get('backend')
                    self.frontend_pid = data.get('frontend')
            except:
                pass
    
    def _save_pids(self):
        """保存服务PID到文件"""
        data = {
            'backend': self.backend_pid,
            'frontend': self.frontend_pid
        }
        with open(PID_FILE, 'w') as f:
            json.dump(data, f)
    
    def _clear_pids(self):
        """清除PID文件"""
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
    
    def _is_process_running(self, pid: int) -> bool:
        """检查进程是否在运行"""
        if pid is None:
            return False
        try:
            if OS == "Windows":
                result = subprocess.run(
                    ["tasklist", "/FI", f"PID eq {pid}"],
                    capture_output=True,
                    text=True
                )
                return str(pid) in result.stdout
            else:
                os.kill(pid, 0)
                return True
        except:
            return False
    
    def _kill_process(self, pid: int, force: bool = False):
        """终止进程"""
        try:
            if OS == "Windows":
                if force:
                    subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)
                else:
                    subprocess.run(["taskkill", "/PID", str(pid)], capture_output=True)
            else:
                if force:
                    os.kill(pid, signal.SIGKILL)
                else:
                    os.kill(pid, signal.SIGINT)
        except:
            pass
    
    def _is_port_in_use(self, port: int) -> bool:
        """检查端口是否被占用"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return False
            except OSError:
                return True
    
    def _find_pid_by_port(self, port: int) -> Optional[int]:
        """根据端口查找占用的进程PID"""
        try:
            if OS == "Windows":
                result = subprocess.run(
                    ["netstat", "-ano"],
                    capture_output=True,
                    text=True
                )
                for line in result.stdout.splitlines():
                    if f":{port}" in line and "LISTENING" in line:
                        parts = line.split()
                        return int(parts[-1])
            else:
                result = subprocess.run(
                    ["lsof", "-ti", f":{port}"],
                    capture_output=True,
                    text=True
                )
                if result.stdout.strip():
                    return int(result.stdout.strip().split()[0])
        except:
            pass
        return None
    
    def stop_existing_services(self, stop_backend: bool = True, stop_frontend: bool = True):
        """停止已存在的服务"""
        stopped = False
        
        # 停止已知PID的服务
        if stop_backend and self.backend_pid and self._is_process_running(self.backend_pid):
            print(f"停止已运行的后端服务 (PID: {self.backend_pid})...")
            self._kill_process(self.backend_pid)
            self.backend_pid = None
            stopped = True
        
        if stop_frontend and self.frontend_pid and self._is_process_running(self.frontend_pid):
            print(f"停止已运行的前端服务 (PID: {self.frontend_pid})...")
            self._kill_process(self.frontend_pid)
            self.frontend_pid = None
            stopped = True
        
        # 检查并停止占用端口的进程
        if stop_backend and self._is_port_in_use(BACKEND_PORT):
            pid = self._find_pid_by_port(BACKEND_PORT)
            if pid and pid != self.backend_pid:
                print(f"端口 {BACKEND_PORT} 被占用，停止进程 (PID: {pid})...")
                self._kill_process(pid, force=True)
                stopped = True
        
        if stop_frontend and self._is_port_in_use(FRONTEND_PORT):
            pid = self._find_pid_by_port(FRONTEND_PORT)
            if pid and pid != self.frontend_pid:
                print(f"端口 {FRONTEND_PORT} 被占用，停止进程 (PID: {pid})...")
                self._kill_process(pid, force=True)
                stopped = True
        
        if stopped:
            time.sleep(2)  # 等待端口释放
    
    def register_backend(self, process: subprocess.Popen):
        """注册后端服务"""
        self.backend_pid = process.pid
        self._save_pids()
    
    def register_frontend(self, process: subprocess.Popen):
        """注册前端服务"""
        self.frontend_pid = process.pid
        self._save_pids()
    
    def cleanup(self):
        """清理资源"""
        self._clear_pids()


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


def stop_all_services():
    """停止所有服务"""
    manager = ServiceManager()
    print("停止所有运行中的服务...")
    manager.stop_existing_services()
    manager.cleanup()
    print("所有服务已停止")
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="便携工具平台启动脚本")
    parser.add_argument("--backend-only", action="store_true", help="仅启动后端")
    parser.add_argument("--frontend-only", action="store_true", help="仅启动前端")
    parser.add_argument("--install-only", action="store_true", help="仅安装依赖，不启动服务")
    parser.add_argument("--stop", action="store_true", help="停止所有运行中的服务")
    parser.add_argument("--no-stop-existing", action="store_true", help="不停止已运行的服务（不推荐）")
    args = parser.parse_args()

    # 停止服务模式
    if args.stop:
        stop_all_services()

    print("=" * 60)
    print("便携工具平台 - 启动脚本")
    print("=" * 60)

    python_cmd = check_python()
    check_node()

    venv_dir = install_backend_deps(python_cmd)
    install_frontend_deps()

    if args.install_only:
        print("\n依赖安装完成！")
        sys.exit(0)

    manager = ServiceManager()
    processes: List[subprocess.Popen] = []

    try:
        # 停止已存在的服务
        if not args.no_stop_existing:
            print("检查并清理已运行的服务...")
            manager.stop_existing_services(
                stop_backend=not args.frontend_only,
                stop_frontend=not args.backend_only
            )
            print("清理完成\n")

        if args.backend_only:
            print("启动后端服务...")
            p = start_backend(venv_dir)
            manager.register_backend(p)
            processes.append(p)
        elif args.frontend_only:
            print("启动前端服务...")
            p = start_frontend()
            manager.register_frontend(p)
            processes.append(p)
        else:
            p1 = start_backend(venv_dir)
            manager.register_backend(p1)
            processes.append(p1)
            time.sleep(3)  # 给后端更多启动时间
            p2 = start_frontend()
            manager.register_frontend(p2)
            processes.append(p2)

        print("\n" + "=" * 60)
        print("服务启动成功！")
        print(f"后端 API: http://localhost:{BACKEND_PORT}")
        print(f"API 文档: http://localhost:{BACKEND_PORT}/docs")
        print(f"前端页面: http://localhost:{FRONTEND_PORT}")
        print("=" * 60)
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
            p.wait(timeout=5)
        manager.cleanup()
        print("所有服务已停止")


if __name__ == "__main__":
    main()
