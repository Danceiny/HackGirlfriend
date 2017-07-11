
# Why
线程的生命周期分为 5 个状态:创建、就绪、运行、阻塞和终止。自线程创建到终 止，线程便不断在运行、就绪和阻塞这 3 个状态之间转换直至销毁。而真正占有 CPU 的只有 运行、创建和销毁这 3 个状态。一个线程的运行时间由此可以分为 3 部分:线程的启动时间 (Ts)、线程体的运行时间(Tr)以及线程的销毁时间(Td)。在多线程处理的情境中，如 果线程不能够被重用，就意味着每次创建都需要经过启动、销毁和运行这 3 个过程。这必然 会增加系统的相应时间，降低效率。而线程体的运行时间 Tr 不可控制，在这种情况下要提高 线程运行的效率，线程池便是一个解决方案。

# threadpool Python库
![](http://opkk27k9n.bkt.clouddn.com/17-7-11/69264278.jpg)

```python
import urllib2
import os
import time
import threadpool
def download_file(url):
    print("begin download {}".format(url ))
    urlhandler = urllib2.urlopen(url)
    fname = os.path.basename(url) + ".html"
    with open(fname, "wb") as f:
while True:
chunk = urlhandler.read(1024) if not chunk:
break
            f.write(chunk)
urls = ["http://wiki.python.org/moni/WebProgramming",
       "https://www.createspace.com/3611970",
       "http://wiki.python.org/moin/Documention"]
pool_size = 2
pool = threadpool.ThreadPool(pool_size) # 创建线程池，大小为 2 requests = threadpool.makrRequests(download_file, urls) # 创建工作请求 [pool.putRequest(req) for req in requests]
print("putting request to pool") pool.putRequest(threadpool.WorkRequest(download_file, args=["http://chrisarndt.de/proj ects/threadpool/api/",])) # 将具体的请求放入线程池 pool.putRequest(threadpool.WorkRequest(download_file, args=["https://pypi.python.org/p ypi/threadpool",]))
pool.poll() # 处理任务队列中的新的请求
pool.wait()
print("destory all threads before exist")
pool.dismissWorkers(pool_size, do_join=True) # 完成后退出
```