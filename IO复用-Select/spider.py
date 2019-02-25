import re
import socket
from urllib import parse


class Spider(object):
    def __init__(self):
        self.data = b""

    def make_request_header(self, url):
        self.urlHandled = parse.urlparse(url)
        httpRequest = "GET {} HTTP/1.1\r\n\r\n".format(self.urlHandled.path)
        return httpRequest

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.urlHandled.netloc, 5000))  # 程序在此阻塞

    def read(self):
        while True:
            buf = self.client.recv(1024)
            if not len(buf):
                break
            self.data += buf
        if verify_code(self.data.decode("utf-8")) == 200:
            body = remove_headers(self.data.decode("utf-8"))
            print(body)
        self.client.close()

    def write(self):
        self.client.send(self.request.encode("utf-8"))

    def get_html(self, url):
        self.request = self.make_request_header(url)
        self.connect()
        self.write()
        self.read()


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


if __name__ == "__main__":

    for page in range(10):
        Spider().get_html("http://127.0.0.1/mysite/{}/".format(page))

