from flask import Flask

import time

app = Flask(__name__)


@app.route("/mysite/<page>/")
def get_page(page):
    time.sleep(1)  # 休眠1s
    return "<h1>Page: {}</h1>".format(page)


if __name__ == "__main__":
    app.run()
