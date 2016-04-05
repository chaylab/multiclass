#from leaves import leaves
import numpy as np
import math
from sklearn.svm import SVC
from loaddata import loadData
class filterTree:
    def __init__(self,num):
        self.k=len(num)
        self.k=int([math.pow(2,i) for i in range(10) if math.pow(2,i)<=self.k][-1])
        self.num=num
        print (self.num)
        self.clf=[SVC()]*(self.k-1)
        self.datX=[[] for i in range(self.k)]
        self.datY=[[] for i in range(self.k)]

    def train(self,X,Y): # X,Y is list Y =[0,k-1]
        l=len(Y)
        if len(X)==l: print('OK')
        for i in range(l):
            k=self.num.index(Y[i]+1)+self.k-1
            j=(k-1)/2
            while j>=0:
                self.datX[int(j)].append(X[i])
                #1 left 0 other(right)
                self.datY[int(j)].append(int(k)%2)
                k=j
                j=(j-1)/2
        for i in range(self.k-1):
            A=np.array(self.datX[i])
            B=np.array(self.datY[i])
            #print (X,Y)
            self.clf[i].fit(A,B)
        #[print (i,self.datX[i], self.datY[i]) for i in range(self.k-1)]

    def test(self,X,n=0): #X is list
        if n>=self.k-1:
            return n-(self.k-1)
        pdt=self.clf[n].predict([X])
        #print (X,n,pdt)
        if pdt[0]==0:
            return self.test(X,2*n+2)
        return self.test(X,2*n+1)

    def perf(self,X,Y): #X,Y is list
        cor=0
        l=len(X)
        for i in range(l):
            if self.test(X[i])==Y[i]:
                cor+=1
        return cor/l

if __name__=='__main__':
    data=loadData('in.dat')
    data.load()
    ft=filterTree([i+1 for i in range(data.getK())])
    ft.train(data.getX(),data.getY())

    tst=loadData('out.dat')
    tst.load()
    print (ft.perf(tst.getX(),tst.getY()))
