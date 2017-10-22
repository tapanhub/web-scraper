import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import datetime

def getaddedremoved(dfs):
	lastkey=list(dfs.keys())[-1]
	seclast=list(dfs.keys())[-2]
	closedpd=[]
	for i in dfs[seclast].Key:
		if i not in list(dfs[lastkey].Key):
			closedpd.append(i)
		
	newpd=[]
	for i in dfs[lastkey].Key:
		if i not in list(dfs[seclast].Key):
			newpd.append(i)

	l=dfs[lastkey].set_index("Key")
	s=dfs[seclast].set_index("Key")
	n=l.loc[newpd]
	n.head()
	n.to_csv('%s_new.csv' % (lastkey))
	c=s.loc[closedpd]
	c.to_csv('%s_closed.csv' % (seclast))

def getduedatecsv(dfs):
	for key in dfs.keys():
		df=dfs[key]
		print (key)
		component=df['Component/s']

		df['Due Date'] = df['Due Date'].fillna('10/30/2017')
		dd=pd.to_datetime(df['Due Date'], format='%m/%d/%Y' )

		a=pd.crosstab(component, dd, margins=True)
		a.to_csv('%s_duedates.csv' % (key))
		overdue=df[dd <= pd.to_datetime(datetime.datetime.now().strftime ("%m/%d/%Y"))]
		overdue.to_csv('%s_overdue.csv' % (key))

def plotprogress(fl, values):
	n_groups = 10
	sns.set()
	fig, ax = plt.subplots()

	rects={}

	index = np.arange(n_groups)
	bar_width = 0.12

	i=0
	for key in values.keys():
		rect = plt.bar(index + i*bar_width, values[key], bar_width, label=key.replace('_', ' '), alpha= 0.7)
		rects[key]=rect
		i=i+1

	plt.xlabel('Teams')
	plt.ylabel('Number of Issues')
	plt.title(' 7.3.1 Open P1/P2 Issues')
	plt.xticks(index + bar_width, fl)
	plt.legend()

	for key in rects.keys():
		for rect in rects[key]:
	    		height = rect.get_height()
	    		ax.text(rect.get_x() + rect.get_width()/float(len(rects)), 0.99*height,
			    '%d' % int(height) , ha='center', va='bottom')
		print (len(rects))
		    
	plt.tight_layout()
	plt.show()



filelist= [
'_731_4th_oct.csv',
'_731_6th_oct.csv',
'_731_8th_oct.csv',
'_731_10th_oct.csv',
'_731_12th_oct.csv',
'_731_15th_oct.csv',
'_731_17th_oct.csv'
]


dfs={}
components={}
value_counts={}
fl=[]
values={}

for f in filelist:
	name=f.split('/')[-1].split('.')[0].split('731_')[-1]
	try:
		df = pd.read_csv(f, encoding='ISO-8859-1')
		df = df.drop(df[df['Component/s'] != df['Component/s']].index)
		dfs[name]=df
		c=df['Component/s'].values
		c = [ line.strip() for line in c]
		components[name]=c
		value_counts[name]=pd.Series(c).value_counts(dropna=False)
		if name == '4th_oct':
			value_counts[name]['_PLT_'] = 0
			fl = value_counts[name].index
			fl=list(map(lambda x: x.split('_')[-1], fl))
	
	except OSError:
		print('cannot open', f)


fourvc = value_counts['4th_oct']
for key in value_counts.keys():
	values[key]=[]
	for i, s in fourvc.iteritems():
		if i not in value_counts[key].index:
    			values[key].append(0)
		else:
    			values[key].append(value_counts[key][i])

for key in values.keys():
	print ( "%s = %s"% (key, values[key]))

plotprogress(fl, values)
getduedatecsv(dfs)
getaddedremoved(dfs)
