class leaves:
    def __init__(self,n=2):
        self.n=n
        self.it=0
        self.num=[[i] for i in range(1,n+1)]
        self.tar=self.rec(self.n,self.num)
        self.lim=len(self.tar)

    def get(self):
        if self.it < self.lim:
            self.it+=1
            return self.tar[self.it-1]
        return None

    def fun(self,num):
        l=len(num)
        tar=[]
        for i in range(l):
            tmp=[j for j in num[i]]
            for j in range(i+1,l):
                x=0
                for k in num[j]:
                    if k in tmp:
                        x+=1
                if x==0:
                    for k in num[j]:
                        tmp.append(k)
                    tar.append(num[i]+num[j])
        return tar[:]

    def rec(self,n,num):
        if n==1:
            return num
        return self.rec(n/2,self.fun(num))

    def show(self):
        [print (i,end=' ') for i in self.tar]

if __name__ == '__main__':
    leaf=leaves(4)
    print(leaf.get())
    print(leaf.get())
    print(leaf.get())
    print(leaf.get())
    #leaf.show()
