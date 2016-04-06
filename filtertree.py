#from leaves import leaves
import numpy as np
import math
from sklearn.svm import SVC
from loaddata import loadData
from leaves import leaves
class filterTree:
    def __init__(self,num):
        #print("__init filterTree__")
        self.k=len(num)
        self.k=int(2**math.ceil(math.log(self.k,2)))
        self.num=num
        self.clf=[SVC()]*(self.k-1)
        self.datX=[[] for i in range(self.k)]
        self.datY=[[] for i in range(self.k)]
        self.winby=[0 for i in range(self.k)]

        x=self.getPos(num[-1])
        self.clearPath(int((x-1)/2),x%2)

    def getPos(self,n):
        return self.num.index(n)+self.k-1

    def clearPath(self,n,m): #n is pos of num of last leaf
        if n==0: return
        if m==1:
            self.winby[n]=1
            #print("ban {0}".format(n))
        self.clearPath(int((n-1)/2),n%2)

    def train(self,X,Y): # X,Y is list Y =[0,k-1]
        l=len(Y)
        for i in range(l):
            k=self.getPos(Y[i]+1)
            j=(k-1)/2
            while j>=0:
                self.datX[int(j)].append(X[i])
                #1 left 0 other(right)
                self.datY[int(j)].append(int(k)%2)
                k=j
                j=(j-1)/2
        for i in range(self.k-1):
            if self.winby[i]==0 and len(self.datX[i])>0:
                A=np.array(self.datX[i])
                B=np.array(self.datY[i])
                #print (B)
                try:
                    self.clf[i].fit(A,B)
                except:
                    print(self.datX[i])
        #print("training complete")
        #[print (i,self.datX[i], self.datY[i]) for i in range(self.k-1)]

    def test(self,X,n=0): #X is list
        if n>=self.k-1:
            return n-(self.k-1)
        if self.winby[n]==1:
            pdt=[1]
        else:
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

    #ft=filterTree([i+1 for i in range(4)])
    #ft.train([[1],[2],[3],[4]],[0,1,2,3])

    data=loadData('in.dat')
    data.load()
    tst=loadData('out.dat')
    tst.load()

    lv=leaves(data.getK()).getAll()

    for i in lv:
        ft=filterTree(i)
        ft.train(data.getX(),data.getY())
        print (i,ft.perf(tst.getX(),tst.getY()))
