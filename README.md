# 网站新增反爬机制,脚本不可用.

# 8comic.se spider

### 依赖库
```shell
 pip3 install bs4 requests
```

### 帮助

```shell
  -h, --help  show this help message and exit
  -u U        指定URL 如 http://8comic.se/144428/ 该漫画的每话都将被下载
  -n N        指定名称 将会下载到 /root/downloads/指定名称
  -s S        下载指定话,如: -s "3 5 9-13 1" 注:要写在""中间,连续的几话要用 - 符号进行连接
  -new NEW    只下载最新的一话,默认为 n(禁用) .使用 -new y 开启
```

### 例如:
```shell
#下载所有话
python3 8comic.se.new.py -n 租借女友 -u http://8comic.se/144428
#下载最新话
python3 8comic.se.new.py -n 租借女友 -u http://8comic.se/144428 -new y
#下载指定话
python3 8comic.se.new.py -n 租借女友 -u http://8comic.se/144428 -s "3 5 9-13 1"
```
