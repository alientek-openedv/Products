# -*- coding: utf-8 -*-
# 作者正点原子保留所有权，如有bug请反馈
# 本脚本用来处理html文件的相关信息，如删除多余的html文件
# 修改html文件能链接到Github上面
# 文档当中的第三方链接通过弹新窗口打开
# 

import os
import io
import re
import sys
import shutil
import subprocess
import bs4

from bs4 import BeautifulSoup
import codecs
from lxml import etree

#导进解析html文件
import lxml.html

from xml.etree import ElementTree
import xml.etree.ElementTree as ET 




#目录所在的文件夹
examples = []


git_hub_url = ["https://github.com/alientek-openedv/Products/tree/master/zdyz_docs/"]

git_hub_nam = [r' Edit on Zdyz/Products']


#排除在外的文件夹
examples_except = ["build"]


sys.path.append(os.path.abspath('_ext'))
sys.path.append(os.path.abspath('_templates'))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')


#获取当前工作目录路径
py_curdir = os.getcwd() 


print("py_curdir = " + py_curdir)






#整个根目录除build文件夹以外
def getallfilesofwalk_del(dir):
    
    #不是目录不需要递归了   
    if not os.path.isdir(dir):
   
        if os.path.splitext(dir)[1]=='.html' or os.path.splitext(dir)[1]=='.HTML':         
            print (dir)
            print("\r\n")   
            os.remove(dir)


        return   

    dirlist = os.listdir(dir)
    for dirret in dirlist:
        if dirret in examples_except[0]:
           continue

        fullname = dir + "\\" + dirret
        if os.path.isdir(fullname):

            #递归
            getallfilesofwalk_del(fullname)
        else:


            if os.path.splitext(fullname)[1]=='.html' or os.path.splitext(fullname)[1]=='.HTML':         
                print  (fullname)
                print("\r\n")                                
                os.remove(fullname) 





#build/html文件夹
def getallfilesofwalk_git_url(dir):
    
    #不是目录不需要递归了   
    if not os.path.isdir(dir):

           
        if os.path.splitext(dir)[1]=='.html' or os.path.splitext(dir)[1]=='.HTML':  

           #通过已有html文件来创建对象
           soup = BeautifulSoup(open(dir))
           print (dir) 
           print('\r\n')

           #查找所有的链接标签
           tags = soup.findAll('a')

           #打印输出标签a  
           print(tags[0].name)


           
        return   

    dirlist = os.listdir(dir)
    for dirret in dirlist:

        fullname = dir + "\\" + dirret
        if os.path.isdir(fullname):

            #递归
            getallfilesofwalk_git_url(fullname)


        else:


            if os.path.splitext(fullname)[1]=='.html' or os.path.splitext(fullname)[1]=='.HTML': 

               print  (fullname)
               print("\r\n") 

               with open(fullname,"r",encoding="utf-8") as file:

                   fcontent = file.read()               

                   #通过已有html文件来创建对象
                   soup = BeautifulSoup(fcontent, 'lxml')

                   tags = soup.findAll('a', text = re.compile(r"\s+View page source"))


                   #查找所有的链接标签
                   tags = soup.findAll('a', text = re.compile(r"\s+View page source"))

                   for li in tags: 

                      print(li)

                      del li['rel']

                      li.string =  git_hub_nam[0]



                      print(li) 

                      rst_relpath = os.path.relpath(fullname, py_curdir+"\\"+examples_except[0]+"\\"+'html') 


                      #文件是.rst后缀
                      li['href'] = git_hub_url[0] + os.path.splitext(rst_relpath)[0] + ".rst"    

                      li['class']="fa fa-github"          

                      #打印输出后的标签
                      print(li)

                   #查找所有的链接标签
                   tags = soup.findAll('a', attrs={"href":re.compile(r"\s?https?:")});

                   for li in tags: 

                      li['target']="_blank"

                      #打印输出后的标签
                      print(li)


                   #查找所有的链接标签
                   tags = soup.findAll('a', attrs={"href":re.compile(r"\s?www:")});

                   for li in tags: 

                      li['target']="_blank"

                      #打印输出后的标签
                      print("target add" + li)




                   #写回原文件
                   with open(fullname,"w",encoding="utf-8") as f_write:

                       f_write.writelines(soup.prettify()) 




                   #print(soup.prettify())


               

                     









# #判断需要建立总共有多少个外设
# for path, dirs, files in os.walk(py_curdir + '/' + examples_except + '/' + 'html'):
#     for dir in dirs: 
#         example.append(dir)  



#     files = os.listdir(AMETALROOT_DIR + 'ametal/examples/' + ametal_config.BUILD_DEMO_BORD + '/' + i)
   
#     for file in files:
#         if os.path.splitext(file)[1]=='.c':         
#             demo.append(os.path.splitext(file)[0]) 
#             #os.mkdir(PRJ_ROOT + 'examples_' + i + '/' + os.path.splitext(file)[0])
           
#             #如果预先创建最后一级相同的路径，将导致拷贝错误
#             shutil.copytree(TEMPLATE_PRJ_ROOT, PRJ_ROOT + 'examples_' + i + '/' + os.path.splitext(file)[0], True)
            
#             #在源文件中加入demo例程入口参数
#             with open(PRJ_ROOT + 'examples_' + i + '/' + os.path.splitext(file)[0] + '/user_code/main.c', 'r') as f_read:
#                 #在内存中修改文件的内容，PRJ_ROOT + 'examples_' + i + '/' + os.path.splitext(file)[0] + '/user_code/main.c'是源文件的路径
#                 str = f_read.readlines()
#                 str.insert(41, '    ' + os.path.splitext(file)[0] + '_entry();')
#             with open(PRJ_ROOT + 'examples_' + i + '/' + os.path.splitext(file)[0] + '/user_code/main.c', 'w') as f_write:
#                 f_write.writelines(str) 
                
#             #修改工程属性
#             change_demo_prj_xml(PRJ_ROOT + 'examples_' + i + '/' + os.path.splitext(file)[0], os.path.splitext(file)[0])
           
# for i in demo:
#     print i






# #以下为正则替换html文件的内容
# with open('1.html', 'r') as r:
#     txt = ''.join(r.readlines())

# print(txt)  # 你原始的html文本

# def replace(match):
#     t, s = match.group(1), match.group(1).strip()
#     return '>%s<' % (t.replace(s, str(len(s))) if s else t)


# txt1 = re.sub(r'>([.\S\s]*?)<', replace, txt)

# print(txt1)  # 转换后的html

if __name__ == "__main__":


    getallfilesofwalk_del(py_curdir)

    print(py_curdir+"\\"+examples_except[0]+"\\"+'html')

    getallfilesofwalk_git_url(py_curdir+"\\"+examples_except[0]+"\\"+'html')







