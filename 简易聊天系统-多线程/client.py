import sys
import time
import socket
import threading


def send_data(sock):
    while True:
        words = input(">>")
        if words in ("q!", "Q!"):
            break
        sock.send(words.encode("utf-8"))

def recv_data(sock, addr):
    while True:
        try:
            data = sock.recv(1024)
            # 兼容linux
            if not data:
                raise ConnectionResetError("远程主机强迫关闭了一个现有的连接。")
        except ConnectionAbortedError:
            break

        dataUTF8 = data.decode("utf-8")
        print("\r【时间：{time}】【来自：{ip}】\n【内容：{content}\n{separate}".format(
            time=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
            ip="%s:%d" % addr,
            content=dataUTF8,
            separate="-"*50
        ))
        print(">>", end="")
        sys.stdout.flush()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 连接服务器
client.connect(("127.0.0.1", 8080))

sendthreading = threading.Thread(target=send_data, args=(client, ))
recvthreading = threading.Thread(target=recv_data, args=(client, ("127.0.0.1", 8080)))
recvthreading.setDaemon(True)  # 兼容linux

sendthreading.start()
recvthreading.start()

sendthreading.join()
client.close()
print("【退出聊天室】")
