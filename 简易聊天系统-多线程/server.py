import sys
import time
import socket
import threading


def send_data():
    while True:
        words = input(">>")
        clientsock.send(words.encode("utf-8"))

def recv_data(addr):
    global clientsock
    while True:
        try:
            data = clientsock.recv(1024)
            # 兼容linux
            if not data:
                raise ConnectionResetError
        except ConnectionResetError:
            # 用户退出后进入等待模式
            print("\r【用户已退出】")
            print("【等待用户连接】")
            clientsock, addr = server.accept()
            print("【接入用户】")
            print(">>", end="")
            continue

        dataUTF8 = data.decode("utf-8")
        print("\r【时间：{time}】【来自：{ip}】\n【内容：{content}\n{separate}".format(
            time=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()),
            ip="%s:%d" % addr,
            content=dataUTF8,
            separate="-"*50
        ))
        print(">>", end="")
        sys.stdout.flush()  # 强刷管道，不然`>>`可能打印不出来


# 设置socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 设置端口复用
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 绑定ip+端口
server.bind(("0.0.0.0", 8080))
# 设置接听数
server.listen(1)

print("【等待用户连接】")
clientsock, addr = server.accept()
print("【接入用户】")

sendthreading = threading.Thread(target=send_data)
recvthreading = threading.Thread(target=recv_data, args=(addr,))

sendthreading.start()
recvthreading.start()

sendthreading.join()
server.close()
