#from leaves import leaves
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.svm import SVC,LinearSVC
from sklearn.tree import DecisionTreeRegressor,DecisionTreeClassifier
from loaddata import loadData
from leaves import leaves
class filterTree:
    def __init__(self,num):
        #print("__init filterTree__")
        self.k=len(num)
        self.k=int(2**math.ceil(math.log(self.k,2)))
        self.num=num
        #self.clf=[SVC(kernel='linear') for i in range(self.k-1)]
        #self.clf=[DecisionTreeClassifier() for i in range(self.k-1)]
        self.clf=[LinearSVC() for i in range(self.k-1)]
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
            ans=self.test(X[i])
            #print(ans,Y[i])
            if ans==Y[i]:
                cor+=1
        return cor/l

    def plotClf(self):
        for i in range(self.k-1):
            if self.winby[i]==1 or len(self.datX[i])==0: continue
            X=np.array(self.datX[i]).T
            Y=self.datY[i]
            plt.figure(i, figsize=(5, 5))
            plt.clf()
            plt.scatter(self.clf[i].support_vectors_[:, 0], self.clf[i].support_vectors_[:, 1], s=80,facecolors='none', zorder=10)
            plt.scatter(X[:, 0], X[:, 1], c=Y, zorder=10, cmap=plt.cm.Paired)

            plt.axis('tight')
            x_min = -5
            x_max = 5
            y_min = -5
            y_max = 5

            XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
            Z = self.clf[i].decision_function(np.c_[XX.ravel(), YY.ravel()])

            # Put the result into a color plot
            Z = Z.reshape(XX.shape)
            plt.figure(i, figsize=(5, 5))
            plt.pcolormesh(XX, YY, Z > 0, cmap=plt.cm.Paired)
            plt.contour(XX, YY, Z, colors=['k', 'k', 'k'], linestyles=['--', '-', '--'],levels=[-.5, 0, .5])

            plt.xlim(x_min, x_max)
            plt.ylim(y_min, y_max)

            plt.xticks(())
            plt.yticks(())
        plt.show()

if __name__=='__main__':

    #ft=filterTree([1,2,3,4])
    #ft.train([[1,0],[0,1],[-1,-1],[-2,-2],[1,-2],[-2,1]],[0,0,2,2,1,3])
    #ft.plotClf()
    #print (ft.test([1.5,-1.5]))

    '''for i in range(1,11):
        s="led7digit"
        n=10
        stra='dataset/'+s+'/'+s+'-'+str(n)+'dobscv-'+str(i)+'tra.dat'
        stst='dataset/'+s+'/'+s+'-'+str(n)+'dobscv-'+str(i)+'tst.dat'
        data=loadData(stra)
        data.load()
        tst=loadData(stst)
        tst.load()
        #print("load {0} complete".format(stra))
        lv=leaves(data.getK()).getAll()
        #print("generate leaves complete")
        mx=0
        for i in lv:
            ft=filterTree(i)
            ft.train(data.getX(),data.getY())
            er=ft.perf(tst.getX(),tst.getY())
            if er>mx:
                mx=er
                per=i[:]
        print (per,mx)'''
