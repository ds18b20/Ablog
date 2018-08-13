# Python解析url
传入Server的url可以使用Python自带的urllib里的parse来解析。
## 解析query
假设有如下的一个URL字符串：

`http://www.example.org/default.html?ct=32&op=92&item=98#anchor`

下面的代码可以获取url内的参数：
```python
from urllib import parse
# Python3 replace `urlparse` with `urllib.parse`.

url = "http://www.example.org/default.html?ct=32&op=92&item=98#anchor"

# split url
split_result = parse.urlsplit(url=url)
print(split_result)

print('*********************************')
print('scheme: {}'.format(split_result.scheme))
print('netloc: {}'.format(split_result.netloc))
print('path: {}'.format(split_result.path))
print('query: {}'.format(split_result.query))
print('fragment: {}'.format(split_result.fragment))
print('*********************************')

# parse query string
query_string = split_result.query
print(parse.parse_qs(query_string))
```
解释如下：
### split url
- parse.urlsplit方法直接把url拆开成`scheme`，`netloc`，`path`，`query`，`fragment`5个部分。
其中query就是以string形式保存的参数部分。
- fragment（片段）表示Html中的一个位置标记。例如`https://docs.python.org/3/library/urllib.parse.html#url-parsing`直接跳转到页面的`url-parsing`处。
`#fragment`不会影响url查询结果，它只会作用于浏览器，告诉浏览器显示的位置。
### parse query string
parse.parse_qs(query_string)方法解析string格式的query语句，返回一个dict。

打印输出：
```text
SplitResult(scheme='http', netloc='www.example.org', path='/default.html', query='ct=32&op=92&item=98', fragment='anchor')
*********************************
scheme: http
netloc: www.example.org
path: /default.html
query: ct=32&op=92&item=98
fragment: anchor
*********************************
{'ct': ['32'], 'op': ['92'], 'item': ['98']}
```
### parse.urlparse()方法
parse模块下还有一个类似于urlsplit的方法，urlparse。https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlsplit
urlsplit可以大致作为为urlsplit的替代方法。二者唯一的区别就是urlparse会多得到一个params属性。
关于params参见：https://doriantaylor.com/policy/http-url-path-parameter-syntax
https://tools.ietf.org/html/rfc3986#section-3.3

## 解码 unquote/unescape
unquote：字符集转换；

unescape：反转义
```python
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
```

打印输出：
```text
/anaconda3/bin/python3.6 /Users/huangqiying/PycharmProjects/Ablog/urlparse_test.py
https://www.google.co.jp/search?newwindow=1&source=hp&ei=mApxW4jOFs-k-QbomZXwBw&q=%E7%BC%96%E7%A0%81&oq=&gs_l=psy-ab.1.0.35i39k1l6.0.0.0.14626.3.1.0.0.0.0.0.0..1.0....0...1c..64.psy-ab..2.1.219.6...220.gCjXlx2JHRc
a: newwindow=1&source=hp&ei=mApxW4jOFs-k-QbomZXwBw&q=%E7%BC%96%E7%A0%81&oq=&gs_l=psy-ab.1.0.35i39k1l6.0.0.0.14626.3.1.0.0.0.0.0.0..1.0....0...1c..64.psy-ab..2.1.219.6...220.gCjXlx2JHRc
b: newwindow=1&source=hp&ei=mApxW4jOFs-k-QbomZXwBw&q=编码&oq=&gs_l=psy-ab.1.0.35i39k1l6.0.0.0.14626.3.1.0.0.0.0.0.0..1.0....0...1c..64.psy-ab..2.1.219.6...220.gCjXlx2JHRc
t: newwindow=1&source=hp&ei=mApxW4jOFs-k-QbomZXwBw&q=编码&oq=&gs_l=psy-ab.1.0.35i39k1l6.0.0.0.14626.3.1.0.0.0.0.0.0..1.0....0...1c..64.psy-ab..2.1.219.6...220.gCjXlx2JHRc
c: {'newwindow': ['1'], 'source': ['hp'], 'ei': ['mApxW4jOFs-k-QbomZXwBw'], 'q': ['编码'], 'oq': [''], 'gs_l': ['psy-ab.1.0.35i39k1l6.0.0.0.14626.3.1.0.0.0.0.0.0..1.0....0...1c..64.psy-ab..2.1.219.6...220.gCjXlx2JHRc']}
```

# Reference
https://www.cnblogs.com/stemon/p/6602185.html
