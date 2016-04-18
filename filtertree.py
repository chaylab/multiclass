#from leaves import leaves
import math
import matplotlib.pyplot as plt
import numpy as np
from loaddata import loadData
from leaves import leaves
from sklearn.svm import SVC,LinearSVC
from sklearn.tree import DecisionTreeRegressor,DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
class filterTree:
    def __init__(self,num,clf='linear'):
        #print("__init filterTree__")
        self.k=len(num)
        self.k=int(2**math.ceil(math.log(self.k,2)))
        self.num=num
        if clf=='linear':
            self.clf=[SVC(kernel='linear') for i in range(self.k-1)]
        if clf=='rbf':
            self.clf=[SVC(kernel='rbf') for i in range(self.k-1)]
        if clf=='decision':
            self.clf=[DecisionTreeClassifier() for i in range(self.k-1)]
        if clf=='knn':
            self.clf=[KNeighborsClassifier() for i in range(self.k-1)]
        if clf=='nb':
            self.clf=[GaussianNB() for i in range(self.k-1)]
        if clf=='rf':
            self.clf=[RandomForestClassifier() for i in range(self.k-1)]
        if clf=='ada':
            self.clf=[AdaBoostClassifier() for i in range(self.k-1)]
        self.dataX=[[] for i in range(self.k)]
        self.dataY=[[] for i in range(self.k)]
        self.winby=[0 for i in range(self.k)]

        x=self.getPos(num[-1])
        self.clearPath(int((x-1)/2),x%2)

    def getPos(self,n):
        return self.num.index(n)+self.k-1

    def clearPath(self,n,m): #n is pos of num of last leaf
        if n==0: return
        if m==1:
            self.winby[n]=2
            #print("ban {0}".format(n))
        self.clearPath(int((n-1)/2),n%2)

    def train(self,X,Y): # X,Y is list Y =[0,k-1]
        l=len(Y)
        for i in range(l):
            k=self.getPos(Y[i]+1)
            j=(k-1)/2
            while j>=0:
                self.dataX[int(j)].append(X[i])
                #1 left 0 other(right)
                self.dataY[int(j)].append(int(k)%2)
                k=j
                j=(j-1)/2
        for i in range(self.k-1):
            if self.winby[i]==0 and len(self.dataX[i])>0:
                A=np.array(self.dataX[i])
                B=np.array(self.dataY[i])
                #print (B)
                try:
                    self.clf[i].fit(A,B)
                except:
                    self.winby[i]=B[0]+1
                    #print(self.dataX[i])
        #print("training complete")
        #[print (i,self.dataX[i], self.dataY[i]) for i in range(self.k-1)]

    def test(self,X,n=0): #X is list
        if n>=self.k-1:
            return n-(self.k-1)
        if self.winby[n]>0:
            pdt=[self.winby[n]-1]
        else:
            pdt=self.clf[n].predict([X])
        if pdt[0]==0:
            return self.test(X,2*n+2)
        return self.test(X,2*n+1)

    def perf(self,X,Y): #X,Y is list
        cor=0
        l=len(X)
        for i in range(l):
            ans=self.num[self.test(X[i])]-1
            if ans==Y[i]:
                cor+=1
        return (l-cor)/l

    def plotClf(self):
        for i in range(0,1):
        #for i in range(self.k-1)
            if self.winby[i]==1 or len(self.dataX[i])==0: continue
            X=np.array(self.dataX[i])
            Y=self.dataY[i]
            plt.figure(i, figsize=(8, 8))
            plt.title('classifier{0} {1}'.format(i,repr(self.num)))
            plt.clf()
            plt.scatter(self.clf[i].support_vectors_[:, 0], self.clf[i].support_vectors_[:, 1], s=80,facecolors='none', zorder=10)
            #plt.scatter(X[:, 0], X[:, 1], c=Y, zorder=10, cmap=plt.cm.Paired)
            plt.scatter(X[:, 0], X[:, 1], c=Y, zorder=10, marker='x')

            plt.axis('tight')
            x_min,x_max,y_min,y_max= -5,20,-5,20
            XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
            Z = self.clf[i].decision_function(np.c_[XX.ravel(), YY.ravel()])
            Z = Z.reshape(XX.shape)
            plt.figure(i, figsize=(8, 8))
            plt.pcolormesh(XX, YY, Z > 0, cmap=plt.cm.Paired)
            plt.contour(XX, YY, Z, colors=['r', 'k', 'b'], linestyles=['--', '-', '--'],levels=[-.5, 0, .5])
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

    ft=filterTree([2,1,4,3,5])
    ft.train([(3, 3), (9, 9), (6, 6), (15, 15), (12, 12)],[0,1,2,3,4])
    ft.plotClf()

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
