from filtertree import filterTree
from gendata import genData
from leaves import leaves
if __name__=='__main__':
    n=5
    n_tra=1000
    n_tst=int(n_tra/0.2)
    num=[5,4,3,2,1]
    data=genData(num,n_tra,n_tst)
    X,Y=data.getData()
    lv=leaves(n).getAll()
    mx=0
    per=[]
    for i in lv:
        ft=filterTree(i)
        ft.train(X[:n_tra],Y[:n_tra])
        er=ft.perf(X[n_tra:],Y[n_tra:])
        print(i,er)
        if er>mx:
            mx=er
            per=i[:]
    print(per,mx)
    data.plot()
