from flask import Flask, request
import socket
import threading
import time
import sys

# --------------------------------------------------
# UDP心跳配置 (必须与sys-mgt-service系统配置一致)
# --------------------------------------------------
UDP_HOST = "127.0.0.1"
UDP_PORT = 53500  # 必须和系统constants.py中的SOCK_PORT一致
HEARTBEAT_INTERVAL = 2  # 心跳间隔(秒)，建议2-5秒

# --------------------------------------------------
# UDP心跳核心实现
# --------------------------------------------------
def _send_heartbeat(label):
    """UDP心跳发送线程函数"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target = (UDP_HOST, UDP_PORT)

    while True:
        try:
            sock.sendto(label.encode("utf-8"), target)
            time.sleep(HEARTBEAT_INTERVAL)
        except Exception as e:
            # 心跳发送失败时的简单处理，继续尝试
            time.sleep(HEARTBEAT_INTERVAL)

def start_heartbeat(label):
    """启动UDP心跳线程"""
    t = threading.Thread(target=_send_heartbeat, args=(label,), daemon=True)
    t.start()
    return t



app = Flask(__name__)

@app.route('/demo/echo', methods=['GET', 'POST'])
def echo():
    if request.method == 'POST':
        data = request.get_json()
        return data
    elif request.method == 'GET':
        data = request.args
        return data

def main():
    app.run(port=8080)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("ERROR: 缺少系统传递的instance_label参数")
        print("系统会自动将label参数传递给服务进程，无需手动设置")
        sys.exit(1)

    instance_label = sys.argv[1]
          # 特殊处理：如果系统传递的是JSON格式的参数，解析出label
    try:
        import json
        params = json.loads(instance_label)
        instance_label = params["label"]
    except:
        # 否则直接使用参数作为label
        pass
    print(f"[Heartbeat] 服务Label: {instance_label}")

    # ------------------------
    # 2. 启动UDP心跳
    # ------------------------
    start_heartbeat(instance_label)
    print(f"[Heartbeat] UDP心跳已启动 (间隔: {HEARTBEAT_INTERVAL}秒, 目标: {UDP_HOST}:{UDP_PORT})")




    main()
