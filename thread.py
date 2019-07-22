import time
import threading
import requests
import queue

exitFlag=False

class hacker(threading.Thread):
    def __init__(self,name,q):
        threading.Thread.__init__(self)
        self.name=name
        self.q=q

    def run(self):
        print('开始线程',self.name)
        download(q)
        print('结束线程',self.name)
    
def scanner(q):
    while not exitFlag:
        if not q.empty():
            threadLock.acquire()
            url=q.get()
            try:
                # req=requests.get(url,timeout=3.05)
                # if req.status_code==200:
                print('is up   :',url)
            except:
                print('is down :',url)
            threadLock.release()
        else:
            time.sleep(0.5)

if __name__ == "__main__":
    print('主线程开始')
    threadLock=threading.Lock()
    q=queue.Queue(10)
    threads=[]
    threadName=['Thread-1','Thread-2','Thread-3']
    tasklist=['https://www.runoob.com','https://www.baidu.com','https://www.google.com',
            'https://www.bilibili.com','https://csdn.com/','https://zhihu.com/',
            'http://github.com/','https://tool.oschina.net','https://daka.whaledu.com:9999',
            'http://www.jarvisoj.com','https://www.jarvue.com','http://index.jarvis.com']

    for i in threadName:
        thread=hacker(i,q)
        thread.start()
        threads.append(thread)

    # threadLock.acquire()
    for i in tasklist:
        q.put(i)
    # threadLock.release()
    while not q.empty():
        time.sleep(0.5)
    exitFlag=True
    print('主线程退出')