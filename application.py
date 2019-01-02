# coding:utf-8

from url import url
import tornado.web
import os

settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    cookie_secret = "UgNVx8vVQLqZ9bbax+3TgKcKUTQwJ0maj/YTxvI6bHg=",
    debug = False
)

application = tornado.web.Application(handlers=url, **settings)