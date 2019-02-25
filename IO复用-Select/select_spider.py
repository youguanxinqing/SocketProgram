import re
import socket
from urllib import parse
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ


class Spider(object):
    def __init__(self):
        self.data = b""

    def make_request_header(self):
        self.urlHandled = parse.urlparse(self.url)
        httpRequest = "GET {} HTTP/1.1\r\n\r\n".format(self.urlHandled.path)
        return httpRequest

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(False)  # 设置socket为非阻塞
        try:
            self.client.connect((self.urlHandled.netloc, 5000))
        except BlockingIOError:
            pass

        # 回调write，发送数据
        selector.register(self.client.fileno(), EVENT_WRITE, self.write)

    def read(self, key):
        buf = self.client.recv(1024)
        if buf:
            self.data += buf
        else:
            selector.unregister(key.fd)
            if verify_code(self.data.decode("utf-8")) == 200:
                body = remove_headers(self.data.decode("utf-8"))
                print(body)
                self.client.close()
            # 当url全部处理完毕，给loop()设置停止信号
            urls.remove(self.url)
            if not urls:
                global stop
                stop = True

    def write(self, key):
        selector.unregister(key.fd)
        self.client.send(self.request.encode("utf-8"))
        # 回调read()，接收数据
        selector.register(self.client.fileno(), EVENT_READ, self.read)

    def get_html(self, url):
        self.url = url
        self.request = self.make_request_header()
        self.connect()  # 程序不会在此阻塞，会直接往下走


def verify_code(data):
    """获取返回码"""
    code = re.search(r"\d{3}", data)
    if code:
        return int(code.group())


def remove_headers(data):
    """去除请求头"""
    newdata = re.split(r"\r\n\r\n", data)
    if len(newdata) == 2:
        return newdata[-1]


def loop():
    while not stop:
        ready = selector.select()
        for key, mask in ready:
            call_back = key.data
            call_back(key)


if __name__ == "__main__":
    stop = False
    urls = []

    selector = DefaultSelector()
    for page in range(10):
        url = "http://127.0.0.1/mysite/{}/".format(page)
        Spider().get_html(url)
        urls.append(url)

    loop()

