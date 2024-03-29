import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-u',help="指定URL 如 http://8comic.se/144428/ 该漫画的每话都将被下载")
parser.add_argument('-n',help='指定名称 将会下载到 /root/downloads/指定名称')
parser.add_argument('-s',help='下载指定话,如: -s "3 5 9-13 3" 注:要写在""中间,连续的几话要用 - 符号进行连接',default='')
parser.add_argument('-new',help='只下载最新的一话,默认为 n(禁用) .使用 -new y 开启',default='n')
args=parser.parse_args()

if not args.u or not args.n:
  print("缺少参数")
  print("示例 python args.py -n 租借女友 -u http://8comic.se/144428/")
  exit()

import time
import threading
import queue

class hacker(threading.Thread):
 def __init__(self,name,q):
  threading.Thread.__init__(self)
  self.name=name
  self.q=q

 def run(self):
  print('开始线程',self.name)
  download(q)
  print('结束线程',self.name)

exitFlag=False
q=queue.Queue()
threads=[]
threadNumber=10   #线程数

import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import os

def download(q):#从队列中获取元素并下载
  while not exitFlag:
    headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.25 (KHTML, like Gecko) Chrome/12.0.706.0 Safari/534.25',
    'Referer':'http://8comic.se/'
    }
    if not q.empty():
      arg=q.get()
      i=arg[0]
      absPath=arg[1]
      print('下载',i)
      req=requests.get(i,headers=headers)
      with open(absPath,'wb') as file:
        file.write(req.content)
    else:
      time.sleep(0.5)

def getPartUrlList(url):  #获取一部漫画的每一话的URL
  al=bs(requests.get(url).text,'html.parser').select('td a')
  try:
    for i in range(len(al)):
      al[i]=[al[i].text , al[i]['href']]
  except:
    print('发生错误,请确保传入的url页面包含该漫画的每一话连接.如 http://8comic.se/144428/')
    exit()
  return al

def getIndexUrl(url):   #获取一话中所有图片URL  如:http://8comic.se/144429/
  req=requests.get(url)
  #本话总页数
  indexNum=int(bs(req.text,'html.parser').select('#infotxtb')[0].text.split('/')[1][1:-2])
  #本页漫画图片地址
  pageImgUrl=bs(req.text,'html.parser').select('img')[1]['src']
  url1=pageImgUrl.split('001.')[0]
  url2=pageImgUrl.split('001.')[1]
  li=[]
  for i in range(indexNum):
    li.append(url1+"%03d"%(i+1)+'.'+url2)
  return li

def downListToLocal(urlList,dir,rootDir='/root/downloads'):   #对URL列表进行下载,下载一整话 参数说明:图片网址,漫画名+第几话,下载统一保存路径(默认/root/downloads) 图片会被下载到 统一保存路径/漫画名/第几话/漫画名第几话第几页.jpg
  if not os.path.exists(rootDir+'/'+dir):
    print('创建文件夹: ',rootDir+'/'+dir)
    os.makedirs(rootDir+'/'+dir)
  for i in urlList:
    #文件绝对路径 如: path='/root/download/租借女友/001话/租借女友001话001.jpg'
    absPath=rootDir+'/'+dir+'/'+dir.replace('/','')+i.split('/')[-1]
    if os.path.exists(absPath) and os.path.getsize(absPath) > 10240: #如果文件存在并大于10k则认为重复任务,跳过下载
      print('文件已存在',i)
    else:
      q.put([i,absPath])

def downAllOfManga(): # 下载全部
  print('正在获取总话数....')
  li=getPartUrlList(args.u)
  print('OK!!!')
  for i in range(len(li)):
    print('正在添加第'+"%03d"%i+'话至队列')
    downListToLocal(getIndexUrl(li[i][1]),args.n+'/'+"%03d"%(i+1)+li[i][0])

def downLastOfManga(): # 下载最新话
  print('正在获取最后一话....')
  li=getPartUrlList(args.u)[-1]
  downListToLocal(getIndexUrl(li[1]),args.n+li[0]+'_最新话')

def downSelectOfManga(selected): # 下载选择话
  print('正在获取指定章节....')
  li=getPartUrlList(args.u)
  # 由于下表是从零开始的,selected中的所有值减一
  selected=[i-1 for i in selected]
  for i in selected:
    print('正在添加第'+"%03d"%i+'话至队列')
    downListToLocal(getIndexUrl(li[i][1]),args.n+'/'+"%03d"%(i+1)+li[i][0])

if args.new=='y':
  downLastOfManga()
  print('最新话已添加至队列') 
elif args.s!='':
  # 这段代码将例如: -s "1 3-5 7 9 12-15"
  # 这样的参数处理成
  # [1,3,4,5,7,9,12,13,14,15]
  # 的列表
  selected=[]
  select=args.s.split(' ')
  for i in select:
    j=i.split('-')
    if len(j)==2:
      for k in range(int(j[0]),int(j[1])+1):
        selected.append(k)
    else:
      selected.append(int(j[0]))
  # 处理完成,selected就是处理后的值
  downSelectOfManga(selected)
  print('指定话已添加至队列')
else:
  downAllOfManga()
  print('全部添加完成')


for i in range(threadNumber):
    thread=hacker('thread'+str(i),q)
    thread.start()
    threads.append(thread)

while not q.empty():
 time.sleep(0.5)
exitFlag=True
print('主线程退出')