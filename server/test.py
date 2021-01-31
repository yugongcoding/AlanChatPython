import sys
import os
"""
在命令行运行的时候 使用python test.py 此时__file__返回的是相对路径,也就是这个文件全名包括后缀
如果是使用绝对路径运行 比如python D://test.py, 此时__file__返回的是绝对路径,也就是这个文件上一层目录的名字
pycharm中的run方法用的应该是python + 绝对路径的方式
"""
sys.path.append(os.path.abspath(__file__))
print('__file__', __file__)
print(__name__)

a = sys.path
print(a)
b = os.path.dirname(__file__)
print(b)
print(os.path.dirname(__file__))
print(os.path.abspath(__file__))

