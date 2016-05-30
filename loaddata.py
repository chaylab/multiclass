import re
import matplotlib.pyplot as plt
class attr:
    def __init__(self,name,bound):
        self.name=name
        self.bound=bound

    def getName(self):
        return self.name

    def getBound(self):
        return self.bound

    def getRange(self):
        return self.bound[1]-self.bound[0]

class loadData:
    def __init__(self,fname='in.dat'):
        try:
            self.file=open(fname,'r')
        except:
            print("load file error")
            return False

        self.attrs=[]
        self.map=[]
        self.ncls=2
        self.ninst=0
        self.nattrs=0
        self.seq=[]
        self.out=[]
        self.X=[]
        self.Y=[]
        self.load()

    def load(self):
        for str_ in self.file:
            if re.match('@\w*',str_)!=None:
                lst=str_.split(' ')
                if lst[0]=='@relation':
                    self.name=lst[1]
                elif lst[0]=='@attribute':
                    if len(lst)==3:
                        tmp=lst[2][lst[2].index('[')+1:lst[2].index(']')].split(',')
                        self.attrs.append(attr(lst[1],(float(tmp[0]),float(tmp[1]))))
                        self.map.append(0)
                    else:
                        j=0
                        tmp={}
                        for i in lst[1][lst[1].index('{')+1:lst[1].index('}')].split(','):
                            tmp[i]=j
                            j+=1
                        self.map.append(tmp)
                        self.attrs.append(attr(lst[1][:lst[1].index('{')],(0,j)))
                elif lst[0]=='@inputs':
                    self.seq=lst[1][:-1].split(',')
                    for i in range(len(self.seq)):
                        for j in range(len(self.attrs)):
                            if self.seq[i]==self.attrs[j].getName():
                                self.map[i],self.map[j]=self.map[j],self.map[i]
                                self.attrs[i],self.attrs[j]=self.attrs[j],self.attrs[i]
                                break
                elif lst[0]=='@outputs':
                    self.out=lst[1][:-1]
            else:
                tmp=str_[:-1].split(', ')
                x,y=[],[]
                for i in range(len(tmp)):
                    if i <len(self.seq):
                        if self.map[i]==0:
                            x.append(float(tmp[i]))
                        else:
                            x.append(float(self.map[i][tmp[i]]))
                    else:
                        y.append(float(self.map[i][tmp[i]]))
                self.X.append(x)
                self.Y.append(y)
        self.ninst=len(self.X)
        self.nattrs=len(self.attrs)-1
        self.ncls=self.attrs[-1].getRange()
        self.file.close()
        self.makeStat()

    def makeStat(self):
        self.avg=[0 for i in range(self.nattrs)]
        self.SD=[0 for i in range(self.nattrs)]
        for i in range(self.ninst):
            for j in range(self.nattrs):
                self.avg[j]+=self.X[i][j]
        for j in range(self.nattrs):
            self.avg[j]/=self.ninst
        for i in range(self.ninst):
            for j in range(self.nattrs):
                self.SD[j]+=(self.X[i][j]-self.avg[j])**(2)
        for j in range(self.nattrs):
            self.SD[j]=self.SD[j]**(0.5)

    def show(self):
        [print(self.X[i],self.Y[i]) for i in range(self.ninst)]

    def getSD(self):
        return self.SD

    def getAvg(self):
        return self.avg

    def getNCls(self): #getK
        return self.ncls

    def getData(self):
        return (self.X,self.Y)

    def getNData(self):
        return self.ninst

    def getNAttr(self):
        return self.nattrs

    def getAttr(self): #getFeature
        return self.attrs

    def plot(self):
        if self.getAttr()>2:
            print('Instances cant plot')
            return False
        X,Y=self.X,self.Y
        plt.figure(figsize=(8, 8))
        for i in range(self.ncls):
            x=[X[j][0] for j in range(len(Y)) if Y[j]==i]
            y=[X[j][1] for j in range(len(Y)) if Y[j]==i]
            z='rbgyc'[i]
            plt.scatter(x,y, marker='x',color=z, label=str(i+1))
        plt.legend(scatterpoints=1,fontsize=8)
        plt.show()
