import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_classification
from sklearn.datasets import make_blobs
from sklearn.datasets import make_gaussian_quantiles

class genData(object):
    def __init__(self,lst,tra=100,tst=20):
        #self.X,self.Y=make_classification(n_features=10, n_redundant=0,n_samples=1000,n_classes=10
        #,n_informative=9,n_repeated=0,n_clusters_per_class=1,hypercube=False)
        n=len(lst)
        self.n=n
        num=[(i*3,i*3) for i in range(1,n+1)]
        if len(lst)!=n:
            print("lst must be equl n")
            return None
        cen=[num[i-1] for i in lst]
        print(cen)
        self.X,self.Y=make_blobs(n_features=2, centers=cen, n_samples=tra+tst)

    def plot(self):
        X,Y=self.X,self.Y
        plt.figure(figsize=(8, 8))
        #print(X[:, 0])
        for i in range(self.n):
            x=[X[j][0] for j in range(Y.size) if Y[j]==i]
            y=[X[j][1] for j in range(Y.size) if Y[j]==i]
            z='rbgyc'[i]
            plt.scatter(x,y, marker='x',color=z, label=str(i+1))
        #plt.scatter(X[:, 0], X[:, 1], marker='x', c=Y, label=str(Y))
        plt.legend(scatterpoints=1,fontsize=8)

        plt.show()

    def getData(self):
        return self.X,self.Y

    def printData(self,fname):
        fname=open(fname,'w')
        s=','.join([str(i) for i in range(self.n)])
        s='@attribute {{{0}}}\n'.format(s)
        fname.write(s)
        l=len(self.X)
        for i in range(l):
            s=', '.join([str(j) for j in (self.X[i].tolist()+[self.Y[i]])])
            fname.write(s+'\n')

    def getK(self):
        return self.n

if __name__=='__main__':
    #data=genData([2,1,3,4,5],1000,200)
    #data.plot()
    data=genData([2,1,3,4,5],100,20)
    data.plot()
    #data.printData('dat1.in')
