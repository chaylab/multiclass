from filtertree import filterTree
from gendata import genData
from leaves import leaves
from loaddata import loadData
from sklearn.svm import SVC,LinearSVC
from sklearn.tree import DecisionTreeRegressor,DecisionTreeClassifier
if __name__=='__main__':
    n=4
    n_tra=2000
    n_tst=int(n_tra/0.2)
    num=[1,3,2,4] #1432 is max
    #data=genData(num,n_tra,n_tst)
    #data=loadData('exp/ed.dat')

    data=loadData('dataset/yeast/yeast-10dobscv-1tra.dat')
    tdata=loadData('dataset/yeast/yeast-10dobscv-1tst.dat')
    X,Y=data.getData()
    tX,tY=tdata.getData()
    leaf=leaves(data.getNCls())
    mx,mn,mj,mk=-1,1,0,0
    per,perm=[],[]
    ft=[i for i in range(leaf.getNData())]
    j,k=0,0
    avg=0
    lv=leaf.getData()
    for i in lv:
        ft[j]=filterTree(i)
        ft[j].train(X,Y)
        er=ft[j].perf(tX,tY)
        avg+=er
        print(i,er)
        if er<mn:
            mk=k
            mn=er
            perm=i[:]

        if er>mx:
            mj=j
            mx=er
            per=i[:]
        else:
            pass
            #ft[j]=True
        j+=1
        k+=1
    avg/=leaf.getNData()
    print('max error{0} {1}'.format(per,mx))
    print('min error{0} {1}'.format(perm,mn))
    print('avg error {0}'.format(avg))
    #data.plot()
    #data.printData('exp/ed.dat')
    #ft[mj].plotClf()
    #ft[mk].plotClf()
