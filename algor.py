import math
import numpy as np
from loaddata import loadData

class algor1:
    def __init__(self,data):
        self.data=data
        self.X,self.Y=[],[]
        self.avg=[[0 for i in range(self.data.getNAttr())] for i in range(self.data.getNCls())]
        self.ncls=[0 for i in range(self.data.getNCls())]
        self.avgs=[0 for i in range(self.data.getNAttr())]
        self.SD=[0 for i in range(self.data.getNAttr())]

        self.reScale()
        self.calAvg()
        self.calSD()
        #self.cal()

    def getName(self):
        return "attribute sort"

    def reScale(self): # to 0-1
        X,self.Y=self.data.getData()
        attrs=self.data.getAttr()
        for i in X:
            tmp=[]
            for j in range(self.data.getNAttr()):
                b=attrs[j].getBound()[0]
                a=attrs[j].getBound()[1]
                tmp.append((i[j]-b)/(a-b))
            self.X.append(tmp)

    def calAvg(self):
        for i in range(self.data.getNData()):
            for j in range(self.data.getNAttr()):
                self.avg[self.Y[i]][j]+=self.X[i][j]
                self.ncls[self.Y[i]]+=1
                self.avgs[j]+=self.X[i][j]
        for j in range(self.data.getNAttr()):
            for i in range(self.data.getNCls()):
                if self.ncls[i]>0:
                    self.avg[i][j]/=self.ncls[i]
            self.avgs[j]/=self.data.getNData()

    def calSD(self):
        for i in self.X:
            for j in range(self.data.getNAttr()):
                self.SD[j]+=(i[j]-self.avgs[j])**2
        for j in range(self.data.getNAttr()):
            self.SD[j]=self.SD[j]**(0.5)

    def cal(self):
        sd=sorted([(i,self.SD[i]) for i in range(self.data.getNAttr())],key=lambda x: (x[1],x[0]))
        tmp=[(i,self.avg[i]) for i in range(self.data.getNCls())]
        tmp=sorted(tmp,key=lambda x: [x[1][i[0]] for i in sd])
        return [i[0]+1 for i in tmp]

class algor2:
    def __init__(self,data):
        self.data=data
        self.X,self.Y=self.data.getData()
        self.ncls=[0 for i in range(self.data.getNCls())]
        self.point=[[0 for i in range(self.data.getNAttr())] for i in range(self.data.getNCls())]
        self.path=[[0 for i in range(self.data.getNCls())] for i in range(self.data.getNCls())]
        self.listPath=[]
        self.num=[i for i in range(self.data.getNCls())]

        self.calAvg()
        self.calPath()

    def getName(self):
        return "longest_path_first"

    def calAvg(self):
        for i in range(self.data.getNData()):
            for j in range(self.data.getNAttr()):
                self.point[self.Y[i]][j]+=self.X[i][j]
                self.ncls[self.Y[i]]+=1
        for i in range(self.data.getNCls()):
            for j in range(self.data.getNAttr()):
                if self.ncls[i]>0:
                    self.point[i][j]/=self.ncls[i]
    def dist(self,a,b):
        dis=0
        for i in range(len(a)):
            dis+=(a[i]-b[i])**2
        return dis**(0.5)

    def calPath(self):
        for i in range(self.data.getNCls()):
            for j in range(i+1,self.data.getNCls()):
                self.path[i][j]=self.dist(self.point[i],self.point[j])
                self.listPath.append((i,j,self.path[i][j]))
        self.listPath=sorted(self.listPath,key=lambda x: (-x[2],x[0],x[1]))

    def pair(self,num):
        n=len(num)
        if n<=2:
            return num
        nl=int(2**math.floor(math.log(n-1,2)))
        tmp=[[],[]] #0left 1right
        for i in self.listPath:
            x=tmp[0]+tmp[1]
            if len(x)==n: break
            if (i[0] in num) and (i[1] in num):
                for j in range(2):
                    if i[j] in x and not(i[(j+1)%2] in x):
                        if i[j] in tmp[0]:
                            tmp[1].append(i[(j+1)%2])
                        else:
                            tmp[0].append(i[(j+1)%2])
                if not(i[0] in x) and not(i[1] in x):
                    tmp[0].append(i[0])
                    tmp[1].append(i[1])
                #print(i,tmp[0],tmp[1])
        tmp=tmp[0]+tmp[1][::-1]
        #print(tmp[:nl],tmp[nl:])
        return self.pair(tmp[:nl])+self.pair(tmp[nl:])

    def cal(self):
        return [i+1 for i in self.pair(self.num)]

class algor3(algor2):
    def getName(self):
        return "longest_path_projection"

    def scalar(self,v,tmp=0):
        for i in v:
            tmp+=i**2
        return tmp**(0.5)

    def shadow(self,va,vb):
        if self.scalar(vb)==0.0000000000:
            return self.listPath[0][2]+1
        return np.dot(va,vb)/self.scalar(vb)

    def tov(self,a,b):
        return [b[i]-a[i] for i in range(len(a))]

    def getRef(self):
        return self.tov(self.point[self.listPath[0][0]],self.point[self.listPath[0][1]])

    def cal(self):
        tmp=[]
        va=self.getRef()
        for i in range(self.data.getNCls()):
            vb=self.tov(self.point[self.listPath[0][0]],self.point[i])
            tmp.append((self.shadow(va,vb),i))
        tmp=sorted(tmp,key=lambda x: x[0])
        return [i[1]+1 for i in tmp]

class algor4(algor3):
    def getName(self):
        return "random_path_projection"

    def getRef(self):
        SD=[max(0.000001,i) for i in self.data.getSD()]
        avg=self.data.getAvg()
        a=[np.random.normal(avg[i], SD[i], 1)[0] for i in range(self.data.getNAttr())]
        b=[np.random.normal(avg[i], SD[i], 1)[0] for i in range(self.data.getNAttr())]
        return self.tov(a,b)

class random:
    def __init__(self,data):
        self.tmp=[i for i in range(1,data.getNCls()+1)]

    def getName(self):
        return "random"

    def cal(self):
        return random.shuffle(tmp)

class algorContain:
    def __init__(self):
        self.algors=[algor1,algor2,algor3,algor4]

    def getAlgor(self):
        return self.algors
