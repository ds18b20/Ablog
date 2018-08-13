# from urllib import parse
# Python3 replace `urlparse` with `urllib.parse`.

# url = "http://www.example.org/default.html;param1;p2;p3?ct=32&op=92&item=98#anchor"
# print(parse.urlparse(url=url))
# # split url
# split_result = parse.urlsplit(url=url)
# print(split_result)
#
# print('*********************************')
# print('scheme: {}'.format(split_result.scheme))
# print('netloc: {}'.format(split_result.netloc))
# print('path: {}'.format(split_result.path))
# print('query: {}'.format(split_result.query))
# print('fragment: {}'.format(split_result.fragment))
# print('*********************************')
#
# # parse query string
# query_string = split_result.query
# print(parse.parse_qs(query_string))
#
# print('/////////////////////////////////')
from urllib import parse
import html
from html import parser
# Python3 replace `HTMLParser` with `html.parser`.

url = "https://www.google.co.jp/search?newwindow=1&source=hp&ei=mApxW4jOFs-k-QbomZXwBw&q=%E7%BC%96%E7%A0%81&oq=&gs_l=psy-ab.1.0.35i39k1l6.0.0.0.14626.3.1.0.0.0.0.0.0..1.0....0...1c..64.psy-ab..2.1.219.6...220.gCjXlx2JHRc"
print(url)
a = parse.urlparse(url).query
print('a:', a)
b = parse.unquote(a)  # 中文字符转换
print('b:', b)

# 这一行可能不需要
html_parser = parser.HTMLParser()  # 对XML转义做反转义，`&amp;`
txt = html.unescape(b)  # 对`%20`做反转义
print('t:', txt)
c = parse.parse_qs(txt, True)
print('c:', c)
