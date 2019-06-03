import requests
from bs4 import BeautifulSoup as bs
import os

def getPartUrlList(url):  #��ȡһ��������ÿһ����URL
 al=bs(requests.get(url).text,'html.parser').select('.rich-content a')
 for i in range(len(al)):
  al[i]=al[i]['href']
 return al

def getIndexUrl(url):   #��ȡһ��������ͼƬURL  ��:http://8comic.se/144429/
 req=requests.get(url)
 #������ҳ��
 indexNum=int(bs(req.text,'html.parser').select('#infotxtb')[0].text.split('/')[1][1:-2])
 #��ҳ����ͼƬ��ַ
 pageImgUrl=bs(req.text,'html.parser').select('img')[1]['src']
 url1=pageImgUrl.split('001.')[0]
 url2=pageImgUrl.split('001.')[1]
 li=[]
 for i in range(10):
  li.append(url1+"%03d"%(i+1)+'.'+url2)
 return li

def downListToLocal(urlList,dir,rootDir='/root/downloads'):   #��URL�б�������� ����˵��:ͼƬ��ַ,������+�ڼ���,����ͳһ����·��(Ĭ��/root/downloads) ͼƬ�ᱻ���ص� ͳһ����·��/������/�ڼ���/�ڼ�ҳ.jpg
 for i in urlList:
  req=requests.get(i)
  if not os.path.exists(rootDir+'/'+dir):
   print('û���ļ���,���ڴ���')
   os.makedirs(rootDir+'/'+dir)
   print('û���ļ���,�����ɹ�')
  with open(rootDir+'/'+dir'/'+i.split('/')[-1],'wb') as file:
   file.write(req.content)
   print('������һҳ')

print('���ڻ�ȡ�ܻ���....')
li=getPartUrlList('http://8comic.se/144428/')
print('OK!!!')
for i in range(len(li)):
 print('�������ص�'+"%03d"%i+'��')
 downListToLocal(getIndexUrl(li[i]),'���Ů��/'+"%3d"%(i+1)+'��')
 print('�������ص�'+"%03d"%i+'��')