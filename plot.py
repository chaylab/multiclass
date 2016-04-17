import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
class loadEx:
    def __init__(self,fname):
        self.file=open('exp/'+fname+'.dat','r')
        self.freq={}
        self.ext=[]

        self.load()

    def load(self):
        for line in self.file:
            if line[0]!='@':
                if line[:-1] in self.freq:
                    self.freq[line[:-1]]+=1
                else:
                    self.freq[line[:-1]]=0
            else:
                self.ext.append(float(line.split(' ')[1][:-1]))

    def getData(self):
        return self.freq

    def getExt(self):
        return self.ext

class loadBin:
    def __init__(self,rela,clf,n):
        self.rela=rela
        self.clf=clf
        self.freqs=[]
        self.exts=[]
        self.n=n

        self.load()
        self.merge()

    def fname(self,rela,clf,n):
        return rela+'-'+clf+'-'+str(n)

    def load(self):
        for i in range(1,self.n+1):
            tmp=loadEx(self.fname(self.rela,self.clf,i))
            self.freqs.append(tmp.getData())
            self.exts.append(tmp.getExt())

    def merge(self):
        for i in range(1,self.n):
            for j,k in self.freqs[i].items():
                if j[0] in self.freqs[0]:
                    self.freqs[0][j]+=k
                else:
                    self.freqs[0][j]=k
            for j in range(len(self.exts[i])):
                self.exts[0][j]+=self.exts[i][j]
        for i,j in self.freqs[0].items():
            j/=self.n
        for i in range(len(self.exts[0])):
            self.exts[0][i]/=self.n

    def getData(self):
        return [(float(i),j) for i,j in self.freqs[0].items()]

    def getExt(self):
        return self.exts[0]

class plotClf:
    def __init__(self,rela,clf,n):
        self.rela=rela
        self.clf=clf
        self.n=n

        self.load()

    def load(self):
        self.file=loadBin(self.rela,self.clf,self.n)
        self.freq=self.file.getData()
        self.ext=self.file.getExt()

        self.freq=sorted(self.freq,key=lambda x: (x[0],x[1]))

    def plot(self):
        print(self.ext)
        X=np.array(self.freq)
        el = Ellipse((2, -1), 0.5, 0.5)
        plt.plot(X[:, 0], X[:, 1],lw=1.5)
        plt.xlabel('Error Rate')
        plt.ylabel('Frequence')
        #plt.xlim(0, 1)
        plt.grid(True)
        plt.title('DataSet: '+self.rela+' , Binary Classifier: '+self.clf)
        fig=plt.figure(1,figsize=(8,8))
        ax=fig.add_subplot(111)
        ax.annotate('mean: '+str(self.ext[0]), xy=(self.ext[0], 0), xycoords='data',
            xytext=(0, 50), textcoords='offset points',size=15,
            arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90,rad=5"),)
        ax.annotate('algor1: '+str(self.ext[1]), xy=(self.ext[1], 0), xycoords='data',
            xytext=(0, 70), textcoords='offset points',size=15,
            arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90,rad=5"),)
        ax.annotate('algor2: '+str(self.ext[2]), xy=(self.ext[2], 0), xycoords='data',
            xytext=(0, 90), textcoords='offset points',size=15,
            arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90,rad=5"),)
        plt.show()

class plotData:
    def __init__(self,rela,clf,nalgor=1):
        self.rela=rela
        self.clf=clf
        self.n=4
        self.nclf=len(clf)
        self.nalgor=nalgor+1
        self.ealgor=[[0 for i in range(self.nclf)] for i in range(self.nalgor)]

        self.load()

    def load(self):
        for i in range(self.nclf):
            tmp=loadBin(self.rela,self.clf[i],self.n).getExt()
            for j in range(self.nalgor): #avg was add
                self.ealgor[j][i]=tmp[j]

    def plot(self):
        fig=plt.figure(1,figsize=(8,8))
        ax=fig.add_subplot(111)
        color='rbgyc'
        width=0.1
        rec=[]
        for i in range(self.nalgor):
            rec.append(ax.bar([(j+width*i) for j in range(self.nclf)],
            tuple([1-j for j in self.ealgor[i]]), width,
            [j for j in self.ealgor[i]],color=color[i]))
        ax.set_ylabel('Error rate')
        plt.ylim(1,0)
        plt.grid(True)
        ax.set_title('DataSet: '+self.rela)
        ax.set_xticks([i+width for i in range(self.nclf)])
        ax.set_xticklabels(self.clf)
        ax.legend([i[0] for i in rec],['avg']+['algor'+str(i+1) for i in range(self.nalgor-1)])
        plt.show()


if __name__=='__main__':
    #pl=plotClf('yeast','linear',4)
    #pl.plot()
    pl=plotData('yeast',['linear','rbf','decision','knn','nb'],2)
    pl.plot()
