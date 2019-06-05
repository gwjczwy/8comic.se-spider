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
```
 
### 例如:
```shell
python3 8comic.se.new.py -n 租借女友 -u http://8comic.se/144428
```

**由于网站限制爬虫,每爬取一张需要等待两秒**