# Parrot Sample - 示例项目
* 本项目基于Python Flask开发而成，用来支持接口自动化/流量回放工具的采样、演示、演练
* 目前仅提供非常基本HTTP操作，数据存储在运行内存中，重启服务后会被重置
* 代码粗糙，可不吝吐槽，也欢迎参与共建

## 用户手册
### Step 0: 基础环境准备
* 本项目基于python 2.7.x或3.x，请确保运行本服务的机器上已安装python及pip，推荐版本：3.7.x
* 本项目依赖的module已写入requirements.txt中，可使用`pip install -r requirements.txt`进行安装

### Step 1: 启动应用
* 本项目默认使用8080端口，如有冲突，可自行修改app.py中的`_PORT_`
* 命令行方式启动应用: `python app.py`，如需调试可在app.run中增加`debug=True`的参数
* 如正常启动，屏幕可见"Running on http://0.0.0.0:8080/" 内容输出，WARNING可忽略
* 如未正常启动，请确认Step 0和端口使用情况，再有问题可反馈Issue

### Step 2: 操作应用
* 可通过`ipconfig` 或 `ifconfig` 获取服务器ip，之后拼接成完整的地址，如：10.100.100.10:8080，不建议使用127.0.0.1
* 上述地址可在浏览器窗口直接访问，正常的话会呈现页面功能模块，可点击操作
* 本站点未兼容移动端样式，移动端显示效果不佳
* 如访问异常，请确保Step 1的命令行应用正常运行中，再有问题可反馈Issue

### 目前支持的功能
* 均为http get/post请求，除首页外，接口响应文本均为json格式，其中包含timestamp和随机tag
* 支持随机的接口异常比例、最长和最短随机耗时范围的在线设置

#### 用户的行为
* 注册：POST方法
* 注销：POST方法，header中包含token传参
* 登录：POST方法，会生成token，体现在response header和cookie中
* 登出：POST方法，header中包含token传参，会清除cookie

#### 用户的爱好
* 爱好列表：GET方法，header中包含token传参
* 爱好详情：GET方法，header中包含token传参，传参依赖列表接口获取的name
* 添加爱好：POST方法，header中包含token传参
* 删除爱好：POST方法，header中包含token传参
* 今日推荐：GET方法，传参包含today日期

#### 建议的演示操作
* 登录 => 爱好列表 => 添加爱好 => 爱好列表 => 爱好详情 => 今日推荐 => 登出
* 可在浏览器的开发者工具中查看到相应的接口调用详情，也可以导出HAR文件
