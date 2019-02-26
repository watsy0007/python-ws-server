# ws_demo

python 推送测试


## 关键字

python + flask + flask-socketio + redis


## 安装依赖

`pip install -r requirements.txt`

## 运行

`python ws.py`

浏览器打开 `http://127.0.0.1:5000`

打开终端
```shell
redis-cli
> publish chat "hello ws!"
```