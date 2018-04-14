import pandas as pd
import sys
import pickle

pklfile="/home/tapan/jiradb.pkl"
inputjirafile="/home/tapan/JIRA.xls"


try:
    with open(pklfile, 'rb') as iput:
        l = pickle.load(iput)
except:
    try:
        fl = open(pklfile, 'wb')
        l=pd.read_html(inputjirafile)
        pickle.dump(l, fl)
    except:
        print("unable to open %s in write mode" % (pklfile))
        sys.exit(-1)

df=l[1]
df.columns=df.columns.str.replace('[ \n\']', '')
tdf=df.loc[:5,:]
tdf.to_csv('raw.xls', index=False, encoding='utf8')
colfilter=['Key', 'Summary', 'IssueType', 'Status', 'Priority', 'Created', 'ClosedDate', 'Assignee', 'Reporter', 'Component/s', 'LinkedIssues', 'Resolution']
fdf=df[colfilter]

fdf.sort_values(by=['Component/s', 'Priority', 'Created'], inplace=True)


fdf = fdf.loc[fdf.Key.str.find("ACI") != -1, :]
fdf.to_excel('out.xls', encoding='utf8')
fdf.head()
fdf['Created'] = pd.to_datetime(fdf['Created'])
fdf['ClosedDate'] = pd.to_datetime(fdf['ClosedDate'])
                                            
fdf['createQ']=fdf['Created'].apply(lambda x: "%d(Q%d)"%(x.year, x.quarter))
                                        



rate=fdf[['createQ', 'IssueType']]
rate = pd.crosstab(rate.createQ, rate.IssueType)
rate.to_excel('bugrate.xls', encoding='utf8')



odf=fdf.loc[fdf.Resolution == 'Unresolved' , :]
unresolved=odf
odf=odf[['createQ', 'IssueType']]
orate=pd.crosstab(odf.createQ, odf.IssueType)
orate.to_excel('ounresolvrate.xls', encoding='utf8')


uc=unresolved[['createQ', 'Component/s']]
ucrate=pd.crosstab(uc.createQ, uc['Component/s'])
ucrate=ucrate.reindex_axis(ucrate.sum().sort_values(ascending=[False]).index, axis=1)
ucrate.to_excel('ounresolvedcomponents.xls', encoding='utf8')
print(ucrate)
#print(orate)

ob=fdf.loc[(fdf.Resolution == 'Unresolved') & (fdf.IssueType ==  'Bug'), :]
ob = ob [['createQ', 'Priority']]
obrate=pd.crosstab(ob.createQ, ob.Priority)
obrate.to_excel('obrate.xls', encoding='utf8')

#print(obrate)

oi=fdf.loc[(fdf.Resolution == 'Unresolved') & (fdf.IssueType ==  'Improvement'), :]
oi = oi [['createQ', 'Priority']]
oirate=pd.crosstab(oi.createQ, oi.Priority)
oirate.to_excel('oirate.xls', encoding='utf8')

#print(oirate)


ot=fdf.loc[(fdf.Resolution == 'Unresolved') & ((fdf.IssueType ==  'Task') | (fdf.IssueType ==  'Sub-Task')), :]
ot = ot [['createQ', 'Priority']]
otrate=pd.crosstab(ot.createQ, ot.Priority)
otrate.to_excel('otrate.xls', encoding='utf8')

#print(otrate)

