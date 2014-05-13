#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'mio'

import MySQLdb
import re
import os
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import leastsq
from matplotlib.font_manager import FontProperties
import TrendExp as te

te.del_heat()
te.del_ew()

#中文支持
font = FontProperties(fname=r"/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", size=14)
localtime = time.strftime('%Y%m%d%H', time.localtime())
conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="liurusi321",charset="utf8")
cursor = conn.cursor()
cursor.execute("use POWANA;")
cursor.execute("SHOW TABLES;")

alltab = cursor.fetchall()
#print alltab
rname = []
rname1 = []
for a in range(len(alltab)):
    #print alltab[a][0]
    #获取表中数据

    cursor.execute("SELECT rep_num,last_rep_time,rep_day,title FROM %s;"%alltab[a][0])
    rows = cursor.fetchall()

    iy = []
    ix = []

    nchartsist = 'yes nchartsist' 
    #firstday = 'Null' 
    #判断是否相差一天
    d = 0
    #d相差1天
    fd = 0 
    #fd 相邻两项day差值
    #chaday = time.strftime('%Y%m%d', time.localtime())
    chaday = ''
    #图表标题时间天，为最新的

    ew = 0

    # rows[r][0]:rep_num; rows[r][1]:last_rep_Num; rows[r][2]:rep_day; rows[r][3]:title;
    for r in range(len(rows)):
        #格式化x值，如果相差天数，给x加上24小时，最后x值精确到分钟
        if r is not 0:
        #跳过该title第一项数据
            #print 'r is not 0'
            #print 'lastday is',rows[r-1][2],type(rows[r-1][2])
            #print '_____________________'
            #print rows[r][2]
            if int(rows[r][2])>int(rows[r-1][2]):
                #print rows[r][2]
                #若后一项数据rep_day值大于前一项，说明后一项时间rep_day比前一项新，跟接近现在时间
                fd += d
                #将上一次的差值赋给fd
                nowday = int(rows[r][2])
                lastday = int(rows[r-1][2])
                if rows[r-1][2]=='20140131':
                    lastday = 20140200
                    print 'last time is %s'%rows[r-1][2]
                if rows[r-1][2]=='20140228':
                    lastday = 20140300
                    print 'last time is %s'%rows[r-1][2]
                if rows[r-1][2]=='20140227':
                    lastday = 20140299
                    print 'last time is %s'%rows[r-1][2]
                if rows[r-1][2]=='20140331':
                    lastday = 20140400
                    print 'last time is %s'%rows[r-1][2]
                if rows[r-1][2]=='20140430':
                    lastday = 20140500
                    print 'last time is %s'%rows[r-1][2]
                if rows[r-1][2]=='20140531':
                    lastday = 20140600
                    print 'last time is %s'%rows[r-1][2]
                if rows[r-1][2]=='20140630':
                    lastday = 20140700
                    print 'last time is %s'%rows[r-1][2]
                if rows[r-1][2]=='20140731':
                    lastday = 20140800
                    print 'last time is %s'%rows[r-1][2]
                if rows[r-1][2]=='20140831':
                    lastday = 20140900
                    print 'last time is %s'%rows[r-1][2]
                if rows[r-1][2]=='20140930':
                    lastday = 20141000
                    print 'last time is %s'%rows[r-1][2]
                if rows[r-1][2]=='20141031':
                    lastday = 20141100
                    print 'last time is %s'%rows[r-1][2]
                if rows[r-1][2]=='20141130':
                    lastday = 20141200
                    print 'last time is %s'%rows[r-1][2]
                if rows[r-1][2]=='20141231':
                    lastday = 20150100
                    print 'last time is %s'%rows[r-1][2]
                d = nowday - lastday
                #d = int(rows[r][2]) - int(rows[r-1][2])        
                #print 'day big than last day'
                nchartsist = 'not nchartsist'
                #与前一项不同，将nchartsist字段值设为'not nchartsist'
                u = re.split(r':',rows[r][1])
                x = (fd+d)*24+float(u[0])+float(u[1])/60
                #x = 倍数X相差天数
                y = float(rows[r][0])
                chaday = rows[r][2]
            else:
                if nchartsist == 'not nchartsist':
                    #d = int(rows[r][2]) - int(rows[r-1][2])
                    u = re.split(r':',rows[r][1])
                    x = (fd+d)*24+float(u[0])+float(u[1])/60
                    y = float(rows[r][0])
                    chaday = rows[r][2]
                else :      
                #print 'day is nchartsist day'
                    u = re.split(r':',rows[r][1])
                    x = float(u[0])+float(u[1])/60
                    y = float(rows[r][0])
                    chaday = rows[r][2]
        else :
            u = re.split(r':',rows[r][1])
            x = float(u[0])+float(u[1])/60
            y = float(rows[r][0])
            chaday = rows[r][2]
        iy.append(y)
        ix.append(x)

    '''
    plt.figure(a)
    plt.grid()
    #plt.plot(ix,iy,'ro--')
    plt.ylabel(u"回复数量",fontproperties=font)
    plt.xlabel(u"当前距首次抓取时间%s"%chaday, fontproperties=font)
    plt.title(u"帖子标题：%s"%rows[r][3],fontproperties=font)
    #plt.savefig("/home/mio/Desktop/pow/static/charts/%s/png/%sa.png"%(alltab[a][0],localtime))
    '''




    xy = te.deldup(ix,iy)
    ix = xy[0]
    iy = xy[1]

    d1 = te.diff1(ix,iy)
    #获得一阶差分表
    '''
    d11 = tuple(d1)
    d12 = list(d11)
    d12.remove(d12[0])
    print d1
    if len(d12) is not 0:
        print d12
        print max(d12)
    '''

    
    d2 = te.diff2(d1)
    #二阶差分表
    
    d3 = te.diff3(d2)
    #三阶差分表
    
    dd = te.divi(iy)
    #环
    #ddf = te.diffd(dd)
    #环比序列一阶差分表

    #sl = te.slope(ix,iy,alltab[a][0])
    #print "max sl:",max(sl)


    if len(iy)>5 and len(ix)>5 :
        '''
        if os.path.exists(r"/home/mio/Desktop/pow/static/charts/%s/"%alltab[a][0]):
            filelist = os.listdir(r"/home/mio/Desktop/pow/static/charts/%s/"%alltab[a][0])
            for f in filelist:
                fi = os.listdir(r"/home/mio/Desktop/pow/static/charts/%s/%s/"%(alltab[a][0],f))
                if len(fi) is not 0:
                    os.remove("/home/mio/Desktop/pow/static/charts/%s/%s/%s"%(alltab[a][0],f,fi[0]))
                os.rmdir("/home/mio/Desktop/pow/static/charts/%s/%s/"%(alltab[a][0],f))
            os.rmdir("/home/mio/Desktop/pow/static/charts/%s/"%alltab[a][0])
            os.makedirs("/home/mio/Desktop/pow/static/charts/%s/"%alltab[a][0])
            os.makedirs("/home/mio/Desktop/pow/static/charts/%s/png/"%alltab[a][0])
            os.makedirs("/home/mio/Desktop/pow/static/charts/%s/txt/"%alltab[a][0])

        else:
            os.makedirs("/home/mio/Desktop/pow/static/charts/%s/"%alltab[a][0])
            os.makedirs("/home/mio/Desktop/pow/static/charts/%s/png/"%alltab[a][0])
            os.makedirs("/home/mio/Desktop/pow/static/charts/%s/txt/"%alltab[a][0])
        '''
        os.makedirs("/home/mio/Desktop/pow/static/charts/%s/"%alltab[a][0])
        os.makedirs("/home/mio/Desktop/pow/static/charts/%s/png/"%alltab[a][0])
        os.makedirs("/home/mio/Desktop/pow/static/charts/%s/txt/"%alltab[a][0])

        modname = te.whichmod(d1,d2,d3,dd)
        print modname
        
        print '_________________________________________________'
        plt.figure(100*a)
        plt.grid()
        fig, ((ax0, ax1),(ax2,ax3)) = plt.subplots(nrows=2,ncols=2)
        x2 = np.array(ix)
        y2 = np.array(iy)
        p2 = [1, 1, 1]
        fitfunc = lambda p, x: p[0] + p[1]*x + p[2]*x**2
        errfunc = lambda p, x, y: y - fitfunc(p, x)
        v,success= leastsq(errfunc, p2, args=(x2, y2))

        ax0.plot(ix,iy,'ro')
        ax0.plot(x2,fitfunc(v,x2),'g--')
        ax0.set_title(u"帖子标题：%s"%rows[r][3],fontproperties=font)
        ax0.set_ylabel(u"回复数量",fontproperties=font)
        ax0.set_xlabel(u"当前距首次抓取时间%s"%chaday, fontproperties=font)

        slope = te.slope(ix,iy,alltab[a][0])
        #slope[0]:time list  slope[1]:slope list
        ax1.plot(slope[0],slope[1],'k')
        ax1.set_title(u"斜率变化",fontproperties=font)
        ax1.set_ylabel(u"斜率",fontproperties=font)
        ax1.set_xlabel(u"当前距首次抓取时间%s"%chaday, fontproperties=font)
        #print "slope:",slope

        x1 = []
        y1 = []
        for yy in range(len(d1)) :
            if d1[yy] == 'Null':
                pass
            else:
                x1.append(ix[yy])
                y1.append(d1[yy])
        d1_max_index = y1.index(max(y1))
        d1_max_y = y1[d1_max_index]
        d1_max_x = x1[d1_max_index]
        ax2.plot(x1,y1,'g')
        ax2.set_title(u"一阶差分表",fontproperties=font)
        ax2.set_ylabel(u"一阶差分",fontproperties=font)
        ax2.set_xlabel(u"当前距首次抓取时间%s"%chaday, fontproperties=font)

        ax3.plot(x2,fitfunc(v,x2),'g--')
        ax3.set_title(u"拟合曲线",fontproperties=font)
        ax3.set_ylabel(u"回复数量",fontproperties=font)
        ax3.set_xlabel(u"当前距首次抓取时间%s"%chaday, fontproperties=font)

        plt.subplots_adjust(hspace=0.5,wspace = 0.5)      

        plt.savefig("/home/mio/Desktop/pow/static/charts/%s/png/%s.png"%(alltab[a][0],localtime))


        f = open("/home/mio/Desktop/pow/static/charts/%s/txt/%s.txt"%(alltab[a][0], localtime), "w")
        f.write("在贴吧首页共抓取%s次该帖子 \n"%(len(ix)))
        #f.write("在贴吧首页共抓取%s次该帖子：分别是%s \n"%(len(ix),ix))
        #f.write("得到%s个回复数 \n"%(len(iy)))
        #f.write("得到%s个回复数，分别是%s \n"%(len(iy),iy))
        f.write("首次抓取时间: %s \n"%(str(chaday)))
        f.write("当前分析时间：%s \n"%(localtime))
        f.write("---------------------------------------------------------------\n")
        
        print rows[r][3]
        #print v
        if v[2] > 0 and v[2]<1:
            ew = 1
            f.write("话题:%s\n"%rows[r][3].encode('utf8'))
            f.write("!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!\n")
            f.write("热度值: %s \n"%v[2])
            f.write("热度趋势：一般\n")
            #f.write("热度值越大，该贴话题越热 \n")
            rname.append(rows[r][3])
        elif v[2]>1:
            ew = 2
            #f1 = open("/home/mio/Desktop/pow/static/charts/%s/%s.txt"%(alltab[a][0], ew), "w")
            #f1.close()
            f.write("话题:%s\n"%rows[r][3].encode('utf8'))
            f.write("!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!\n")
            f.write("热度值: %s  >1 \n"%v[2])
            f.write("热度趋势：强劲\n")
            #f.write("热度值越大，该贴话题越热 \n")
            rname1.append(rows[r][3])
        elif v[2] <= 0:
            ew = 0
            f.write("话题:%s\n"%rows[r][3].encode('utf8'))
            f.write("---------------------------------------------------------------\n")
            f.write("热度值: %s  <0 \n "%(v[2]))
            #f.write("热度无明显快速上涨趋势\n")
            #f.write("热度值达到0时，该话题热度有快速上升趋势\n")
            f.write("无明显热度趋势\n")
        s_max_index = slope[1].index(max(slope[1]))
        f.write("斜率在%s达到最大值：%s\n"%(slope[0][s_max_index],slope[1][s_max_index]))
        f.write("一阶差分在%s达到最大值：%s\n"%(d1_max_x,d1_max_y))
        f.close()
        #ax.plot(ix,a1,'k--')
        #ax.plot(ix,a2,'b--')
        #ax.plot(ix,a3,'g--')

        #plt.plot(ix,iy,'ro--')
        #plt.ylabel(u"回复数量",fontproperties=font)
        #plt.xlabel(u"当前距首次抓取时间%s"%chaday, fontproperties=font)
        #plt.title(u"帖子标题：%s"%rows[r][3],fontproperties=font)
        
        #print u"抓取次数大于10,ANA is OK"
        #plt.savefig("/home/mio/Desktop/testANA/charts/%s/%s.png"%(alltab[a][0],localtime))
    

    if ew == 1 or ew == 2:
        '''
        if os.path.exists(r"/home/mio/Desktop/pow/static/ew/%s/"%alltab[a][0]):
            filelist = os.listdir(r"/home/mio/Desktop/pow/static/ew/%s/"%alltab[a][0])
            #print filelist
            for f in filelist:
                fi = os.listdir(r"/home/mio/Desktop/pow/static/ew/%s/%s/"%(alltab[a][0],f))
                if len(fi) is not 0:
                    os.remove("/home/mio/Desktop/pow/static/ew/%s/%s/%s"%(alltab[a][0],f,fi[0]))
                os.rmdir("/home/mio/Desktop/pow/static/ew/%s/%s/"%(alltab[a][0],f))
            os.rmdir("/home/mio/Desktop/pow/static/ew/%s/"%alltab[a][0])
            os.makedirs("/home/mio/Desktop/pow/static/ew/%s/"%alltab[a][0])
            os.makedirs("/home/mio/Desktop/pow/static/ew/%s/png/"%alltab[a][0])
            os.makedirs("/home/mio/Desktop/pow/static/ew/%s/txt/"%alltab[a][0])
        else:
            os.makedirs("/home/mio/Desktop/pow/static/ew/%s/"%alltab[a][0])
            os.makedirs("/home/mio/Desktop/pow/static/ew/%s/png/"%alltab[a][0])
            os.makedirs("/home/mio/Desktop/pow/static/ew/%s/txt/"%alltab[a][0])
            pass
        print "抓取次数>30,is hot "
        '''
        os.makedirs("/home/mio/Desktop/pow/static/ew/%s/"%alltab[a][0])
        os.makedirs("/home/mio/Desktop/pow/static/ew/%s/png/"%alltab[a][0])
        os.makedirs("/home/mio/Desktop/pow/static/ew/%s/txt/"%alltab[a][0])


        #-----------------------------------------------------------------------------------
        x1 = np.array(ix)
        y1 = np.array(iy)

        p0 = [1, 1, 1]
        fitfunc = lambda p, x: p[0] + p[1]*x + p[2]*x**2
        errfunc = lambda p, x, y: y - fitfunc(p, x)
        v,success= leastsq(errfunc, p0, args=(x1, y1))
        #print plsq[0]

        plt.figure(a)
        plt.grid()
        fig, ax = plt.subplots()
        #ax.plot(ix,iy,'ro')
        ax.plot(x1,y1,'ro')
        ax.plot(x1,fitfunc(v,x1),'g--')
        ax.set_title(u"帖子标题：%s"%rows[r][3],fontproperties=font)
        ax.set_ylabel(u"回复数量",fontproperties=font)
        ax.set_xlabel(u"当前距首次抓取时间%s"%chaday, fontproperties=font)

        #---------------------------------------------------------------------------------------------------
        plt.savefig("/home/mio/Desktop/pow/static/ew/%s/png/%s.png"%(alltab[a][0],localtime))

        f = open("/home/mio/Desktop/pow/static/ew/%s/txt/%s.txt"%(alltab[a][0], localtime), "w")
        #f.write("在贴吧首页共抓取%s次该帖子：分别是%s \n"%(len(ix),ix))
        #f.write("得到%s个回复数，分别是%s \n"%(len(iy),iy))
        

        if v[2] > 0 and v[2]<1:
            ew = 1
            #f.write("!-!-!-!-!-!-!-!-!-!-!-!-!-!\n")
            f.write("话题:%s\n"%rows[r][3].encode('utf8'))
            f.write("热度值: %s \n"%v[2])
            f.write("热度趋势：一般")
            #f.write("热度值越大，该贴话题越热 \n")
        elif v[2]>1:
            ew = 2
            #f.write("!*!*!*!*!*!*!*!*!*!*!*!*!*!\n")
            f.write("话题:%s\n"%rows[r][3].encode('utf8'))
            f.write("热度值: %s \n"%v[2])
            f.write("热度趋势：强劲")
            #f.write("热度值越大，该贴话题越热 \n")
        #elif v[2] <= 0:
            #ew = 0
            #f.write("___________________________\n")
            #f.write("话题:%s\n"%rows[r][3].encode('utf8'))
            #f.write("本贴热度值: %s \n"%v[2])
            #f.write("热度无明显快速上涨趋势\n")
            #f.write("热度值达到0时，该话题热度有快速上升趋势\n")
        #f.write("当前分析时间：%s \n"%(localtime))
        f.close()
    else:
        #print u"抓取次数小于10,DO NOT ANA"
        pass


print '============================='
print ">0"
for r in rname:
	print r
print '|||||||||||||||'
print ">1"
for r in rname1:
	print r
