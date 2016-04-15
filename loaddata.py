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

class loadData:
    def __init__(self,fname='in.dat'):
        try:
            self.file=open(fname,'r')
        except:
            print("load file error")
            return False

        self.attrs=[]
        self.vcls={}
        self.ncls=2
        self.X=[]
        self.Y=[]
        self.load()

    def load(self):
        for str in self.file:
            if re.match('@\w*',str)!=None:
                lst=str.split(' ')
                if lst[0]=='@relation':
                    self.name=lst[1]
                elif lst[0]=='@attribute':
                    if len(lst)==3:
                        tmp=lst[2][lst[2].index('[')+1:lst[2].index(']')].split(',')
                        self.attrs.append(attr(lst[1],(float(tmp[0]),float(tmp[1]))))
                    else:
                        j=0
                        for i in lst[1][lst[1].index('{')+1:lst[1].index('}')].split(','):
                            self.vcls[i]=j
                            j+=1
                        self.ncls=j
            else:
                tmp=str[:-1].split(', ')
                self.X.append([float(i) for i in tmp[:-1]])
                self.Y.append(self.vcls[tmp[-1]])
        self.ninst=len(self.X)
        self.file.close()

    def show(self):
        [print(self.X[i],self.Y[i]) for i in range(self.ninst)]

    def getNCls(self): #getK
        return self.ncls

    def getData(self):
        return (self.X,self.Y)

    def getNData(self):
        return self.ninst

    def getNAttr(self):
        return len(self.attrs)

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

if __name__=='__main__':
    dat=loadData('dataset/yeast/yeast-10dobscv-1tra.dat')
    dat.show()
    [print(i.name,i.bound) for i in dat.getAttr()]
