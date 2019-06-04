import requests
from bs4 import BeautifulSoup as bs
import os
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

def downListToLocal(urlList,dir,rootDir=r'D:\\manga'):   #对URL列表进行下载 参数说明:图片网址,漫画名+第几话,下载统一保存路径(默认/root/downloads) 图片会被下载到 统一保存路径/漫画名/第几话/第几页.jpg
 for i in urlList:
  headers={
   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
   'Accept-Encoding':'gzip, deflate',
   'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,zh-HK;q=0.7,zh-TW;q=0.6',
   'Cache-Control':'max-age=0',
   'Connection':'keep-alive',
   'Cookie':'__cfduid=d0f621cbbccf2b4fa4df06c7a01e39f851559538909',
   'Host':'pic.8comic.se',
   'If-Modified-Since':'Sat, 05 Aug 2017 09:30:04 GMT',
   'If-None-Match':'"5985901c-19d1f"',
   'Upgrade-Insecure-Requests':'1',
   'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
  }
  req=requests.get(i,headers=headers)
  if not os.path.exists(rootDir+'/'+dir):
   print('没有文件夹,正在创建')
   os.makedirs(rootDir+'/'+dir)
   print('没有文件夹,创建成功')
  with open(rootDir+'/'+dir+'/'+i.split('/')[-1],'wb') as file:
   file.write(req.content)
   print('已下载一页')

print('正在获取总话数....')
li=getPartUrlList('http://8comic.se/144428/')
print('OK!!!')
for i in range(len(li)):
 print('正在下载第'+"%03d"%(i+1)+'话')
 downListToLocal(getIndexUrl(li[i]),'租借女友/'+"%03d"%(i+1)+'话')
 print('正在下载第'+"%03d"%(i+1)+'话')