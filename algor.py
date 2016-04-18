import math
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

class algorContain:
    def __init__(self):
        self.algors=[algor1,algor2]

    def getAlgor(self):
        return self.algors

if __name__=='__main__':
    data=loadData('dataset/vowel/vowel-10dobscv-1tra.dat')
    #algor=algor1(data)
    #print(algor.cal())
    algor2=algor2(data)
    print(algor2.cal())
