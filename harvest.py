from filtertree import filterTree
from gendata import genData
from leaves import leaves
from loaddata import loadData
from algor import algor1,algor2
import multiprocessing as mp
def fun(Data):
    rela,t,lv,N = Data
    data=loadData('dataset/{0}/{0}-10dobscv-{1}tra.dat'.format(rela,t))
    tdata=loadData('dataset/{0}/{0}-10dobscv-{1}tst.dat'.format(rela,t))
    X,Y=data.getData()
    tX,tY=tdata.getData()
    for clf in clfList:
        str_='exp/{0}-{1}-{2}.dat'.format(rela,clf,t)
        fileName=open(str_,'w')
        print(str_,'start')
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
        fileName.close()


if __name__=='__main__':
    fileList=['satimage']
    #flare start with 0
    #lym nursery input string
    #fileList=['yeast','ecoli','flare','glass','lymphography','nursery','page-blocks','satimage','vehicle','led7digit']
    numList={'yeast':10,'ecoli':8,'flare':6,'glass':7,'led7digit':10,'lymphography':4,'nursery':5,'page-blocks':5,'satimage':7,'vehicle':4}
    #clfList=['linear']
    clfList=['linear','rbf','decision','knn','nb']
    n=11
    pool = mp.Pool()
    for rela in fileList:
        leaf=leaves(numList[rela])
        lv=leaf.getData()
        for t in range(1,n):
            pool.apply_async(fun, args = ((rela,t,lv,leaf.getNData()),))
    pool.close()
    pool.join()
