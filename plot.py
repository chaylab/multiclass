import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
from matplotlib.patches import Ellipse
class loadEx:
    def __init__(self,fname):
        self.file=open('exp/{0}.dat'.format(fname),'r')
        self.filee=open('exp/{0}-exp.dat'.format(fname),'r')
        self.freq={}
        self.ext=[]
        self.ndata=0
        self.load()

    def load(self):
        for line in self.file:
            if line[0]!='@':
                self.ndata+=1
                if line[:-1] in self.freq:
                    self.freq[line[:-1]]+=1
                else:
                    self.freq[line[:-1]]=1
        self.file.close()
        for line in self.filee:
            tmp=line[:-1].split(' ')
            self.ext.append([tmp[0],float(tmp[1])])
        self.filee.close()

    def getNData(self):
        return self.ndata

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
                self.exts[0][j][1]+=self.exts[i][j][1]
        for i,j in self.freqs[0].items():
            j/=self.n
        for i in range(len(self.exts[0])):
            self.exts[0][i][1]/=self.n

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
        ax.annotate(self.ext[0][0], xy=(self.ext[0][1], 0), xycoords='data',
            xytext=(0, 50), textcoords='offset points',size=15,
            arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90,rad=5"),)
        ax.annotate(self.ext[1][0], xy=(self.ext[1][1], 0), xycoords='data',
            xytext=(0, 70), textcoords='offset points',size=15,
            arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90,rad=5"),)
        ax.annotate(self.ext[2][0], xy=(self.ext[2][1], 0), xycoords='data',
            xytext=(0, 90), textcoords='offset points',size=15,
            arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90,rad=5"),)
        plt.show()

    def plot2(self):
        X=np.array(self.freq)
        fig, ax = plt.subplots()

        # histogram our data with numpy
        #data = np.random.randn(1000)
        #n, bins = np.histogram(data, 50)
        n, bins = X[:, 1],X[:, 0]
        # get the corners of the rectangles for the histogram
        left = np.array(bins[:-1])
        right = np.array(bins[:-1])+np.array([0.007 for i in range(len(bins)-1)])
        bottom = np.zeros(len(left))
        top = bottom + n[:-1]
        # we need a (numrects x numsides x 2) numpy array for the path helper
        # function to build a compound path
        XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T

        # get the Path object
        barpath = path.Path.make_compound_path_from_polys(XY)

        # make a patch out of it
        patch = patches.PathPatch(
            barpath, facecolor='blue', edgecolor='none', alpha=0.8)
        ax.add_patch(patch)

        # update the view limits
        ax.set_xlim(left[0], right[-1])
        ax.set_ylim(bottom.min(), top.max())
        plt.xlabel('Error Rate')
        plt.ylabel('Frequence')
        plt.grid(True)
        plt.title('DataSet: '+self.rela+' , Binary Classifier: '+self.clf)
        ax.annotate(self.ext[0][0], xy=(self.ext[0][1], 0), xycoords='data',
            xytext=(0, 50), textcoords='offset points',size=15,
            arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90,rad=5"),)
        ax.annotate(self.ext[1][0], xy=(self.ext[1][1], 0), xycoords='data',
            xytext=(0, 70), textcoords='offset points',size=15,
            arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90,rad=5"),)
        ax.annotate(self.ext[2][0], xy=(self.ext[2][1], 0), xycoords='data',
            xytext=(0, 90), textcoords='offset points',size=15,
            arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90,rad=5"),)
        plt.show()

class plotData:
    def __init__(self,rela,clf):
        self.rela=rela
        self.clf=clf
        self.n=10
        self.nclf=len(clf)
        self.ealgor=[[0 for i in range(self.nclf)] for i in range(10)]

        self.load()

    def load(self):
        for i in range(self.nclf):
            tmp=loadBin(self.rela,self.clf[i],self.n).getExt()
            self.lalgor=[j[0] for j in tmp]
            self.nalgor=(len(tmp))
            for j in range(len(tmp)):
                self.ealgor[j][i]=tmp[j][1]

    def plot(self):
        fig=plt.figure(1,figsize=(8,8))
        ax=fig.add_subplot(111)
        color='rbgyc'
        width=0.1
        rec=[]
        for i in range(self.nalgor):
            rec.append(ax.bar([(j+width*i) for j in range(self.nclf)],
            tuple([1-j for j in self.ealgor[i]]), width,
            [j for j in self.ealgor[i]],color=color[i],alpha=0.5))
        ax.set_ylabel('Error rate')
        plt.ylim(1,0)
        plt.grid(True)
        ax.set_title('DataSet: '+self.rela)
        ax.set_xticks([i+width for i in range(self.nclf)])
        ax.set_xticklabels(self.clf)
        ax.legend([i[0] for i in rec],self.lalgor)
        plt.show()


if __name__=='__main__':
    if 0:
        pl=plotClf('yeast','nb',10)
    else:
        pl=plotData('yeast',['linear','rbf','decision','knn','nb'])
        #pl=plotData('yeast',['linear'])
    pl.plot()
