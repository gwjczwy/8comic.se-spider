import requests
from bs4 import BeautifulSoup as bs
import os
from time import sleep

def getPartUrlList(url):  #获取一部漫画的每一话的URL
 al=bs(requests.get(url).text,'html.parser').select('.rich-content a')
 for i in range(len(al)):
  al[i]=al[i]['href']
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

def downListToLocal(urlList,dir,rootDir='/root/downloads'):   #对URL列表进行下载 参数说明:图片网址,漫画名+第几话,下载统一保存路径(默认/root/downloads) 图片会被下载到 统一保存路径/漫 画名/第几话/第几页.jpg
 for i in urlList:
  headers={
  'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.25 (KHTML, like Gecko) Chrome/12.0.706.0 Safari/534.25',
  'Referer':'http://8comic.se/144429/'
  }
  req=requests.get(i,headers=headers)
  sleep(2)
  if not os.path.exists(rootDir+'/'+dir):
   print('没有文件夹,正在创建')
   os.makedirs(rootDir+'/'+dir)
   print('没有文件夹,创建成功')
  with open(rootDir+'/'+dir+'/'+i.split('/')[-1],'wb') as file:
   file.write(req.content)
   print('已下载一页')

print('正在获取总话数....')
li=getPartUrlList('http://8comic.se/144428/')#要修改漫画,在此处修改
print('OK!!!')
for i in range(len(li)):
 print('正在下载第'+"%03d"%i+'话')
 downListToLocal(getIndexUrl(li[i]),'租借女友/'+"%03d"%(i+1)+'话')#要修改漫画保存的文件夹名,修改'租借女友'
 print('正在下载第'+"%03d"%i+'话')