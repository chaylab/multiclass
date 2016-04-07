import matplotlib.pyplot as plt

from sklearn.datasets import make_classification
from sklearn.datasets import make_blobs
from sklearn.datasets import make_gaussian_quantiles

class genData(object):
    def __init__(self,lst,tra=100,tst=20):
        #self.X,self.Y=make_classification(n_features=10, n_redundant=0,n_samples=1000,n_classes=10
        #,n_informative=9,n_repeated=0,n_clusters_per_class=1,hypercube=False)
        n=len(lst)
        num=[(i*3,i*3) for i in range(1,n+1)]
        if len(lst)!=n:
            print("lst must be equl n")
            return None
        cen=[num[i-1] for i in lst]
        self.X,self.Y=make_blobs(n_features=2, centers=cen, n_samples=tra+tst)

    def plot(self):
        X,Y=self.X,self.Y
        plt.figure(figsize=(8, 8))
        plt.scatter(X[:, 0], X[:, 1], marker='o', c=Y)
        #for i in Y:
            #plt.plot(label='Class %s'%i,color=i)
        plt.show()

    def getData(self):
        return self.X,self.Y

if __name__=='__main__':
    data=genData([2,1,3,4,5],1000,200)
    data.plot()
