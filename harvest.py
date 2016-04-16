from filtertree import filterTree
from gendata import genData
from leaves import leaves
from loaddata import loadData
from algor import algor1,algor2
import multiprocessing as mp
def fun(Data):
    rela,t,lv,N = Data
    data=loadData('dataset/'+rela+'/'+rela+'-10dobscv-'+str(t)+'tra.dat')
    tdata=loadData('dataset/'+rela+'/'+rela+'-10dobscv-'+str(t)+'tst.dat')
    X,Y=data.getData()
    tX,tY=tdata.getData()
    for clf in clfList:
        str_='exp/'+rela+'-'+clf+'-'+str(t)+'.dat'
        print(str_,'start')
        fileName=open(str_,'w')
        avg=0
        for i in lv:
            ft=filterTree(i,clf)
            ft.train(X,Y)
            er=ft.perf(tX,tY)
            fileName.write('{0}\n'.format(er))
            avg+=er
            #work+=x
            #print('{0}'.format(work),end='\r')
        print(str_,'done')
        avg/=N
        fileName.write('@avg {0}\n'.format(avg))
        a1,a2=algor1(data),algor2(data)
        ft1,ft2=filterTree(a1.cal(),clf),filterTree(a2.cal(),clf)
        ft1.train(X,Y)
        ft2.train(X,Y)
        fileName.write('@a1 {0}\n'.format(ft1.perf(tX,tY)))
        fileName.write('@a2 {0}\n'.format(ft2.perf(tX,tY)))
        fileName.close()


if __name__=='__main__':
    fileList=['yeast']
    #fileList=['ecoli','flare','glass','led7digit','lymphography','nursery','page-blocks','satimage','vehicle']
    numList={'yeast':10,'ecoli':8,'flare':6,'glass':7,'led7digit':10,'lymphography':4,'nursery':5,'page-blocks':5,'satimage':7,'vehicle':4}
    #clfList=['linear']
    clfList=['linear','rbf','decision','knn','nb']
    n=11
    pool = mp.Pool()
    for rela in fileList:
        leaf=leaves(numList[rela])
        lv=leaf.getData()
        for t in range(5,n):
            pool.apply_async(fun, args = ((rela,t,lv,leaf.getNData()),))
    pool.close()
    pool.join()
