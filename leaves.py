import math
class leaves:
    def __init__(self,n=2,mode='opt'):
        self.n=n
        self.m=int(math.ceil(math.log(n,2)))
        #print("n {0} m {1}".format(self.n,self.m))
        self.tar=[[] for i in range(self.m+1)]
        self.tar[0]=[[i] for i in range(1,n+1)]
        self.data=[]

        if mode=='opt':
            self.gen()
            self.com(self.m+1,self.n,[],[])
        elif mode=='per':
            self.permu(n,[0 for i in range(n+1)],[0 for i in range(n)])

    def checkin(self,x,y):
        for i in x:
            if i in y:
                return False
        for i in x:
            y.append(i)
        return True

    def fun(self,num):
        l=len(num)
        tar=[]
        for i in range(l):
            tmp=[j for j in num[i]]
            for j in range(i+1,l):
                if self.checkin(num[j],tmp):
                    tar.append(num[i]+num[j])
        return tar[:]

    def gen(self):
        for i in range(1,self.m+1):
            self.tar[i]=self.fun(self.tar[i-1])

    def com(self,it,n,tmp,used):
        #print(it,n,tmp,used)
        if it==0:
            self.data.append(tmp)
            return 1;
        if n&(1<<(it-1))>0:
            for i in self.tar[(it-1)]:
                tused=used[:]
                if self.checkin(i,tused):
                    self.com(it-1,n%(1<<it),tmp+i,tused)
        else:
            self.com(it-1,n%(1<<it),tmp,used)

    def permu(self,n,used,tmp):
        if n==0:
            self.data.append(tmp[:])
        for i in range(1,self.n+1):
            if used[i]==0:
                used[i]=1
                tmp[n-1]=i
                self.permu(n-1,used,tmp)
                used[i]=0

    def getData(self):
        return self.data

    def showTar(self,n):
        [print (i) for i in self.tar[n]]

    def showData(self):
        [print(i) for i in self.data]
        
if __name__ == '__main__':
    leaf=leaves(5)
    leaf.showData()
