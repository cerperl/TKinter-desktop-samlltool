import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

1.因为要修改python的模块搜索路径(sys.path),所以导入sys--import行为控制

2.pathlib.Path=用对象方式操作文件路劲的标注库

3.定义一个基本目录，resolve()获得干净路径后，两次parent来回退两级(具体要回退几级用几次parent?)
4.(工程习惯)把项目根目录插到模块搜索路径最前面，提高 import 优先级，为什么是0?--1.优先级最高 2.防止同名第三方包抢占、防止系统库覆盖自己的模块

总结：在直接运行子目录脚本的情况下，手动将项目根目录加入 Python 的模块搜索路径，并设置为最高优先级，从而保证可以正常导入同级的自定义模块（如 api）。

DAY1.(TK+api+多线程+文本呈现)
问题：按钮按下后无响应且变黑色 文本呈现不全
方法：引入threading库来处理多线程，创建后台任务，防止阻塞界面， 并通过after()方法安全更新ui ; get_weahter()返回的是列表，通过"\n".join(list)拼接多行字符串并更新label,并配合justify进行对齐

“背景图片功能因 Tkinter 透明度限制暂未启用，未来可迁移至 Qt 实现