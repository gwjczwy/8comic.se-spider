import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-u',help="指定URL 如 http://8comic.se/144428/ 该漫画的每话都将被下载")
parser.add_argument('-n',help='指定名称 将会下载到 /root/downloads/指定名称')
args=parser.parse_args()

if not args.u or not args.n:
   print("缺少参数")
   print("示例 python args.py -n 租借女友 -u http://8comic.se/144428/")
   exit()


import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import os

def getPartUrlList(url):  #获取一部漫画的每一话的URL
 al=bs(requests.get(url).text,'html.parser').select('.rich-content a')
 try:
  for i in range(len(al)):
   al[i]=al[i]['href']
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
 for i in urlList:
  headers={
  'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.25 (KHTML, like Gecko) Chrome/12.0.706.0 Safari/534.25',
  'Referer':'http://8comic.se/144428/'
  }
  req=requests.get(i,headers=headers)
  sleep(2)
  if not os.path.exists(rootDir+'/'+dir):
   print('没有文件夹,正在创建')
   os.makedirs(rootDir+'/'+dir)
   print('没有文件夹,创建成功')
  with open(rootDir+'/'+dir+'/'+dir.replace('/','')+i.split('/')[-1],'wb') as file:
   file.write(req.content)
   print('已下载一页')

print('正在获取总话数....')
li=getPartUrlList(args.u)
print('OK!!!')
for i in range(len(li)):
 print('正在下载第'+"%03d"%i+'话')
 downListToLocal(getIndexUrl(li[i]),args.n+'/'+"%03d"%(i+1)+'话')
 print('完成下载第'+"%03d"%i+'话')