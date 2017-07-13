# Blueprint
应用模块化的关键。

初始化函数：
```python
Blueprint(self, name, import_name, static_folder=None,
                 static_url_path=None, template_folder=None,
                 url_prefix=None, subdomain=None, url_defaults=None,
                 root_path=None)
```

# endpoint
urlmap的索引（细节不赘述）。一般与url相同。
- [最清楚的一篇](http://blog.csdn.net/bestallen/article/details/52107944)
- [Flask中endpoint的理解](http://www.cnblogs.com/eric-nirnava/p/endpoint.html)

一个很重要的函数，url_for(endpoint,**values)。在蓝图里，渲染模板时引用静态资源，通常用该函数构造路径（而非写死！即便是手动通过上下文判断也存在诸多问题！）。通常这里的endpoint用'static'，不知道为啥就是可以。

当初始化蓝图时, template_folder='templates',static_folder='static'，注册时url_prefix = '/',有：
- root_path = /workspaces/HackGirlfriend/Applications/QQBot
- template_folder = templates
- static_url_path = /static # 实际的static_url_path = '/' + static_url_path
- static_folder = /workspaces/HackGirlfriend/Applications/QQBot/static


在上述蓝图初始化参数情形下，
- url_for('static',filename='') = '/' # 这里的endpoint为static，对应app的static_url_path。
- url_for('QQBot.static',filename='') = '/static/'

# 实战解读
**重点**！！！我的策略
### 需求
>(以~表示项目家目录，例如`/home/ubuntu/web2/HackGirlfriend`)
- 一个flask应用(application/app)有多个应用模块(blueprint)。其中application在`~/Applications/wsgi.py`中“声明”，blueprint在`~/Applications/BLUEPRINT_NAME/BLUEPRINT_FILE.py`中声明，并在wsgi.py中被import并register。
- 静态资源总目录在 `~/static`，下面有`~/static/templates`,`~/static/images`,`~/static/js`,`~/static/css`等。
- 各个blueprint有自己的私有静态资源目录，其私有静态资源目录结构类同application的静态资源目录结构（我的实现里`template_folder`在两处有些许差别），并共享application的静态资源目录。

### 实现
1. 在“声明”applicatio时，设置如下参数：
- `template_folder = os.path.abspath('Applications/static/templates')`
- `tatic_folder = os.path.abspath('Applications/static')`

得到：
- app.root_path = ~
- app.template_folder = ~/Applications/static/templates
- app.static_url_path = /static
- app.static_folder = ~/Applications/static

注册blueprint时，`url_prifix = '/'`.
2.  声明blueprint BLUEPRINT_NAME时，
创建`~/Applications/BLUEPRINT_NAME`的python package（即有`__init__.py`文件），并在该目录创建`BLUEPRINT_NAME.py`,声明blueprint时设置如下参数：
- template_folder = 'templates'
- static_folder='static'
- static_url_path='qqbot/static'    
其中`X_folder`显而易见地指向实际文件系统的`~/Applications/BLUEPRINT_NAME/X`。而设置static_url_path的目的是对外（对浏览器等客户端）暴露本blueprint的static_folder的url路径（浏览器访问的url）。

得到：
- QQBot.root_path = ~/Applications/QQBot
- QQBot.template_folder = templates
- QQBot.static_url_path = qqbot/static
- QQBot.static_folder = ~/Applications/QQBot/static

3. 测试

- 有公用资源`~/Applications/static/js/lazysizes.min.js`，私有资源`~/Applications/QQBot/static/templates/QRCode.html`以及`~/Applications/QQBot/static/images/*.png`。

在`BLUEPRINT_NAME=QQBot`情况下，在`~/Applications/QQBot/QQBot.py`中声明blueprint对象`QQBot`,并通过route装饰器，定义路由`qqbot/one`的视图函数`oneclickstart`。在该函数中：

1. 设置`lazy_js_path = url_for('static',filename='js/lazysizes.min.js')`,构造得到`/static/js/lazysizes.min.js`;设置`static_img = url_for('QQBot.static',filename='images/'+'*.png')`构造得到`static_img = /qqbot/static/images/*.png`。

`。
2. 将lazy_js_path放入模板中：`render_template('QRCode.html',lazy_js_path=lazy_js_path,static_img=static_img)`。其中QRCode.html中通过`<script>`,`<img>`标签引入`{{ lazy_js_path }}`,`{{ static_img }}`。
    
3. 浏览器访问`ip:port/qqbot/one`,检查元素可知，js文件的实际GET路径为`http://ip:port/static/js/lazysizes.min.js`,png图片的实际GET路径为`http://ip:port/qqbot/static/images/*.png`。
均可正常访问。（无论是在`~`路径下`python Applications/wsgi.py`还是在`~/Applicaitons`路径下`python wsgi.py`。这里需要说明的是，如果不使用url_for构造路径，而手动指定，在上述两种情形下有较大偏差，最好不用）

注：上文中所述“声明”意会即可 ~= 类的实例化 or 对象初始化 or 构造对象 etc.

注2：以上值得揣摩的是url_for的endpoint参数，我用到了'static','QQBot.static'两个。分别指向了公有的`~/Applications/static`目录和私有的`~/Applications/QQBot/static`。

注：以上配置，Windows环境，Pycharm-Configuration里不加PYTHONPATH，则会无法加载js,css等公用文件，加了source_roots或者content_roots（任一或全加）就正常。(更正：加这两个path同样无法加载，前面的错误是由于浏览器缓存所致。)不过我不推荐加，命令行才是最纯粹可预知的运行环境，服务器环境下是没有pycharm来做这些自动化工作的。

# Nginx反向代理的新坑
- [Flask的url_for重定向问题和相应源码分析](https://jiayi.space/post/flaskde-url_forzhong-ding-xiang-wen-ti-he-xiang-ying-yuan-ma-fen-xi)

# 有关Flask的一些精品文章
- [在 Flask 里产生流式响应](https://blog.tonyseek.com/post/flask-stream-response/)
- [](https://juejin.im/entry/5821856abf22ec0068e2595a)