# -*- coding: utf-8 -*-

import os.path
import os
import xlwt
 
f=open('douban250.txt','r+')

#f.write('xxx')

wb = xlwt.Workbook() # 新增一个表单
sh = wb.add_sheet('A Test Sheet')
# 按位置添加数据

i = 0
for line in f.readlines():
    j = 0
    for item in line.split('\t'):
        try:
            item=item.strip().decode('gbk')
        except UnicodeDecodeError:
            print i,j,item
            sh.write(i,j,"NULL")
        else:
            sh.write(i,j,item)
        j=j+1
    i=i+1

f.close()


# 保存文件
wb.save('example1.xls')
