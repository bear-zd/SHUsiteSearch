from AlphaList import alphalist,numlist
import requests
import sys
import importlib
from threading import Thread  # 导入线程函数
importlib.reload(sys)



def main():
    SavePath='site.txt' #保存路径
    global file,Basesite #file和网站作为全局变量供多线程访问
    file=open(SavePath,'w+')
    Basesite='shu.edu.cn' #原网站
    keywordnum=2 #关键词数量
    Treadnum=128 #线程数量
    Keywordlist = KeywordCreate(keywordnum) #创建关键词序列
    MutiThread(Treadnum,Keywordlist) #多线程
    file.close() #文件保存并关闭
    #由于关键词数量为a~z，A~Z，组成的组合，因而会随着数量显著递增，所以在CPU数量较少的情况下可能会消耗大量的时间

def MutiThread(Treadnum,Keywordlist): #多线程函数
    createVar = locals()
    listTemp = range(0,Treadnum)
    ThreadList = []
    for i, s in enumerate(listTemp):
        createVar['t' + str(i)] = s #动态生成变量
    Slice=len(Keywordlist)/Treadnum #序列切片
    print(Slice)
    for i in range(0,Treadnum):
        createVar['t'+str(i)]=Thread(target=SiteSearch, args=(Basesite,Keywordlist[int((i)*Slice):int((i+1)*Slice)])) #为动态变量赋线程
        #创建线程变量
        print('t'+str(i)+'线程创建完成')
    for i in range(0,Treadnum):
        createVar['t'+str(i)].start()
        print('t' + str(i) + '线程启动完成')
    for i in range(0, Treadnum):
        createVar['t' + str(i)].join()
        print('t' + str(i) + '线程运行结束')
    print("Finished!")


def SiteSearch(Basesite,Keywordlist): #网站访问
    try:
        Keywordlist.remove('')
    except ValueError:
        pass
    for i in Keywordlist:
        tempsite='https://'+i+'.'+Basesite
        try:
            Request=requests.get(tempsite)
        except requests.exceptions.ConnectionError:
            continue
        if(Request.status_code==200):
            file.write(tempsite+'\n')
    return 0



def KeywordCreate(Keywordnum,Includenum=False): #关键词组合
    if Keywordnum==0:
        return []
    else:
        if Includenum==True:
            Keywordlist=alphalist+numlist+['']
        else:
            Keywordlist=alphalist+['']
        klist = Keywordlist
        temp=[]
        for i in range(Keywordnum-1):
            for j in range(len(Keywordlist)):
                for k in (klist):
                    temp.append(Keywordlist[j]+k)
                Keywordlist=Keywordlist+temp
                temp=[]
    print(Keywordlist)
    return Keywordlist






if __name__=='__main__':
    main()
