# coding:utf-8

from handlers.index import IndexHandler,MergeHandler


url = [
    (r'/', IndexHandler),
    (r'^/merge$', MergeHandler),

]