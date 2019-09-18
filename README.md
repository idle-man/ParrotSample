# Sample - 示例项目
* 用来支持接口自动化/流量回放工具的采样、演练、演示
* 本项目使用Python Flask开发而成，仅提供非常基本的功能
* 代码粗糙，可不吝吐槽，也欢迎参与共建

## 用户手册
### Step 0: 基础环境准备
* 本项目基于python 2.7.x或3.x，请确保运行本服务的机器上已安装python及pip，推荐版本：3.7.x
* 本项目依赖的module已写入requirements.txt中，可使用`pip install -r requirements.txt`进行安装

### Step 1: 启动应用
* 本项目默认使用8080端口，如有冲突，可自行修改app.py中的`_port_`
* 命令行方式启动应用: `python app.py`，如需调试可在app.run中增加debug=True的参数
* 如正常启动，屏幕可见"Running on http://0.0.0.0:8080/" 内容输出，WARNING可忽略
* 如未正常启动，请确认Step 0和端口使用情况，再有问题可反馈Issue

### Step 2: 操作应用
* 可通过`ipconfig` 或 `ifconfig` 获取服务器ip，之后拼接成完整的地址，如：10.100.100.10:8080，切勿使用127.0.0.1
* 上述地址可在浏览器窗口直接访问，正常的话会呈现页面功能块，可点击操作
* 如需抓包，可将该地址在手机浏览器或微信窗口打开，记得设置好WiFi代理，确保Fiddler/Charles可抓取到请求
* 如访问异常，请确保Step 1的命令行应用正常运行中，再有问题可反馈Issue

### 目前支持的功能
* 均为http get/post请求，除首页外，接口响应文本均为json格式，其中包含timestamp和随机tag
* 设置了随机的失败比例，可自行修改app.py中的exception_percent，默认为0
* 各接口设置了随机的耗时，区间可自行修改app.py中的duration_max和duration_min

#### 用户行为
* 注册：POST方法
* 注销：POST方法，header中包含token传参
* 登录：POST方法，会生成token，体现在response header和cookie中
* 登出：POST方法，header中包含token传参，会清除token

#### 用户的兴趣
* 兴趣列表：GET方法，header中包含token传参
* 兴趣详情：GET方法，header中包含token传参，传参依赖列表接口获取的name
* 添加兴趣：POST方法，header中包含token传参
* 删除兴趣：POST方法，header中包含token传参
* 今日推荐：GET方法，传参包含today日期
