# -*- coding: utf-8 -*-

from Tkinter import *   #Tkinter 是一个GUI图形接口，在本程序中显示窗口
from ScrolledText import ScrolledText #Tkinter的ScrolledText 文本框滚动条组件
import requests, re, threading  

#request与HTTP相关，在本程序中起到获取豆瓣网页内容的作用
#re是正则表达式模块
#threading是操作多线程的模块


def reptile(ID):
    varl.set('正在获取第%d页内容' % (ID / 25 + 1))
    html = 'https://movie.douban.com/top250?start=' + str(ID)
    response = requests.get(html).text #利用requset获取对应网页中的内容

    # response = unicode(response, 'GBK').encode('UTF-8')

    response = response.encode('utf-8 ')   #解码
    # print  response
    # reg = r'<span class="title">(.*?)</span>.*?"v:average">(.*?)</span>'
    regTitle = r'<span class="title">(.[^&]*?)</span>' #含有电影名称的正则表达式
    regStars = r'.*?"v:average">(.*?)</span>'          #含有评分的正则表达式
    reg_Scorenumber= r'<span>([1-9]\d*)人评价</span>'
    reg_year = r'([1-9]\d*)&nbsp;/&nbsp;'
    reg_country = r'&nbsp;/&nbsp;(.*?)&nbsp;/&nbsp;'

    regTitle = re.compile(regTitle) #把正则表达式编译成一个正则表达式对象
    regStars = re.compile(regStars)
    reg_Scorenumber = re.compile(reg_Scorenumber)
    reg_year = re.compile(reg_year)
    reg_country = re.compile(reg_country)

    titles = re.findall(regTitle, response) #查找所有包含title正则表达式的单词
    stars = re.findall(regStars, response)
    Scorenumber = re.findall(reg_Scorenumber, response)
    year = re.findall(reg_year, response)
    country = re.findall(reg_country, response)
    
    info = list(zip(titles, stars, Scorenumber, year, country)) #调用zip()函数,使得title和stars一一对应。并用list()转换为列表
    #print(info)
    return info




def write():
    varl.set('开始爬取内容') #标签文字
    ID = 0
    nums = 1
    while ID < 250:
        res = reptile(ID)   #一次爬一页25部电影
        ID += 25
        for each in res:
            text.insert(END, 'No.%d\t%s\t%s分\t%s人评价\t%s\t%s\n' 
            % (nums, each[0], each[1], each[2], each[3], each[4]))  #在文本框中输入抓取结果
            nums += 1
    varl.set('获取内容成功')


def start():
    t1 = threading.Thread(target=write)  #创建线程  并调用write函数
    t1.start()
    #write();  #如果不创建线程直接调用write函数，图形界面就会呈现卡住一段时间，因为唯一的主线程被占用了；而如果创建了一个新的线程就不会。


def save():
    content = text.get("0.0", "end").encode('GBK') 
    textfile = open(u'douban250.txt', 'w') #豆瓣电影排行250.txt
    textfile.write(content)
    varl.set('保存内容成功')
    textfile.close()


##########-以下代码创建GUI窗口-##########

root = Tk()    #创建一个顶层窗口，或者叫根窗口

root.title('豆瓣电影top250') #窗口名
root.geometry('820x500+400+200') #窗口尺寸

text = ScrolledText(root, font=('楷体', 15), width=80, height=20)  #加入滚动条
text.grid()

frame = Frame(root)
frame.grid()

####################


# 启动爬虫功能  设置启动按钮
startButton = Button(frame, text='开始', font=('宋体', 18), command=start)   #调用start函数
startButton.grid()
startButton.pack(side=LEFT)

# 保存爬取信息
saveButton = Button(frame, text='保存文件', font=('楷体', 18), command=save)
saveButton.grid()
saveButton.pack(side=LEFT)
# 退出程序
exitButton = Button(frame, text='退出', font=('楷体', 18), command=frame.quit)
exitButton.grid()
exitButton.pack(side=LEFT)

varl = StringVar()  #Tkinter中一些组件(Button, Label等) 如果设置一个textvariable属性为一个StringVar(IntVar, DoubleVar)对象。 
#当这个对象的值被重新设置的时候，组件上的显示文字就会自动变成新的值。

info_label = Label(root, fg='blue', textvariable=varl) #三个按钮下面的标签
info_label.grid()

varl.set('准备中....')

root.mainloop() #mainloop就进入到事件(消息)循环
