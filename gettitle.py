# -*- coding: utf-8 -*-
import queue
import re
import threading

import requests

Queue = queue.LifoQueue()
header = {
    'User-Agent': 'baidu.bot',
}


# 获取页面，返回页面信息
def gettitle(domain):

    if ("http://" or  "https://" )in domain:
        url = domain
    else:
        url1 = 'http://' + domain
        url2 = 'https://' + domain
        urls = [url1,url2]

        
    try:
        for url in urls:
            html = requests.get(url=url, headers=header, timeout=20)
            # if html.status_code != 200:
            #     print('\033[1;31;40m' + str(html.status_code) + "\t" +str(url) + '\t'+"请求失败"  +   ' \033[0m')
            #     continue
            charset = re.findall('<meta.*charset=.*?>', html.text)

            if charset.__len__() != 0:
                charset = re.findall('charset=.*"', charset[0])
                # print(charset)
                if charset.__len__() != 0:
                    charset = charset[0].replace('"', '').replace('charset=', '')
                    html.encoding = charset
                    # print(charset)

            title = re.findall('<title>(.+)</title>', html.text)
            print(str(html.status_code) + "\t"+url + "\t"+  'title:' + title[0])
            write_data(url,title[0])


    except:

        print('\033[1;31;40m' + str(url) + '\t'+"请求异常"  +  ' \033[0m')
        # Queue.put(url)



    

def write_data(url: str,title:str):
    with open('output.txt', 'a', encoding='utf8') as f:
        f.write(url + "\t" + title+ '\n')
        f.close()


def init_queue():
    global Queue
    with open('ip_port.txt', 'r+', encoding='utf-8') as file:
        domains = file.readlines()
        for domain in domains:
            Queue.put(domain)
    print("队列初始化完毕")


def run_main():
    global Queue
    while not Queue.empty():
        domain = Queue.get()
        domain = domain.replace('\n','')
        gettitle(domain)

def thread_fun(fun):
    thread_list = []
    for i in range(100):
        t = threading.Thread(target=fun)
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()

if __name__ == '__main__':
    init_queue()
    thread_fun (run_main)
