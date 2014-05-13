#-*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import os

#求一个列表平均值
def aver(data):
	sum = 0.0
	li = len(data)
	nulls = 0
	for d in range(len(data)):
		if data[d] is not 'Null':
			#print 'not null'
			sum += data[d]
		else :
			#print 'null'
			nulls += 1
	a = sum/(li-nulls)
	#print sum
	#print li
	#print nulls
	#print a
	#print '______________-'
	return a

#去除列表中的重复值
def deldup(ix,iy):
	dx = []
	dy = []
	for i in range(len(ix)):
		if i is not 0:
			if ix[i]==ix[i-1] and iy[i]==iy[i-1] :
				dx.append(ix[i])
				dy.append(iy[i])
	for d in dx:
		ix.remove(d)
	for d in dy:
		iy.remove(d)
	#print ix,len(ix)
	return [ix,iy]

#求一阶差分表
def diff1(ix,iy):
	yt1=[]
	for i in range(len(iy)):
		if i is not 0:
			yt1.append( iy[i] - iy[i-1] )
		else:
			yt1.append('Null')
	return yt1

#求二阶差分表
def diff2(d1):
	yt2 = []
	#return diff 2 list
	for i in range(len(d1)):
		if i ==0 or i==1:
			yt2.append('Null')
		else:
			yt2.append(d1[i]-d1[i-1])
	return yt2
#求三阶差分表
def diff3(d2):
	yt3 = []
	#return diff 2 list
	for i in range(len(d2)):
		if i ==0 or i==1 or i==2 :
			yt3.append('Null')
		else:
			yt3.append(d2[i]-d2[i-1])
	return yt3
#求环比序列一阶差分表
def diffd(dd):
	ydd = []
	#return diff 2 list
	for i in range(len(dd)):
		if i ==0 or i==1 :
			ydd.append('Null')
		else:
			ydd.append(dd[i]-dd[i-1])
	return ydd

#求环比序列
def divi(iy):
	ytd = []
	for i in range(len(iy)):
		if i == 0 :
			ytd.append('Null')
		else:
			ytd.append((iy[i])/(iy[i-1]))
	return ytd

#获得模型名称
def whichmod(d1,d2,d3,dd):
	modname = []
	n = []
	a1 = aver(d1)
	a2 = aver(d2)
	a3 = aver(d3)
	a4 = aver(dd)
	#a5 = aver(ddf)
	for d in range(len(d1)) :
		if d1[d] is not 'Null':
			if a1<0:
				a1 = -a1
			if d1[d]>-a1 and d1[d]<a1:
				n.append('strat')
			else:
				n.append('unkown')
		if d2[d] is not 'Null':
			if a2<0:
				a2 = -a2
			if d2[d]>-a2 and d2[d]<a2:
				n.append('parabola')
			else:
				n.append('unkown')
		if dd[d] is not 'Null':
			if a4<0:
				a4 = -a4
			if dd[d]>-a4 and dd[d]<a4:
				n.append('expon')
			else:
				n.append('unkown')
	un = 0
	ex = 0
	st = 0
	pa = 0
	for i in range(len(n)):
		if n[i] == 'unkown':
			un += 1
		elif n[i] == 'expon':
			ex += 1 
		elif n[i] == 'parabola':
			pa += 1
		elif n[i] == 'strat' :
			st += 1
		pass
	#print un,st,pa,ex
	select_name = 0.3*len(n)
	#print select_name
        #print select_name
        #print un,ex,pa
        #当满足模型的值大于等于该ix数量的x%时，则将该模型放入modname，modname不唯一
        # x值满足: 50%:至多两个 >50%:至多一个 <50%:至多100/x个
        #有可能不满足4种模型中的任意一个,返回空列表[]
	if un>=select_name :
		modname.append('unkown')
	if ex>=select_name:
		modname.append('expon')
	if pa>=select_name:
		modname.append('parabola')
	if st>=select_name:
		modname.append('straght')
	return modname

def summ(lis):
	s = 0
	for l in lis:
		s += l
	return s


def stline(ix,iy,tabname):
	cg_t = 0
	cg_y = 0
	cg_ty = 0
	cg_t2 = 0

	cg_t = summ(ix)
	cg_y = summ(iy)

	ty = []
	for i in range(len(ix)):
		ty.append(ix[i]*iy[i])
	cg_ty = summ(ty)

	t2 = []
	for i in range(len(ix)):
		t2.append(ix[i]*ix[i])
	cg_t2 = summ(t2)

	n = len(ix)
	b = cg_y/n
	c = cg_ty/cg_t2
	#x=np.arange(ix[0],ix[-1],0.1)
	#y = b+c*x
	y = []
	for i in range(len(ix)):
		yi = b+c*ix[i]
		y.append(yi)
	#print tabname
	return y

