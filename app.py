# 这是一个完整的Flask服务，包含UDP心跳维持系统status
import socket
import threading
import time
import sys
from flask import Flask

# ------------------------------
# 配置信息
# ------------------------------
FLASK_PORT = 5000
UDP_SERVER = ('127.0.0.1', 53500)
HEARTBEAT_INTERVAL = 2  # 秒


# ------------------------------
# 核心功能：UDP心跳维持系统status
# ------------------------------
def _start_heartbeat(instance_id):
    """启动UDP心跳线程，维持系统中的Running状态"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            sock.sendto(str(instance_id).encode('utf-8'), UDP_SERVER)
            time.sleep(HEARTBEAT_INTERVAL)
        except Exception:
            time.sleep(HEARTBEAT_INTERVAL)  # 发送失败重试


def start_heartbeat(instance_id):
    """将心跳线程设置为daemon，自动随主进程退出"""
    heartbeat_t = threading.Thread(target=_start_heartbeat, args=(instance_id,), daemon=True)
    heartbeat_t.start()
    return heartbeat_t


# ------------------------------
# Flask业务逻辑
# ------------------------------
app = Flask(__name__)


@app.route('/')
def index():
    return "Flask服务运行中，UDP心跳已启动"


@app.route('/api/test')
def api_test():
    return {"message": "Hello from Flask", "status": "ok"}


# ------------------------------
# 启动程序
# ------------------------------
if __name__ == "__main__":
    # -------------
    # 自动获取或设置instance_id
    # -------------
    # 方案1: 从系统参数获取 (系统启动时)
    instance_id = "207"  # 默认值

    if len(sys.argv) > 1:
        try:
            import json

            params = json.loads(sys.argv[1])
            instance_id = params.get("instance_id") or instance_id
            print(f"系统自动传入 Instance ID: {instance_id}")
        except:
            instance_id = sys.argv[1]
            print(f"手动传入 Instance ID: {instance_id}")

    # -------------
    # 启动UDP心跳
    # -------------
    start_heartbeat(instance_id)
    print(f"UDP心跳已启动: 目标={UDP_SERVER}, 间隔={HEARTBEAT_INTERVAL}秒")

    # -------------
    # 启动Flask服务
    # -------------
    print(f"Flask服务启动: http://localhost:{FLASK_PORT}")
    app.run(host='0.0.0.0', port=FLASK_PORT)