def parline(ix,iy,tabname):
	cg_t = 0
	cg_y = 0
	cg_t2 = 0
	cg_t4 = 0
	cg_ty = 0
	cg_t2y = 0

	cg_t = summ(ix)
	cg_y = summ(iy)

	t2 = []
	for i in range(len(ix)):
		t2.append(ix[i]*ix[i])
	cg_t2 = summ(t2)

	t4 = []
	for i in range(len(ix)):
		t4.append(ix[i]*ix[i]*ix[i]*ix[i])
	cg_t4 = summ(t4)

	ty = []
	for i in range(len(ix)):
		ty.append(ix[i]*iy[i])
	cg_ty = summ(ty)

	t2y = []
	for i in range(len(ix)):
		t2y.append(ix[i]*ix[i]*iy[i])
	cg_t2y = summ(t2y)

	n=len(ix)

	b1 = cg_ty / cg_t2
	a = cg_t2 / n
	b2 = (cg_t2y - a * cg_y) / (cg_t4 - a * cg_t2)
	b0 = (cg_y - b2 * cg_t2) / n
	#x = np.arange(ix[0],ix[-1],0.1)
	#y = b0 + b1*x + b2*(x**2) 
	#print b0,b1,b2
	#print tabname
	y = []
	for i in range(len(ix)):
		yi = b0 + b1*ix[i] + b2*(ix[i]**2)
		y.append(yi)
	return y

def expon(ix,iy,tabname):
	n = len(ix)
	cg_t = 0
	cg_t2 = 0 
	cg_by = 0
	cg_byt2 = 0
	cg_tby = 0


	cg_t = summ(ix)
	

	t2 = []
	for i in range(len(ix)):
		t2.append(ix[i]*ix[i])
	cg_t2 = summ(t2)

	by = []
	for i in range(len(ix)):
		by.append(np.log10(iy[i]))
	cg_by = summ(by)

	byt2 = []
	for i in range(len(ix)):
		byt2.append(np.log10(iy[i]) * ix[i] * ix[i])
	cg_byt2 = summ(byt2)

	tby = []
	for i in range(len(ix)):
		tby.append(ix[i] * np.log10(iy[i]))
	cg_tby = summ(tby)

	tt = cg_t / n
	yy = cg_by / n

	b = (cg_tby - n*tt*yy)/(cg_t2 - n*(tt*tt))

	ba = yy - b*tt

	a = np.e**ba

	#x = np.arange(ix[0],ix[-1],0.1)
	#x = np.arange(ix[0],ix[-1]+ix[-1]*1,1)
	#print 'a:', a
	#print 'cg_tby',cg_tby
	#print 'yy:',yy
	#print by
	#print iy
	#print 'b:' ,b
	#y = a*np.e**(b*x)
	#print a,b
	print tabname
	y = []
	for i in range(len(ix)):
		yi = a*np.e**(b*ix[i])
		y.append(yi)
	return y

def slope(ix,iy,tabname):
	s = []
	x = []
	for i in xrange(len(ix)):
		if i == 0:
			#s.append(ix[0])
			pass
		else:
			d1 = ix[i]-ix[i-1]
			d2 = iy[i]-iy[i-1]
			d3 = d2/d1
			s.append(d3)
			x.append(ix[i])
	#x = np.arange(ix[1],ix[-1],0.1)
	print tabname
	return [x,s]

def del_heat():
    filelist_1 = os.listdir('/home/mio/Desktop/pow/static/charts/')
    for f1 in filelist_1:
	    filelist_2 = os.listdir('/home/mio/Desktop/pow/static/charts/%s/'%f1)
	    for f2 in filelist_2:
		    filelist_3 = os.listdir('/home/mio/Desktop/pow/static/charts/%s/%s'%(f1,f2))
		    if len(filelist_3) is not 0:
		        os.remove('/home/mio/Desktop/pow/static/charts/%s/%s/%s'%(f1,f2,filelist_3[0]))
		    os.rmdir('/home/mio/Desktop/pow/static/charts/%s/%s'%(f1,f2))
	    os.rmdir('/home/mio/Desktop/pow/static/charts/%s/'%f1)

def del_ew():
    filelist_1 = os.listdir('/home/mio/Desktop/pow/static/ew/')
    for f1 in filelist_1:
	    filelist_2 = os.listdir('/home/mio/Desktop/pow/static/ew/%s/'%f1)
	    for f2 in filelist_2:
		    filelist_3 = os.listdir('/home/mio/Desktop/pow/static/ew/%s/%s'%(f1,f2))
		    if len(filelist_3) is not 0:
		        os.remove('/home/mio/Desktop/pow/static/ew/%s/%s/%s'%(f1,f2,filelist_3[0]))
		    os.rmdir('/home/mio/Desktop/pow/static/ew/%s/%s'%(f1,f2))
	    os.rmdir('/home/mio/Desktop/pow/static/ew/%s/'%f1)